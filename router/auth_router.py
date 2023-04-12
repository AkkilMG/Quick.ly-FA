# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0

import uuid
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from bson import ObjectId

from model import *
from config import *
from utils.auth import Auth

router = APIRouter()

templates = Jinja2Templates(directory=["templates", "templates/auth"])


# Signin
@router.post("/signin", response_class=HTMLResponse)
async def signin(request: Request, response: Response): #
    try:
        form_data = await request.form()
        username = form_data.get("username")
        password = await Auth.hash_password(form_data.get("password"))
        res = await authdb.find_one({'username': username, 'password': password})
        if res:
            return RedirectResponse("/dashboard")
        else:
            context={
                "request": request,
                "error": "User not found. Please check your username/password",
                "bg": request.url_for("static", path="home.jpg"),
                "auth": bool(1)
            }
        return templates.TemplateResponse("signin.html", context)
    except Exception as e:
        print(e)
        return RedirectResponse("/error")
   
@router.get("/signin", response_class=HTMLResponse)
async def signin(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("signin.html", context)
    
# Signup
@router.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, response: Response):
    form_data = await request.form()
    email = form_data.get("email")
    if await authdb.find_one({'email': email}):
        context={
            "request": request,
            "error": "Email already exists",
            "bg": request.url_for("static", path="home.jpg"),
            "auth": bool(1)
        }
        return templates.TemplateResponse("signup.html", context)
    if (form_data.get("password") == form_data.get("confirm_password")):
        ps = str(form_data.get("password"))
        check, error = await Auth.authPassword(ps)
        if check:
            context={
                "request": request,
                "error": error,
                "bg": request.url_for("static", path="home.jpg"),
                "auth": bool(1)
            }
            return templates.TemplateResponse("signup.html", context)
        password = await Auth.hash_password(ps)
    else:
        context={
            "request": request,
            "error": "Check your password",
            "bg": request.url_for("static", path="home.jpg"),
            "auth": bool(1)
        }
        return templates.TemplateResponse("signup.html", context)
    name = form_data.get("name")
    username = form_data.get("username")
    if await authdb.find_one({'username': username}):
        context={
            "request": request,
            "error": "Username already exists",
            "bg": request.url_for("static", path="home.jpg"),
            "auth": bool(1)
        }
        return templates.TemplateResponse("signup.html", context)
    gender = form_data.get("gender")
    key = await Auth.key(username, email)
    res = {
        "name": name,
        "email": email,
        "password": password,
        "username": username,
        "verified": 0,
        "admin": 0,
        "gender": gender,
        "created_at": datetime.utcnow(),
        "key": key,
        "short": []
    }
    rt = await authdb.insert_one(res)
    # if await Auth.emailVerify(name, email, f"{DOMAIN}/verify/{rt.inserted_id}"):
    context={
            "request": request,
            "auth": bool(1),
            "bg": request.url_for("static", path="home.jpg"),
    }
    return templates.TemplateResponse("signin.html", context)
    # else:
    #     context={
    #         "request": request,
    #         "error": "Something went wrong",
    #         "bg": request.url_for("static", path="home.jpg"),
    #         "auth": bool(1)
    #     }
    #     return templates.TemplateResponse("signup.html", context)
    
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }   
    return templates.TemplateResponse("signup.html", context)

# Signout
@router.get("/signout", response_class=HTMLResponse)
async def signout(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }   
    return templates.TemplateResponse("signup.html", context)

# Reset password
@router.get("/reset-password/{id}", response_class=HTMLResponse)
async def resetPassword(request: Request, response: Response, id: str):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
    }   
    return templates.TemplateResponse("signup.html", context)

@router.post("/reset-password/{id}", response_class=HTMLResponse)
async def resetPassword(request: Request, response: Response, id: str):
    form_data = await request.form()
    if (form_data.get("password") == form_data.get("confirm_password")):
        ps = str(form_data.get("password"))
        check, error = await Auth.authPassword(ps)
        if check:
            context={
                "request": request,
                "error": error,
                "bg": request.url_for("static", path="home.jpg"),
                "auth": bool(1)
            }
            return templates.TemplateResponse("setPassword.html", context)
        password = await Auth.hash_password(ps)
    else:
        context={
            "request": request,
            "error": "Check your password",
            "bg": request.url_for("static", path="home.jpg"),
            "auth": bool(1)
        }
        return templates.TemplateResponse("setPassword.html", context)
    rt = await authdb.update_one({'_id': ObjectId(id)}, {'$set': {'password': password}})
    if rt:
        context={
            "request": request,
            "bg": request.url_for("static", path="home.jpg"),
        }   
        return templates.TemplateResponse("setPassword.html", context)
