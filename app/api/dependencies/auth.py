from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.dependencies.db import get_db
from app.repositories.user_repository import UserRepository
from app.core.config import settings

# Định nghĩa oauth2_scheme để sử dụng trong các route cần xác thực
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Tạo JWT token
    
    Parameters:
    -----------
    data : dict
        Dữ liệu cần mã hóa vào token (thường là user_id)
    expires_delta : timedelta, optional
        Thời gian token hết hạn
    
    Returns:
    --------
    str
        JWT token đã mã hóa
    """
    to_encode = data.copy()
    
    # Thiết lập thời gian hết hạn
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Tạo JWT token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Lấy thông tin người dùng hiện tại từ token.
    Sử dụng làm dependency trong các API endpoint cần xác thực.
    
    Parameters:
    -----------
    token : str
        JWT token được trích xuất từ header Authorization
    db : Session
        Database session
    
    Returns:
    --------
    User
        Đối tượng User
    
    Raises:
    -------
    HTTPException
        Nếu token không hợp lệ hoặc người dùng không tồn tại
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin người dùng",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Giải mã token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Lấy thông tin người dùng từ database
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user