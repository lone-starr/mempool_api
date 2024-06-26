
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
OWM_API_KEY = os.environ.get('OWM_API_KEY')


def authenticate(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return True


@app.get("/pulldata", dependencies=[Depends(authenticate)])
async def pulldata():
    try:
        bh_response = requests.get(
            "https://mempool.space/api/blocks/tip/height")
        blockheight = bh_response.json()
    except:
        blockheight = None

    try:
        mp_response = requests.get("https://mempool.space/api/mempool")
        count = mp_response.json()["count"]
        vsize = mp_response.json()["vsize"]
    except:
        count, vsize = None, None

    try:
        hr_response = requests.get(
            "https://mempool.space/api/v1/mining/hashrate/3d")

        hashrate = int(hr_response.json()["currentHashrate"])
        difficulty = float(hr_response.json()["currentDifficulty"])
    except:
        hashrate, difficulty = 0, 0

    try:
        fee_response = requests.get(
            "https://mempool.space/api/v1/fees/recommended")
        minimumFee = fee_response.json()["minimumFee"]
        fastestFee = fee_response.json()["fastestFee"]
        hourFee = fee_response.json()["hourFee"]
        halfHourFee = fee_response.json()["halfHourFee"]
    except:
        minimumFee, fastestFee, hourFee, halfHourFee = None, None, None, None

    try:
        p_response = requests.get("https://mempool.space/api/v1/prices")
        priceUSD = p_response.json()["USD"]
        priceEUR = p_response.json()["EUR"]
        priceGBP = p_response.json()["GBP"]
        priceCAD = p_response.json()["CAD"]
        priceJPY = p_response.json()["JPY"]
    except:
        priceUSD, priceEUR, priceGBP,  priceCAD, priceJPY = None, None, None, None, None

    data = {
        "height": blockheight,
        "count": count,
        "vsize": vsize,
        "hashrate": hashrate/1000000000000000,
        "diff": difficulty/1000000000000,
        "minimumFee": minimumFee,
        "fastestFee": fastestFee,
        "hourFee": hourFee,
        "halfHourFee": halfHourFee,
        "austinTemp": pullweatherdata(),
        "priceUSD": priceUSD,
        "priceEUR": priceEUR,
        "priceGBP": priceGBP,
        "priceCAD": priceCAD,
        "priceJPY": priceJPY,
        "ts": datetime.now()
    }

    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client['mempool']
        collection = db['blockheight']
        collection.insert_one(data)
        mongo_client.close()
    except:
        return {"Error occured while inserting data into MongoDB"}

    return {blockheight}


def pullweatherdata():
    # coordinates for Austin, TX
    lat = 30.266
    long = -97.733
    try:
        w_response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&units=imperial&appid={OWM_API_KEY}")
        temp = w_response.json()["main"]["temp"]
    except:
        temp = None

    return temp
