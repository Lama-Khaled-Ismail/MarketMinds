from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

# Add additional platforms in the future
class Platform(str, Enum):
    TWITTER = "Twitter"
    TALABAT = "Talabat"
    FACEBOOK = "Facebook"
    ELMENUS = "Elmenus"


class Review(BaseModel):
    text: str
    brand_id: int
    platform: Platform
    time: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    score: Optional[int] = None
    
