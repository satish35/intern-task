from sqlalchemy.orm import Session
from . import models, schemas

def get_user(user: schemas.UserCreate, db: Session):
    res=db.query(models.User).filter(models.User.email == user.email).all()
    return res

def create_user(user: schemas.UserCreate, db: Session, hashed_password: str):
    new_user=models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
