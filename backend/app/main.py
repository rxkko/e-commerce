import httpx
from fastapi import FastAPI
from routes.user import auth_route as auth

app = FastAPI()

app.include_router(auth.router, prefix="/user", tags=["user"])