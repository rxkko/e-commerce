from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routes.user import auth_route as auth
from routes.user import user_crud_route as user
from routes.products import product_route as products, cart_route as cart

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(products.router, tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
