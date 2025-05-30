from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from app.models.order import OrderStatus, PaymentMethod

# Schema cho thông tin OrderItem trả về
class OrderItemResponse(BaseModel):
    order_item_id: int
    product_id: int
    product_name: str
    quantity: int
    price_at_purchase: float
    subtotal: float
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

# Schema cho thông tin Order trả về trong danh sách
class OrderListItemResponse(BaseModel):
    order_id: int
    order_date: str
    status: str
    total_amount: float
    payment_method: str
    item_count: int
    shipping_address: Dict[str, Any]

    class Config:
        orm_mode = True

# Schema cho danh sách Order trả về
class OrderListResponse(BaseModel):
    items: List[OrderListItemResponse] = []
    pagination: Dict[str, Any]

# Schema cho thông tin Order chi tiết trả về
class OrderDetailResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    order: Optional[Dict[str, Any]] = None  # Chứa thông tin order và items

# Schema cho việc tạo Order mới
class CreateOrderRequest(BaseModel):
    address_id: int
    notes: Optional[str] = None

# Schema cho kết quả của việc tạo Order
class CreateOrderResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[int] = None
    total_amount: Optional[float] = None

# Schema cho việc hủy Order
class CancelOrderResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[int] = None