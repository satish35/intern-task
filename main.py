from fastapi import FastAPI, Response
from fastapi.requests import Request
from router import authenticate, twitter_access
from router.sqlite_db import schemas,endpoint

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root(request: Request):
    res=await authenticate.validate(request.cookies.get('token'))
    return {"hello": "world"}

@app.post("/login")
async def login(user: schemas.UserCreate, response: Response):
    res=await authenticate.login(user)
    return response.set_cookie(key='token', value=res)

@app.post("/register")
async def register(user: schemas.UserCreate):
    res=await authenticate.register(user)
    return res

@app.post("/twitter-login")
async def get_follower(user: schemas.UserCredentials, request: Request):
    res=await authenticate.validate(request.cookies.get('token'))
    resp=twitter_access.auth(user= user)
    return resp
'''after that using the email from res will try to find the user_id and pass in Follower table using follower schema'''

app.include_router(authenticate.router)