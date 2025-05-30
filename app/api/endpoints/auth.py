from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api.dependencies.db import get_db
from app.api.dependencies.auth import create_access_token, get_current_user
from app.api.schemas.user import (
    Token, UserCreate, UserResponse, UserUpdate, 
    AddressCreate, AddressResponse, AddressUpdate
)
from app.services.user_service import UserService
from app.core.config import settings
from app.models.user import User

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Đăng nhập và lấy token JWT.
    """
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Tạo access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Đăng ký tài khoản mới.
    """
    user_service = UserService(db)
    
    # Kiểm tra email đã tồn tại chưa
    if user_service.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được sử dụng"
        )
    
    # Tạo user mới
    return user_service.create_user(user_data)

@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user: User = Depends(get_current_user)):
    """
    Lấy thông tin người dùng hiện tại.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_info(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật thông tin người dùng.
    """
    user_service = UserService(db)
    return user_service.update_user(current_user.user_id, user_data)

@router.get("/me/addresses", response_model=list[AddressResponse])
async def get_user_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách địa chỉ của người dùng.
    """
    user_service = UserService(db)
    return user_service.get_user_addresses(current_user.user_id)

@router.post("/me/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def add_user_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Thêm địa chỉ mới cho người dùng.
    """
    user_service = UserService(db)
    return user_service.add_address(current_user.user_id, address_data)

@router.put("/me/addresses/{address_id}", response_model=AddressResponse)
async def update_user_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cập nhật địa chỉ của người dùng.
    """
    user_service = UserService(db)
    return user_service.update_address(current_user.user_id, address_id, address_data)

@router.delete("/me/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Xóa địa chỉ của người dùng.
    """
    user_service = UserService(db)
    result = user_service.delete_address(current_user.user_id, address_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy địa chỉ hoặc bạn không có quyền xóa"
        )