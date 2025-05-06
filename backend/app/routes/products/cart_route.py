from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from deps import get_db, get_current_user
from models import CartItem
from schemas import UserResponse

router = APIRouter()
templates = Jinja2Templates(directory="../app/templates")

@router.get("/mycart", response_class=HTMLResponse)
async def get_my_cart(request: Request, 
                      db: AsyncSession = Depends(get_db),
                      user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(CartItem).where(CartItem.user_id == user.id))
    cart_items = result.scalars().all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items})