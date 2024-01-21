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
    bh_response = requests.get("https://mempool.space/api/blocks/tip/height")
    blockheight = bh_response.json()
    count = 0
    vsize = 0
    data = {
        "height": blockheight,
        "count": count,
        "vsize": vsize,
        "ts": datetime.now()
    }
    save_data(data)
    return {blockheight}


def save_data(data):
    db = get_db('blockheight')
    db.insert_one(data)
    return data


def get_db(db_name):
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client['mempool']
    return db[db_name]
