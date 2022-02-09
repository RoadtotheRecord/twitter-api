import uvicorn
from fastapi import FastAPI, HTTPException
from routers.twitter import router as twitter_router
from routers.spreadsheet import router as spreadsheet_router
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title='Road to the Record API',
              description='Road to the Record API from REST API',
              version='0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(twitter_router, prefix='/twitter', tags=['twitter'])
app.include_router(spreadsheet_router, prefix='/spreadsheet', tags=['spreadsheet'])

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', reload=True)