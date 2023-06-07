from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
import utils
from jose import jwt
from datetime import datetime, timedelta,timezone
import configparser
from .sqlite_db import models, schemas, endpoint
from .sqlite_db import database

config= configparser.ConfigParser()
config.read('config.ini')
jwt_secret= config['secret']['jwt_secret']
models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def encode(user: str):
    try:    
        payload={
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "subject": user
        }
        encoded_token=jwt.encode(payload, jwt_secret, algorithm='HS256')
        return encoded_token
    except Exception as err:
        pass

def decode(token):
    try:
        result=jwt.decode(token, jwt_secret, algorithms='HS256')
        return result
    except Exception as err:
        pass

@router.get("/user", tags=['authenticate'])
async def get_user(skip: int = 0, limit: int = 100):
    res=database.SessionLocal().query(models.User).offset(skip).limit(limit).all()
    database.SessionLocal().close()
    return res


@router.post('/rlogin', tags=['authenticate'])
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    res=endpoint.get_user(user= user, db= db)
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        resp=encode(user= user.email)
        return resp
    
@router.post('/login', tags=['authenticate'])
async def login(user: schemas.UserCreate):
    res=database.SessionLocal().query(models.User).filter(models.User.email == user.email).all()
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        resp=encode(user= user.email)
        return resp

@router.post('/rregister', tags=['authenticate'])
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password=utils.get_hashed_password(user.password)
    resp=endpoint.create_user(user= user, db= db, hashed_password= hashed_password)
    return resp

@router.post('/register', tags=['authenticate'])
async def register(user: schemas.UserCreate):
    hashed_password=utils.get_hashed_password(user.password)
    new_user=models.User(email= user.email, hashed_password= hashed_password)
    database.SessionLocal().add(new_user)
    database.SessionLocal().commit()
    database.SessionLocal().refresh(new_user)
    return new_user
    
@router.get('/validate', tags=['authenticate'])
async def validate(token: str):
    res=decode(token)
    if res is None:
        raise HTTPException(status_code=401, detail='Unauthorized user')
    else:
        return res
