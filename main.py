from fastapi import FastAPI
from fastapi import FastAPI, Depends, Header, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from pymongo import MongoClient
import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

MONGO_URI = os.environ.get('MONGO_URI')
API_KEY = os.environ.get('API_KEY')


def authenticate(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return True


@app.get("/getblocktip", dependencies=[Depends(authenticate)])
async def getblocktip():
    bh_response = requests.get("https://mempool.space/api/blocks/tip/height")
    blockheight = bh_response.json()
    mp_response = requests.get("https://mempool.space/api/mempool")
    count = mp_response.json()["count"]
    vsize = mp_response.json()["vsize"]
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


def get_db(db_name: str):
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client['mempool']
    return db[db_name]
