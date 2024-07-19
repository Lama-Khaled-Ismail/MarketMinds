from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from postgres.database import get_db
from postgres import schemas, models
import oauth2
from utils import verify, hash


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

# get user info 
@router.get("/userinfo", response_model=schemas.UserOut)
def get_userinfo(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return current_user

@router.get("/userbrands", response_model=schemas.UserBrands)
def get_userbrands(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(user: schemas.UserReset, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.email == user.email and verify(user.old_password,current_user.password):
        db_user = db.query(models.User).filter(models.User.id==current_user.id).first()
        if db_user :
            db_user.password = hash(user.new_password)
            db.commit()
            return {"message" : "password changesd successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")