# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0

import os
import motor.motor_asyncio

DOMAIN = os.getenv("DOMAIN")

# MongoDB connection
MONGODB_NAME = "quickly" # os.getenv("MONGODB_NAME")
MONGODB_COL = "quickly" # os.getenv("MONGODB_COL")
MONGODB_URL = os.getenv("MONGODB_URL")
mongoClient =  motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
mongodb = mongoClient[MONGODB_NAME][MONGODB_COL]
MONGODB_NAME2 = "quicklyAuth" # os.getenv("MONGODB_NAME2")
MONGODB_COL2 = "quicklyAuth" # os.getenv("MONGODB_COL2")
MONGODB_URL2 = os.getenv("MONGODB_URL2")   
mongoAuthClient =  motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
authdb = mongoClient[MONGODB_NAME2][MONGODB_COL2]

# Chat ID
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
CHAT_ID = str(os.getenv("CHAT_ID"))

# JWT
SECRET_KEY = str(os.getenv("SECRET_KEY"))
SALT = str(os.getenv("SALT"))
