from fastapi import Depends
from postgres import models, schemas
import utils, oauth2
from postgres.database import get_db
from sqlalchemy.orm import Session


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

# TODO change password

