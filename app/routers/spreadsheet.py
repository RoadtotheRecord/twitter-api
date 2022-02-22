import os
import gspread
from fastapi import APIRouter
from oauth2client.service_account import ServiceAccountCredentials

scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
file = None
router = APIRouter()

@router.on_event('startup')
async def startup():
    global file
    file = client.open_by_key(os.getenv("FILE_KEY"))

@router.on_event('shutdown')
async def shutdown():
    global file
    file = None

@router.get('/')
async def get_sheet_all(sheet_name: str):
    sheet = file.worksheet(sheet_name)
    list_of_hashes = sheet.get_all_records()
    return list_of_hashes

@router.get('/line')
async def get_sheet_line(sheet_name: str, line: int):
    sheet = file.worksheet(sheet_name)
    return_json = {}
    header_list = sheet.row_values(1)
    values_list = sheet.row_values(int(line) + 1)
    for i in range(len(header_list)):
        return_json[header_list[i]] = values_list[i]
    return return_json

@router.get('/reload')
async def get_sheet_line():
    global file
    file = client.open_by_key(os.getenv("FILE_KEY"))
