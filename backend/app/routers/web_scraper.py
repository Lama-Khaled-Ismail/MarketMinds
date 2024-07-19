from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from postgres.database import get_db
from postgres import models, schemas
import oauth2
import httpx
from mongo import schemas as mongo_schema
from mongo import models as mongo_model
from mongo.database import english_collection




router = APIRouter(
    prefix="/scrape",
    tags=["Scraper"],
)
"""
@router.post("/review")
def post_todo(review: models.Review):
    english_collection.insert_one(dict(review))
"""
    
# api to get english reviews and store in db
@router.post("/twitter/{lang}/{brand_name}",status_code=status.HTTP_201_CREATED)
async def scrape_twitter_en(lang: str,brand_name:str, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    brand =  db.query(models.Brand).filter(models.Brand.name==brand_name).first()
    
    alt_names = [alt_name.altname for alt_name in brand.alt_names]
    alt_names.append(brand_name)
    
    request = mongo_schema.TwitterRequest(
        brandnames=alt_names,
        lang= lang,
        )
    
    api_url = "http://localhost:8080/scrape"
    json_data = request.model_dump()
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, json=json_data, timeout=60.0)
        if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from the other API")
            
        
        response = response.json()
        tweets = response["tweets"]
        if tweets is None:
            print("No tweets found.")
    
        for tweet in tweets:
            review = mongo_model.Review(
                text=tweet,
                brand_id=brand.id,
                platform=mongo_model.Platform.TWITTER
            )
            english_collection.insert_one(dict(review))
            
        return tweets
    
# api to get arabic reviews and store in db

