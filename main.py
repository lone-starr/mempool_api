from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from urllib.parse import quote
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import os
from dotenv import load_dotenv
from pymongo import MongoClient

app = FastAPI()


@app.get("/blocktip")
async def root():
    return {"height": "826590"}
