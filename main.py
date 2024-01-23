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
    hr_response = requests.get(
        "https://mempool.space/api/v1/mining/hashrate/3d")
    hashrate = hr_response.json()["currentHashrate"]
    difficulty = hr_response.json()["currentDifficulty"]
    data = {
        "height": blockheight,
        "count": count,
        "vsize": vsize,
        "hashrate": hashrate/1000000000000000000,
        "diff": difficulty/1000000000000,
        "ts": datetime.now()
    }

    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client['mempool']
    collection = db['blockheight']
    collection.insert_one(data)
    mongo_client.close()

    return {blockheight}


# @app.get("/getblocks")
# async def getblocks():
#     db = get_db('blockheight')
#     result = db.find({})
#     return {result}
