from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.db.init_db import create_first_admin

# Tạo ứng dụng FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API hệ thống eCommerce AI với chức năng gợi ý sản phẩm",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký API router
app.include_router(api_router)

# Sự kiện khởi động
@app.on_event("startup")
async def startup_event():
    # Tạo tài khoản admin đầu tiên nếu cần
    create_first_admin()

@app.get("/")
async def root():
    """
    Endpoint kiểm tra API hoạt động
    """
    return {
        "message": "Chào mừng đến với API hệ thống eCommerce AI",
        "documentation": "/api/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)