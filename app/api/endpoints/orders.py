from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.db import get_db
from app.api.dependencies.auth import get_current_user
from app.api.schemas.order import (
    OrderListResponse, OrderDetailResponse, CreateOrderRequest, 
    CreateOrderResponse, CancelOrderResponse
)
from app.services.order_service import OrderService
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=OrderListResponse)
async def get_user_orders(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách đơn hàng của người dùng hiện tại.
    """
    order_service = OrderService(db)
    orders = order_service.get_orders_by_user(
        user_id=current_user.user_id,
        page=page,
        page_size=page_size
    )
    return orders

@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order_details(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy chi tiết một đơn hàng cụ thể.
    """
    order_service = OrderService(db)
    order_details = order_service.get_order_details(
        order_id=order_id,
        user_id=current_user.user_id
    )
    
    if not order_details["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=order_details["message"]
        )
    
    return order_details

@router.post("/", response_model=CreateOrderResponse)
async def place_order(
    order_data: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Đặt đơn hàng mới từ giỏ hàng hiện tại.
    """
    order_service = OrderService(db)
    result = order_service.place_order(
        user_id=current_user.user_id,
        address_id=order_data.address_id,
        notes=order_data.notes
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result

@router.post("/{order_id}/cancel", response_model=CancelOrderResponse)
async def cancel_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Hủy đơn hàng nếu đơn hàng vẫn ở trạng thái PENDING.
    """
    order_service = OrderService(db)
    result = order_service.cancel_order(
        order_id=order_id,
        user_id=current_user.user_id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result