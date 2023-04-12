# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0

import string
import random
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from model import *
from config import *

router = APIRouter()

# Check if API key is valid
@router.post("/api/{key}", response_class=HTMLResponse)
async def apiCheckKey(key: str):
    rs = await authdb.find_one({"key": key})
    if rs:
        return JSONResponse({"status": "success"})
    else:
        return JSONResponse({"status": "error", "message": "Invalid API key"})

# Create shorten URL
@router.post("/api/{key}/create", response_class=HTMLResponse)
async def apiCreateShorten(key: str, url: str):
    rs = await authdb.find_one({"key": key})
    if rs:
        short = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        while await mongodb.find_one({"short": short}):
            short = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        r = await mongodb.insert_one({
            "url": url,
            "short": short,
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "secured": 0,
            "views": 0,
            "ads": 0,
            "report": 0,
        })
        await authdb.update_one({"key": key}, {'$push': {'short': str(r.inserted_id)}})
        return JSONResponse({"status": "success", "short": f"{DOMAIN}s/{short}"})
    else:
        return JSONResponse({"status": "error", "message": "Invalid API key"})

# 
@router.post("/api/{key}/createSecure", response_class=HTMLResponse)
async def apiCreateSecuredShorten(key: str, url: str, password: str):
    rs = await authdb.find_one({"key": key})
    if rs:
        scode = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        while await mongodb.find_one({"scode": scode}):
            scode = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        await mongodb.insert_one({
            "url": url,
            "scode": scode,
            "password": password,
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "secured": 1,
            "views": 0,
            "ads": 0,
            "report": 0,
        })
        return JSONResponse({"status": "success", "short": f"{DOMAIN}secured/{scode}"})
    else:
        return JSONResponse({"status": "error", "message": "Invalid API key"})

# 
@router.post("/api/{key}/visitor", response_class=HTMLResponse)
async def api(key: str, short: str, password: Optional[str] = None):
    rs = await authdb.find_one({"key": key})
    if rs:
        try:
            if password == None:
                r = await mongodb.find_one({"short": short})
            else:
                r = await mongodb.find_one({"scode": short, "password": password})
            return JSONResponse({"status": "success", "visitors": r["views"]})
        except Exception as e:
            print(e)
            return JSONResponse({"status": "error", "message": "Check your data"})
    else:
        return JSONResponse({"status": "error", "message": "Invalid API key"})

# 
@router.post("/api/{key}/reports", response_class=HTMLResponse)
async def api(key: str, short: str, password: Optional[str] = None):
    rs = await authdb.find_one({"key": key})
    if rs:
        try:
            if password == None:
                r = await mongodb.find_one({"short": short})
            else:
                r = await mongodb.find_one({"scode": short, "password": password})
            return JSONResponse({"status": "success", "reports": r["report"]})
        except Exception as e:
            print(e)
            return JSONResponse({"status": "error", "message": "Check your data"})
    else:
        return JSONResponse({"status": "error", "message": "Invalid API key"})
    
# 
@router.post("/api/{key}/delete", response_class=HTMLResponse)
async def api(key: str, short: str, password: Optional[str] = None):
    rs = await authdb.find_one({"key": key})
    if rs:
        try:
            if password:
                await mongodb.delete_one({"scode": short, "password": password})
            else:
                await mongodb.delete_one({"short": short})
            return JSONResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JSONResponse({"status": "error", "message": "Check your data"})
    else:
        return JSONResponse({"status": "error", "message": "Invalid API key"})