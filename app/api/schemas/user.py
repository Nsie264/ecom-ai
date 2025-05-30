from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Schema cho token trả về sau khi đăng nhập
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema cho dữ liệu token
class TokenData(BaseModel):
    user_id: Optional[int] = None

# Schema cơ bản cho User
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Schema cho việc tạo User
class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str

# Schema cho việc cập nhật User
class UserUpdate(UserBase):
    password: Optional[str] = None

# Schema cho thông tin User trả về
class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Schema cho thông tin đăng nhập
class Login(BaseModel):
    email: EmailStr
    password: str

# Schema cơ bản cho địa chỉ
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    phone: str
    is_default: bool = False

# Schema cho việc tạo địa chỉ mới
class AddressCreate(AddressBase):
    pass

# Schema cho việc cập nhật địa chỉ
class AddressUpdate(AddressBase):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    is_default: Optional[bool] = None

# Schema cho thông tin địa chỉ trả về
class AddressResponse(AddressBase):
    address_id: int
    user_id: int
    
    class Config:
        orm_mode = True