import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from database import get_db
from models import Staff as StaffModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    error = HTTPException(status_code=401, detail="Could Not Validate Credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise error
        
        return username
    except JWTError:
        raise error
    
def get_current_manager(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    error = HTTPException(status_code=403, detail="Forbidden Access")
    try:
        get_user = get_current_user(token)
        db_user = db.query(StaffModel).filter(StaffModel.username == get_user).first()
        if db_user is None:
            raise HTTPException(status_code=401, detail="Manager Not Found.")
        if db_user.role.lower() != "manager":
            raise error
        
        return db_user
    except JWTError:
        return HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        return HTTPException(status_code=401, detail="Invalid token")