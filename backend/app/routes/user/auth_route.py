from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserResponse, UserCreate, UserLogin
from deps.db import get_db
from services.security.token_service import create_access_token, create_refresh_token
from services.user.user_service import create_user
from services.user.auth_service import authenticate_user
from core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(db, user)
    return new_user

@router.post("/login", response_model=UserResponse)
async def login(user_data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user_data)
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*86400)
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        username=user.username,
        is_active=user.is_active
    )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Successfully logged out"}

