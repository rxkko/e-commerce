from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import UserResponse
from deps.user_deps import get_current_user
from deps.db import get_db
from models import User

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: UserResponse = Depends(get_current_user)):
    return {current_user}

@router.post("/delete/{user_id}")
async def user_delete(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar().first()

    await db.delete(user)
    await db.commit() 