from fastapi import HTTPException, Response
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

async def delete_user(db: AsyncSession, user_id: int, response: Response):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "User deleted successfully"}

