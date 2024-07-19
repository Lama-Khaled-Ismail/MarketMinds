import joblib
from passlib.context import CryptContext
from password_strength import PasswordPolicy
from fastapi import HTTPException

policy = PasswordPolicy.from_names(
    length=8,  # Minimum length: 8
    uppercase=1,  # Must have at least 1 uppercase letters
    numbers=1,  # Must have at least 1 digits
    special=1,  # Must have at least 1 special characters
    nonletters=0,  # Can have 0 or more non-letter characters (digits, specials, anything)
) 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str):
    errors = policy.test(password)
    if errors :
        raise ValueError("Password not strong enough")
    
    return True

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


