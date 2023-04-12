

import hashlib
import jwt
import string
import random
from jwt.exceptions import DecodeError
# import smtplib
# # import asyncio
# import random
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from datetime import datetime, timedelta

from config import *

class Auth():
    @staticmethod
    async def authPassword(password: str):
        if len(password) < 8:
            return True, "Password must be at least 8 characters"
        if len(password) > 18:
            return True, "Password must be at most 18 characters"
        if not any(char.isdigit() for char in password):
            return True, "Password must contain at least 1 number"
        if not any(char.isupper() for char in password):
            return True, "Password must contain at least 1 uppercase letter"
        if not any(char.islower() for char in password):
            return True, "Password must contain at least 1 lowercase letter"
        if not any(char in ".!@#$%^&*()_+-=" for char in password):
            return True, "Password must contain at least 1 special character"
        return False, None

    @staticmethod
    async def hash_password(password: str):
        hashed_password = hashlib.sha256(password.encode('utf-8') + SALT.encode('utf-8')).hexdigest()
        return hashed_password
    
    @staticmethod
    async def check_password(password: str, hashed_password: str):
        test_hashed_password = hashlib.sha256(password.encode('utf-8') + SALT.encode('utf-8')).hexdigest()
        return test_hashed_password == hashed_password
    
    @staticmethod
    def create_access_token(data: dict):
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode = data.copy()
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str):
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_jwt
        except DecodeError:
            return None
        
    @staticmethod
    async def key(username: str, email: str):
        k = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))
        return hashlib.sha256((username + email).encode('utf-8') + k.encode('utf-8')).hexdigest()[:24]

    # @staticmethod
    # async def emailVerify(name:str, mail:str, url:str):
    #     try:
    #         server = smtplib.SMTP('smtp.gmail.com', 587)
    #         server.starttls()
    #         server.login(MAIL, PASS)
    #         message = MIMEMultipart("alternative")
    #         message["Subject"] = "Mail verification"
    #         message["From"] = MAIL
    #         message["To"] = mail
    #         msg = MIMEText(MSG_EMAIL.format(name=name, verify1=url, verify2=url), "html")
    #         message.attach(msg)
    #         server.sendmail(MAIL, mail, message.as_string())
    #         server.quit()
    #         return True
    #     except Exception as e:
    #         print(f"Email verified: {{e}}")
    #         return False

    # @staticmethod
    # async def phoneNumberVerify(name:str, phone:str):
    #     otp = ''.join([str(random.randint(0,9)) for i in range(6)])
        
    #     return otp
    
    # @staticmethod
    # async def emailForgotPassword(name:str, mail:str, url:str):
    #     try:
    #         server = smtplib.SMTP('smtp.gmail.com', 587)
    #         server.starttls()
    #         server.login(MAIL, PASS)
    #         message = MIMEMultipart("alternative")
    #         message["Subject"] = "Reset password"
    #         message["From"] = MAIL
    #         message["To"] = mail
    #         msg = MIMEText(PASS_MSG_EMAIL.format(name=name, reset1=url, reset2=url), "html")
    #         message.attach(msg)
    #         server.sendmail(MAIL, mail, message.as_string())
    #         server.quit()
    #     except Exception as e:
    #         print("Auth: "+e)
