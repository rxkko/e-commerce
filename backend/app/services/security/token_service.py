from fastapi import HTTPException
from jose import jwt
from jwt import decode, PyJWTError
from datetime import datetime, timedelta, timezone
from schemas import TokenData
from core.config import settings


def create_access_token(data: TokenData):
    to_encode = data.model_dump(exclude_none=True)
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: TokenData):
    to_encode = data.model_dump(exclude_none=True)
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_refresh_token(refresh_token: str):
    try:
        payload = decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        return None
    
async def refresh_access_token(refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = create_access_token(data=payload)
    return {"access_token": access_token}