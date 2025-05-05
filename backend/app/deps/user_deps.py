from fastapi import Request, HTTPException, Depends, Response
from jose import JWTError, jwt, ExpiredSignatureError
from core.config import settings
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .db import get_db
from services.security.token_service import verify_refresh_token, create_access_token

async def get_current_user(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    access_token = request.cookies.get("access_token")
    user_email = None

    if access_token:
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_email = payload.get("sub")
        except ExpiredSignatureError:
            pass 
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid access token")

    if not user_email:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        try:
            payload = verify_refresh_token(refresh_token)
            user_email = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token(data={"sub": user_email})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax"
        )

    result = await db.execute(select(User).where(User.email == user_email))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User not found or inactive")

    return user


async def get_current_user_with_role(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user = await get_current_user(request, response, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    return user