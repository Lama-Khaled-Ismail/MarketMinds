from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session
import oauth2, utils, crud.crud_user as crud_user
from postgres import schemas, models
from postgres.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


# TODO captilize Name
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # add to db
        db_user = crud_user.create_user(user,db)
    
        # token
        access_token = oauth2.create_access_token(data= {"uid":db_user.id})
    
        return {"access_token": access_token, "token_type": "bearer"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.post("/login")
def login(user_cred: schemas.UserLogin, db: Session = Depends(get_db)):
    
   user = db.query(models.User).filter(models.User.email == user_cred.email).first()
   # wrong email
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
   
   # wrong password
   if not utils.verify(user_cred.password, user.password):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
   
   # token 
   access_token = oauth2.create_access_token(data= {"uid":user.id})
    
   return {"access_token": access_token, "token_type": "bearer"}
    
    