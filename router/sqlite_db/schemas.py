from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserCheck(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    consumer_key: str
    consumer_secret: str

class UserAccess(UserAuth):
    access_token: str
    access_token_secret: str

class UserCredentials(UserAccess):
    twitter_bearer_token: str

    class Config:
        orm_mode= True

class Follower(BaseModel):
    id: int
    user_id: int
    follower_name: str
    user: User

    class Config:
        orm_mode= True