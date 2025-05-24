from pydantic import BaseModel

class User(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY= "mysecretkey"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =30

fake_users_db={
    "praveen":{
        "uesrname":"praveen",
        "password":pwd_context.hash("praveen@27")
    }
}


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def get_user(db,username:str):
    if username in db:
        return db[username]
    return None

def create_access_token(data:dict,expires_delta:timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt