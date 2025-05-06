from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from schemas import UserResponse
from deps.user_deps import get_current_user
from deps import get_db
from services.user.user_service import delete_user

router = APIRouter()
templates = Jinja2Templates(directory="../app/templates")

@router.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, current_user: UserResponse = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "current_user": current_user})

@router.post("/delete/{user_id}")
async def user_delete(response: Response, user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user(db, user_id, response)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)