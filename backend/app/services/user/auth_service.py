from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserLogin
from ..security.password_service import verify_password

async def authenticate_user(db: AsyncSession, user_data: UserLogin):
    if "@" in user_data.login:
        result =  await db.execute(select(User).where(User.email == user_data.login))
    else:
        result = await db.execute(select(User).where(User.username == user_data.login))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    elif not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    return user