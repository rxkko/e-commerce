from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate
from models import User
from ..security.password_service import hash_password


async def create_user(db: AsyncSession, user_data: UserCreate):
    existing_user = await db.execute(
        select(User).where(
            or_(
                User.email == user_data.email,
                User.username == user_data.username
            )
        )
    )
    user = existing_user.scalars().first()
    if user:
        if user.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if user.username == user_data.username:
            raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# async def get_user_by_login(db: AsyncSession, login: str):
#     if "@" in login:
#         result =  await db.execute(select(User).where(User.email == login))
#     else:
#         result = await db.execute(select(User).where(User.username == login))
#     return result.scalars().first()

