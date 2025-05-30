from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Schema cơ bản cho Category
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

# Schema cho thông tin Category trả về
class CategoryResponse(CategoryBase):
    category_id: int
    children: List["CategoryResponse"] = []

    class Config:
        orm_mode = True

# Giải quyết circular reference
CategoryResponse.update_forward_refs()

# Schema cơ bản cho Category dạng cây
class CategoryTree(BaseModel):
    id: int
    name: str
    children: List["CategoryTree"] = []

# Schema cho thông tin ProductImage trả về
class ProductImageResponse(BaseModel):
    image_id: int
    product_id: int
    image_url: str
    is_primary: bool
    display_order: int

    class Config:
        orm_mode = True

# Schema cho thông tin Tag trả về
class TagResponse(BaseModel):
    tag_id: int
    name: str

    class Config:
        orm_mode = True

# Schema cơ bản cho Product
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    stock_quantity: int
    attributes: Optional[Dict[str, Any]] = None
    is_active: bool = True

# Schema cho thông tin Product trả về trong danh sách
class ProductListItem(BaseModel):
    product_id: int
    name: str
    price: float
    category_id: int
    category_name: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

# Schema cho kết quả tìm kiếm sản phẩm
class ProductSearchResult(BaseModel):
    items: List[ProductListItem]
    pagination: Dict[str, Any]
    filters: Dict[str, Any]

# Schema cho thông tin Product đầy đủ trả về
class ProductResponse(ProductBase):
    product_id: int
    category_name: Optional[str] = None
    images: List[ProductImageResponse] = []
    tags: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schema cho việc tạo Product mới
class ProductCreate(ProductBase):
    pass

# Schema cho việc cập nhật Product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    stock_quantity: Optional[int] = None
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True