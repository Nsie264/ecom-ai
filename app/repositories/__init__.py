from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional, Any, Dict, Union

from app.db.base import Base

# Định nghĩa kiểu generic cho các Model
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Repository cơ sở cung cấp các thao tác CRUD cơ bản.
    Các repository cụ thể sẽ kế thừa từ lớp này.
    """
    
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    def get(self, id: Any) -> Optional[ModelType]:
        """Lấy một bản ghi theo ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Lấy nhiều bản ghi với phân trang."""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, *, obj_in: Dict[str, Any]) -> ModelType:
        """Tạo mới một bản ghi."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, *, db_obj: ModelType, obj_in: Union[Dict[str, Any], ModelType]) -> ModelType:
        """Cập nhật một bản ghi."""
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.__dict__
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def remove(self, *, id: int) -> ModelType:
        """Xóa một bản ghi."""
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj