from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from deps import get_db
from schemas import ProductResponse
from services.product import get_all_products, get_product_by_id, get_all_categories

router = APIRouter()
templates = Jinja2Templates(directory="../app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_all_products_view(
    request: Request,
    db: AsyncSession = Depends(get_db),
    category_id: int = Query(None)
):
    categories = await get_all_categories(db)
    products = await get_all_products(db, category_id)
    
    return templates.TemplateResponse("main.html", {
        "request": request,
        "products": products,
        "categories": categories,
        "selected_category": category_id
    })

@router.get("/product/{product_id}", response_model=ProductResponse)
async def get_product_by_id_view(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product