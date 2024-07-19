from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from postgres import models
from routers import auth, brand, user, web_scraper, prediction
from postgres.database import SessionLocal, engine
from english_model.needed_fucntions import text_data_cleaning
from arabic_model.needed_ar import clean_arabic_text

models.Base.metadata.create_all(bind=engine)
from lifespan import lifespan


app = FastAPI(lifespan=lifespan)

# add routers here
app.include_router(auth.router)
app.include_router(brand.router)
app.include_router(user.router)
app.include_router(web_scraper.router)
app.include_router(prediction.router)


    
     


        


origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


@app.get("/")
def read_root():
    return {"message": "first api in our project"}