from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.templating import Jinja2Templates
from schemas import UserResponse
from deps.user_deps import get_current_user
from deps import get_db
from models import User

router = APIRouter()
templates = Jinja2Templates(directory="../app/templates")

@router.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, current_user: UserResponse = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "current_user": current_user})

@router.post("/delete/{user_id}")
async def user_delete(response: Response, user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    await db.delete(user)
    await db.commit() 
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)