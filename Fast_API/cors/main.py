from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from auth import Token, get_user, verify_password, create_access_token, fake_users_db
from datetime import timedelta
import jwt
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer

HTTP_401_UNAUTHORIZED = 401
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app = FastAPI()

origins = [
    'http://localhost'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET','POST','PUT','DELETE'],
    allow_headers=['*']
)

@app.get("/items/")
def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

@app.post("/token",response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=401,
    detail="Couldnotvalidatecredentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jwt.PyJWTError:
        raise credentials_exception
@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}. You have access to this route!"}