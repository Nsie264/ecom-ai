from typing import List, Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository, UserAddressRepository
from app.models.user import User, UserAddress
from app.api.schemas.user import UserCreate, UserUpdate, AddressCreate, AddressUpdate

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.address_repository = UserAddressRepository(db)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Lấy thông tin người dùng theo email
        """
        return self.user_repository.get_by_email(email)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Lấy thông tin người dùng theo ID
        """
        return self.user_repository.get_by_id(user_id)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Xác thực người dùng với email và password
        """
        user = self.get_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Kiểm tra mật khẩu khớp với hash
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Tạo hash từ mật khẩu
        """
        return pwd_context.hash(password)

    def create_user(self, user_data: UserCreate) -> User:
        """
        Tạo người dùng mới
        """
        # Tạo hash mật khẩu
        hashed_password = self.get_password_hash(user_data.password)
        
        # Chuẩn bị dữ liệu người dùng
        user_dict = user_data.dict(exclude={"password"})
        user_dict["password_hash"] = hashed_password
        
        # Map full_name to name for the database model
        if "full_name" in user_dict:
            user_dict["name"] = user_dict.pop("full_name")
        
        # Tạo người dùng mới
        return self.user_repository.create_user(user_dict)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Cập nhật thông tin người dùng
        """
        user_dict = user_data.dict(exclude_unset=True)
        
        # Nếu có cập nhật mật khẩu, tạo hash mới
        if "password" in user_dict:
            user_dict["password_hash"] = self.get_password_hash(user_dict.pop("password"))
        
        # Map full_name to name for the database model
        if "full_name" in user_dict:
            user_dict["name"] = user_dict.pop("full_name")
        
        return self.user_repository.update_user(user_id, user_dict)

    def get_user_addresses(self, user_id: int) -> List[UserAddress]:
        """
        Lấy danh sách địa chỉ của người dùng
        """
        return self.address_repository.get_by_user_id(user_id)

    def add_address(self, user_id: int, address_data: AddressCreate) -> UserAddress:
        """
        Thêm địa chỉ mới cho người dùng
        """
        address_dict = address_data.dict()
        address_dict["user_id"] = user_id
        
        return self.address_repository.create_address(address_dict)

    def update_address(self, user_id: int, address_id: int, address_data: AddressUpdate) -> Optional[UserAddress]:
        """
        Cập nhật địa chỉ của người dùng
        """
        # Kiểm tra địa chỉ thuộc về người dùng
        address = self.address_repository.get_by_id(address_id)
        if not address or address.user_id != user_id:
            return None
            
        return self.address_repository.update_address(address_id, address_data.dict(exclude_unset=True))

    def delete_address(self, user_id: int, address_id: int) -> bool:
        """
        Xóa địa chỉ của người dùng
        """
        # Kiểm tra địa chỉ thuộc về người dùng
        address = self.address_repository.get_by_id(address_id)
        if not address or address.user_id != user_id:
            return False
            
        return self.address_repository.delete_address(address_id)