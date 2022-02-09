import os
import requests
from fastapi import APIRouter

url = None
router = APIRouter()

@router.on_event('startup')
async def startup():
    global url
    web_app_id = os.getenv("WEB_APP_ID")
    sheet_id = os.getenv("SHEET_ID")

    url = f"https://script.google.com/macros/s/{web_app_id}/exec?id={sheet_id}&sheet="

@router.on_event('shutdown')
async def shutdown():
    global url
    url = None

@router.get('/')
async def get_sheet(sheet: str):
    req_url = url + sheet

    res = requests.get(req_url)
    return res.json()
