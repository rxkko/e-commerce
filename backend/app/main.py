import httpx
from fastapi import FastAPI
from routes.user import auth_route as auth
from routes.user import user_crud_route as user

app = FastAPI()

app.include_router(auth.router, prefix="/user", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])