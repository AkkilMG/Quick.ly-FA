# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0


from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from model import *
from config import *

router = APIRouter()

templates = Jinja2Templates(directory=["templates", "templates/admin"])


# Dashboard
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("adminDashboard.html", context)

@router.post("/admin/dashboard", response_class=HTMLResponse)
async def admin(request: Request, response: Response):
    context={
        "request": request,
        "bg": request.url_for("static", path="home.jpg"),
        "auth": bool(1)
    }
    return templates.TemplateResponse("adminDashboard.html", context)
    