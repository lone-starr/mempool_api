from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from urllib.parse import quote
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient
import os
import requests

MONGO_URI = os.environ.get('MONGO_URI')

app = FastAPI()


@app.get("/getblocktip")
async def getblocktip():
    url = "https://mempool.space/api/blocks/tip/height"
    response = requests.get(url)
    response_json = response.json()
    save_blockheight(response_json)
    return {response_json}


def save_blockheight(blockheight):
    data = {
        "height": blockheight,
        "ts": datetime.now()
    }
    db = get_db('blockheight')
    db.insert_one(data)


def get_db(db_name):
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client['mempool']
    return db[db_name]
