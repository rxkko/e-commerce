from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserResponse, UserCreate, UserLogin
from deps.user_deps import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: UserResponse = Depends(get_current_user)):
    return {current_user}