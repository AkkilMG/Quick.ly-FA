# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0

import os
import random
import string
import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from model import *
from config import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Common intreface/User interface
## Home 
### GET
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("home.html", context)

### POST
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
        "views": 0,
        "ads": 0,
        "report": 0,
    })
    context={
        "request": request,
        "short": f"{DOMAIN}/s/{short}",
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("home.html", context)

## Short Redirect
@router.get("/s/{short}")
async def short(short: str):
    rs = await mongodb.find_one({"short": short})
    if rs:
        await mongodb.update_one({"short": short}, {"$inc": {"views": 1}})
        return RedirectResponse(rs["url"])
    else:
        return RedirectResponse(f"{DOMAIN}/error")

## Error page
@router.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="error.jpg")
    }
    return templates.TemplateResponse("error.html", context)

## Report
### GET
@router.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="error.jpg")
    }
    return templates.TemplateResponse("report.html", context)

### POST
@router.post("/report", response_class=HTMLResponse)
async def report(request: Request, short: str):
    await mongodb.update_one({"short": short}, {"report": 1})
    context={
        "request": request,
        "bg": request.url_for("static", path="error.jpg")
    }
    return templates.TemplateResponse("report.html", context)

## Dashboard
### GET
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("dashboard.html", context)

### POST
@router.post("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    context = {
        "request": request,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("dashboard.html", context)

# Pages
@router.post("/contact", response_class=HTMLResponse)
async def contact(request: Request, response: Response):
    try:
        form_data = await request.form()
        payload = {
            "chat_id": CHAT_ID, 
            "text": f"New message from Shortner:\nEmail: " + form_data.get("email") + "\nSubject: " + form_data.get("subject") + "\nMessage: " + form_data.get("message")
        }
        res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", headers={"Content-Type": "application/json"}, json=payload)
        if res.status_code == 200:
            context={
                "request": request,
                "bg": request.url_for("static", path="home.jpg"),
                "message": "Message sent successfully!"
            }
        else:
            context={
                "request": request,
                "bg": request.url_for("static", path="home.jpg"),
                "message": f"Error sending message: {res.status_code} {res.text}"
            }
        return templates.TemplateResponse("contact.html", context)
    except Exception as e:
        print(e)
        return RedirectResponse(f"{DOMAIN}/error")

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("contact.html", context)


# Blog
@router.get("/blogs", response_class=HTMLResponse)
async def contact(request: Request, response: Response):
    context={
        "request": request,
        "posts": POSTS,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("contact.html", context)


# Admin
## Dashboard
### GET
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("adminDashboard.html", context)

### POST
@router.post("/admin/dashboard", response_class=HTMLResponse)
async def admin(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg")
    }
    return templates.TemplateResponse("adminDashboard.html", context)
    
