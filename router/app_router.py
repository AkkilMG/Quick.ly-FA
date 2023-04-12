# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0


import random
import string
from bson import ObjectId
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from model import *
from config import *
from utils.auth import Auth

router = APIRouter()

templates = Jinja2Templates(directory=["templates", "templates/app"])


# Home
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "urlLanding": request.url_for("static", path="urlLanding.avif"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("home.html", context)

@router.post("/", response_class=HTMLResponse)
async def home(request: Request):
    form_data = await request.form()
    url = form_data.get("url")
    short = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    while await mongodb.find_one({"short": short}):
        short = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    await mongodb.insert_one({
        "url": url,
        "short": short,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "secured": 0,
        "views": 0,
        "ads": 0,
        "report": 0,
    })
    context={
        "request": request,
        "short": f"{DOMAIN}s/{short}",
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("home.html", context)

# Secured Form
@router.get("/secured", response_class=HTMLResponse)
async def securedShortHome(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("securedShortForm.html", context)

@router.post("/secured", response_class=HTMLResponse)
async def securedShortHome(request: Request):
    form_data = await request.form()
    url = form_data.get("url")
    password = form_data.get("password")
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
    context={
        "request": request,
        "scode": f"{DOMAIN}secured/{scode}",
        "password": password,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("securedShortForm.html", context)

# Short Redirect
@router.get("/s/{short}")
async def short(short: str):
    rs = await mongodb.find_one({"short": short})
    if rs:
        await mongodb.update_one({"short": short}, { '$inc': { 'views': 1 } })
        return RedirectResponse(url=rs["url"], status_code=301)
    else:
        return RedirectResponse(url=f"/error", status_code=301)

# Delete shorten
@router.post("/delete")
async def deleteShorten(id: str):
    try:
        await mongodb.delete_one({"_id": ObjectId(id)})
        return JSONResponse({"status": "success"})
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)})

# Secured Short Redirect
@router.get("/secured/{scode}")
async def securedShort(request: Request, scode: str):
    rs = await mongodb.find_one({"scode": scode})
    if rs['secured'] == 1:
        context={
            "request": request,
            "bg": request.url_for("static", path="home.jpg"),
            "scode": scode,
            "auth": bool(1)
        }
        return templates.TemplateResponse("securedShort.html", context)
    else:
        return RedirectResponse(url=f"/error", status_code=301)
    
@router.post("/secured/{scode}")
async def securedShort(request: Request, scode: str):
    rs = await mongodb.find_one({"scode": scode})
    if rs['secured'] == 1:
        form_data = await request.form()
        password = form_data.get("password")
        res = await mongodb.find_one({"scode": scode, "password": password})
        if res:
            await mongodb.update_one({"scode": scode}, {"$inc": {"views": 1}})
            return RedirectResponse(url=rs["url"], status_code=301)
        else:
            return RedirectResponse(url=f"/error", status_code=301)
    else:
        return RedirectResponse(url=f"/error", status_code=301)

# Report
@router.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("report.html", context)

@router.post("/report", response_class=HTMLResponse)
async def report(request: Request):
    form_data = await request.form()
    url = form_data.get("url")
    if url.split('/')[-2] == "s":
        rs = await mongodb.find_one({"short": url.split('/')[-1]})
    else:
        rs = await mongodb.find_one({"scode": url.split('/')[-1]})

    if rs:
        await mongodb.update_one({"short": short}, {"report": 1})
        context={
            "request": request,
            "bg": request.url_for("static", path="home.jpg"),
            "auth": bool(1)
        }
        return templates.TemplateResponse("report.html", context)
    else:
        await mongodb.update_one({"short": short}, {"report": 1})
        context={
            "request": request,
            "bg": request.url_for("static", path="error.jpg"),
            "auth": bool(1),
            "error": "Invalid URL"
        }
        return templates.TemplateResponse("report.html", context)