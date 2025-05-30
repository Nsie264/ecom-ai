from fastapi import APIRouter

from app.api.endpoints import products, cart, orders, recommendations, auth

# Tạo một APIRouter chính
api_router = APIRouter(prefix="/api")

# Đăng ký các API routers con
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(products.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
api_router.include_router(recommendations.router)