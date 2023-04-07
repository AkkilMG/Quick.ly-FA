# (c) 2022-2023, Akkil M G (https://github.com/HeimanPictures)
# License: GNU General Public License v3.0


from pydantic import BaseModel
from typing import Optional, TypeVar
from datetime import datetime

T = TypeVar('T')

class Vehicle(BaseModel):
    pass