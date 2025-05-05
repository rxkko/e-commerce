from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserResponse, UserCreate, UserLogin
from deps.db import get_db

router = APIRouter()

@router.post("/login")
def login():
    return "hello"