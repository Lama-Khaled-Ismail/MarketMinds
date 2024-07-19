from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import datetime
from typing import List, Optional
from utils import validate_password


from pydantic.types import conint

common_words = ['password', '123456', 'qwerty']


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v:str) -> str:
        validate_password(v)
         # Check for spaces
        if ' ' in v:
            raise ValueError("Password cannot contain spaces")
        
        if any(common_word in v.lower() for common_word in common_words):
            raise ValueError('Password contains a common word or phrase')
        
        return v
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserReset(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    
class Altname(BaseModel):
    altname: str
    
    class Config:
        from_attributes = True
        
    def __str__(self):
        return self.altname
    
class Brand(BaseModel):
    name: str
    alt_names: List[Altname]
    
    class Config:
        from_attributes = True
        
class BrandOut(BaseModel):
    name: str
    alt_names: List[Altname] = Field(default_factory=list)
    
    @model_validator(mode='after')
    def convert_altnames(cls, values):
        values.alt_names = [Altname(altname=altname) if isinstance(altname, str) else altname for altname in values.alt_names]
        return values
    
    class Config:
        from_attributes = True    
        
class BrandAltnames(BaseModel):
    alt_names: List[Altname] = Field(default_factory=list)
    
    @model_validator(mode='after')
    def convert_altnames(cls, values):
        values.alt_names = [Altname(altname=altname) if isinstance(altname, str) else altname for altname in values.alt_names]
        return values
    
    class Config:
        from_attributes = True
    
class UserOut(BaseModel):
    email: EmailStr
    username: str
    brands: List[Brand] = []
    created_at: datetime

    class Config:
        from_attributes = True

class UserBrands(BaseModel):
    brands: List[BrandOut] = []
    
    class Config:
        from_attributes = True
 
# TODO   
class BrandCreate(BaseModel):
    pass
    
class Review(BaseModel):
    text: str
    score: bool
    
class AnalysisOut(BaseModel):
    
    positive: int
    negative: int
    num_reviews: int
    created_at: datetime
    platform: str
    language: str
    reviews: List[Review] = []
    class Config:
        from_attributes = True
 
    
