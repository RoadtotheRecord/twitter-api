import os
import time
import base64
from typing import Optional
from requests_oauthlib import OAuth1Session
from fastapi import APIRouter
from pydantic import BaseModel

twitter_api = None
router = APIRouter()

class StatusItem(BaseModel):
    status: str
    id: int = None
    media: Optional[bytes] = None

class DestroyItem(BaseModel):
    id: int

@router.on_event('startup')
async def startup():
    global twitter_api
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    twitter_api = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

@router.on_event('shutdown')
async def shutdown():
    global twitter_api
    twitter_api = None

@router.get('/')
async def user_timeline(count: int = 10):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': count,
        'exclude_replies': False,
        'include_rts': False,
        'tweet_mode': 'extended'
    }

    res = twitter_api.get(url, params = params)
    return res.json()

@router.get('/show')
async def show(tweet_id: int):
    url = f"https://api.twitter.com/1.1/statuses/show/{tweet_id}.json?tweet_mode=extended"

    res = twitter_api.get(url)
    return res.json()

@router.post('/post')
async def update_status(item: StatusItem):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {'status': item.status}

    if item.id:
        params["in_reply_to_status_id"] = item.id

    if item.media:
        split_point = str(item.media).find(",") - 1
        media_type = str(item.media[:split_point])
        replace_media = item.media[split_point:]
        decode_media = base64.b64decode(replace_media)
        if "video" in media_type:
            params["media_ids"] = upload_movie(decode_media)
        elif "image" in media_type:
            params["media_ids"] = upload_image(decode_media)

    res = twitter_api.post(url, params=params)
    return res.json()

@router.post('/destroy')
async def destroy(item: DestroyItem):
    url = f"https://api.twitter.com/1.1/statuses/destroy/{item.id}.json"

    res = twitter_api.post(url)
    return res.json()

def upload_image(media) -> str:
    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    files = {"media" : media}

    req_media = twitter_api.post(url_media, files = files)
    return req_media.json()['media_id']

def upload_movie(media) -> str:
    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    total_bytes = len(media)

    # INIT
    init_params = {
        "command": "INIT",
        "media_type": "video/mp4",
        "total_bytes": total_bytes,
        "media_category": "tweet_video"
    }
    res_init = twitter_api.post(url_media, data=init_params)
    media_id = res_init.json()['media_id']

    # APPEND
    chunk_size = 4*1024*1024
    segment_id = 0
    bytes_start = 0
    bytes_end = chunk_size
    data = {
        'command': 'APPEND',
        'media_id': media_id,
        'segment_index': segment_id
    }
    while bytes_start < total_bytes:
        chunk = media[bytes_start:bytes_end]
        data["segment_index"] = segment_id
        files = {'media': chunk}
        twitter_api.post(url_media, data=data, files=files)
        bytes_start = bytes_end
        bytes_end += chunk_size
        if total_bytes < bytes_end:
            bytes_end = total_bytes
        segment_id += 1

    # FINALIZE
    finalize_params = {
        "command": "FINALIZE",
        "media_id": media_id
    }
    twitter_api.post(url_media, data=finalize_params)

    # STATUS
    status_params = {
        "command": "STATUS",
        "media_id": media_id
    }
    res_status = twitter_api.get(url_media, params=status_params)
    processing_info = res_status.json().get("processing_info", None)
    while processing_info["state"] == "in_progress":
        time.sleep(1)
        res_status = twitter_api.get(url_media, params=status_params)
        processing_info = res_status.json().get("processing_info", None)

    return media_id
