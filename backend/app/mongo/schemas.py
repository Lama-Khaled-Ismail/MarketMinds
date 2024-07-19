from enum import Enum
from pydantic import BaseModel
from typing import List

def individual_serial(review) -> dict:
    return{
        "id": str(review["_id"]),
        "text": review["text"],
        "platform": review["platform"],
        "time": review["time"]
        
    }
    
def list_serial(reviews) -> list:
    return[individual_serial(review) for review in reviews ]

class Language(str, Enum):
    ENGLISH = "en"
    ARABIC = "ar"
    

class TwitterRequest(BaseModel):
    brandnames: List[str]
    lang: Language
    maxTweets: int = 150