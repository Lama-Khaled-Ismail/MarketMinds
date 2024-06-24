from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

# TODO -> import issue
import schemas, models, utils

from database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

# TODO strong password
# TODO captilize Name
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    # TODO change this decrapted function
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user