from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


from pydantic.types import conint


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
