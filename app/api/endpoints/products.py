from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.api.dependencies.db import get_db
from app.api.dependencies.auth import get_current_user
from app.api.schemas.product import ProductListItem, ProductSearchResult, ProductResponse
from app.services.product_service import ProductService
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=ProductSearchResult)
async def search_products(
    search_query: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    order_by: str = "created_at",
    descending: bool = True,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Tìm kiếm sản phẩm với nhiều bộ lọc khác nhau.
    """
    product_service = ProductService(db)
    user_id = current_user.user_id if current_user else None
    
    result = product_service.search_products(
        search_query=search_query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        order_by=order_by,
        descending=descending,
        page=page,
        page_size=page_size,
        user_id=user_id
    )
    
    return result

@router.get("/{product_id}")  # Removed response_model=ProductResponse temporarily
async def get_product_by_id(
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Lấy thông tin chi tiết của một sản phẩm.
    """
    product_service = ProductService(db)
    user_id = current_user.user_id if current_user else None
    
    product = product_service.get_product_by_id(product_id, user_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sản phẩm không tồn tại hoặc không khả dụng"
        )
    
    return product

@router.get("/categories/tree")
async def get_categories(db: Session = Depends(get_db)):
    """
    Lấy danh sách danh mục theo cấu trúc cây.
    """
    product_service = ProductService(db)
    return product_service.get_categories()