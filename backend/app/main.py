from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import models
from routers import auth
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# add routers here
app.include_router(auth.router)


        
# TODO uncomment later
'''

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)
'''

@app.get("/")
def read_root():
    return {"message": "first api in our project"}