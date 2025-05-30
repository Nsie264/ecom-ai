from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories import BaseRepository
from app.models.user import User, UserAddress

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.user_id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def create_user(self, user_data: dict) -> User:
        """Tạo người dùng mới"""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Cập nhật thông tin người dùng"""
        user = self.get_by_id(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Xóa người dùng"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

class UserAddressRepository(BaseRepository[UserAddress]):
    def __init__(self, db: Session):
        super().__init__(db, UserAddress)
    
    def get_by_id(self, address_id: int) -> Optional[UserAddress]:
        return self.db.query(UserAddress).filter(UserAddress.address_id == address_id).first()
    
    def get_by_user_id(self, user_id: int) -> List[UserAddress]:
        return self.db.query(UserAddress).filter(UserAddress.user_id == user_id).all()
    
    def get_default_address(self, user_id: int) -> Optional[UserAddress]:
        return self.db.query(UserAddress).filter(
            UserAddress.user_id == user_id,
            UserAddress.is_default == True
        ).first()
    
    def create_address(self, address_data: dict) -> UserAddress:
        """Tạo địa chỉ mới"""
        # Nếu đây là địa chỉ mặc định, đặt tất cả các địa chỉ khác thành không mặc định
        if address_data.get("is_default", False):
            self.db.query(UserAddress).filter(
                UserAddress.user_id == address_data["user_id"],
                UserAddress.is_default == True
            ).update({"is_default": False})
        
        address = UserAddress(**address_data)
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address
    
    def update_address(self, address_id: int, address_data: dict) -> Optional[UserAddress]:
        """Cập nhật địa chỉ"""
        address = self.get_by_id(address_id)
        if address:
            # Nếu đây là địa chỉ mặc định, đặt tất cả các địa chỉ khác thành không mặc định
            if address_data.get("is_default", False):
                self.db.query(UserAddress).filter(
                    UserAddress.user_id == address.user_id,
                    UserAddress.address_id != address_id,
                    UserAddress.is_default == True
                ).update({"is_default": False})
            
            for key, value in address_data.items():
                setattr(address, key, value)
            
            self.db.add(address)
            self.db.commit()
            self.db.refresh(address)
        return address
    
    def delete_address(self, address_id: int) -> bool:
        """Xóa địa chỉ"""
        address = self.get_by_id(address_id)
        if address:
            self.db.delete(address)
            self.db.commit()
            return True
        return False