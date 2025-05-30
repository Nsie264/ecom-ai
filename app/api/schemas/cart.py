from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Schema cho thông tin CartItem trả về
class CartItemResponse(BaseModel):
    cart_item_id: int
    product_id: int
    name: str
    price: float
    quantity: int
    subtotal: float
    image_url: Optional[str] = None
    stock_quantity: int
    is_in_stock: bool

    class Config:
        orm_mode = True

# Schema cho toàn bộ giỏ hàng trả về
class CartResponse(BaseModel):
    items: List[CartItemResponse] = []
    total_amount: float
    item_count: int

# Schema cho việc thêm sản phẩm vào giỏ hàng
class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)  # Số lượng phải lớn hơn 0

# Schema cho việc cập nhật số lượng sản phẩm trong giỏ hàng
class UpdateCartItemRequest(BaseModel):
    quantity: int  # Có thể là 0 để xóa khỏi giỏ hàng

# Schema cho kết quả thao tác giỏ hàng
class CartActionResponse(BaseModel):
    success: bool
    message: str
    cart: Optional[CartResponse] = None