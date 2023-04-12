# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0


import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import *

import router.app_router as app_router
import router.admin_router as admin_router
import router.user_router as user_router
import router.auth_router as auth_router
import router.page_router as page_router

app = FastAPI(
    title="Shortener",
    description="This is an application as a service for shortening URLs",
    version="0.0.1",
    contact={
        "name": "Akkil M G",
        "url": "http://github.com/HeimanPictures",
    },
    license_info={
        "name": "GNU GENERAL PUBLIC License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)

origins = [
    "http://localhost:3000",
    "http://localhost:5000",
    DOMAIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(app_router.router)
app.include_router(page_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(admin_router.router)

# for local testing
if __name__ == "__main__":
  uvicorn.run("main:app", host="localhost", port=10000, reload=True)