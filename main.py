from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from urllib.parse import quote
from dotenv import load_dotenv
from pymongo import MongoClient
import requests


app = FastAPI()


@app.get("/getblocktip")
async def getblocktip():
    url = "https://mempool.space/api/blocks/tip/height"
    response = requests.get(url)
    response_json = response.json()
    return {response_json}
