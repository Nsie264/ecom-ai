from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.api.dependencies.db import get_db
from app.api.dependencies.auth import get_current_user
from app.api.schemas.cart import (
    CartResponse, AddToCartRequest, UpdateCartItemRequest, CartActionResponse
)
from app.services.cart_service import CartService
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
async def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy thông tin giỏ hàng hiện tại của người dùng.
    """
    cart_service = CartService(db)
    cart = cart_service.get_cart(current_user.user_id)
    return cart

@router.post("/add", response_model=CartActionResponse)
async def add_to_cart(
    item: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Thêm sản phẩm vào giỏ hàng.
    """
    cart_service = CartService(db)
    result = cart_service.add_to_cart(
        user_id=current_user.user_id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    return result

@router.put("/items/{product_id}", response_model=CartActionResponse)
async def update_cart_item(
    product_id: int = Path(..., gt=0),
    item: UpdateCartItemRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật số lượng sản phẩm trong giỏ hàng.
    Số lượng = 0 sẽ xóa sản phẩm khỏi giỏ hàng.
    """
    print(f"[CART_UPDATE_REQUEST] user_id: {current_user.user_id}, product_id: {product_id}, quantity: {item.quantity}")

    cart_service = CartService(db)
    result = cart_service.update_cart_item(
        user_id=current_user.user_id,
        product_id=product_id,
        quantity=item.quantity
    )
    print(f"[CART_UPDATE_RESPONSE] success: {result['success']}, message: {result['message']}")
    return result

@router.delete("/items/{product_id}", response_model=CartActionResponse)
async def remove_from_cart(
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xóa sản phẩm khỏi giỏ hàng.
    """
    cart_service = CartService(db)
    result = cart_service.remove_from_cart(
        user_id=current_user.user_id,
        product_id=product_id
    )
    return result

@router.delete("/", response_model=CartActionResponse)
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xóa toàn bộ giỏ hàng.
    """
    cart_service = CartService(db)
    result = cart_service.clear_cart(current_user.user_id)
    return result