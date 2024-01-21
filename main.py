from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from pymongo import MongoClient
import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

MONGO_URI = os.environ.get('MONGO_URI')

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
