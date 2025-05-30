from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_

from app.repositories import BaseRepository
from app.models.product import Product, Category, ProductImage, Tag

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(db, Product)
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.product_id == product_id).first()
    
    def get_multi(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 20,
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        order_by: str = "created_at",
        descending: bool = True
    ) -> List[Product]:
        """Lấy danh sách sản phẩm với các bộ lọc"""
        query = self.db.query(Product).filter(Product.is_active == True)
        
        # Áp dụng các bộ lọc
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        
        if search_query:
            search_filter = f"%{search_query}%"
            query = query.filter(Product.name.ilike(search_filter))
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Sắp xếp
        if order_by == "price":
            order_column = Product.price
        elif order_by == "name":
            order_column = Product.name
        else:  # default: created_at
            order_column = Product.created_at
        
        if descending:
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(order_column)
        
        # Phân trang
        return query.offset(skip).limit(limit).all()
    
    def get_multi_mananger(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        order_by: str = "created_at",
        descending: bool = True
    ) -> List[Product]:
        """Lấy danh sách sản phẩm với các bộ lọc"""
        query = self.db.query(Product)
        
        # Áp dụng các bộ lọc
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        
        if search_query:
            search_filter = f"%{search_query}%"
            query = query.filter(Product.name.ilike(search_filter))
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Sắp xếp
        if order_by == "price":
            order_column = Product.price
        elif order_by == "name":
            order_column = Product.name
        else:  # default: created_at
            order_column = Product.created_at
        
        if descending:
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(order_column)
        
        # Phân trang
        return query.offset(skip).limit(limit).all()
    
    def get_count(
        self,
        *,
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> int:
        """Đếm tổng số sản phẩm thỏa mãn điều kiện lọc"""
        query = self.db.query(func.count(Product.product_id)).filter(Product.is_active == True)
        
        # Áp dụng các bộ lọc
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        
        if search_query:
            search_filter = f"%{search_query}%"
            query = query.filter(Product.name.ilike(search_filter))
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        return query.scalar()
    
    def get_count_mananger(
        self,
        *,
        category_id: Optional[int] = None,
        search_query: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> int:
        """Đếm tổng số sản phẩm thỏa mãn điều kiện lọc"""
        query = self.db.query(func.count(Product.product_id))
        
        # Áp dụng các bộ lọc
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        
        if search_query:
            search_filter = f"%{search_query}%"
            query = query.filter(Product.name.ilike(search_filter))
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        return query.scalar()
    
    def check_and_lock_stock(self, product_id: int, quantity: int) -> bool:
        """Kiểm tra và khóa tạm thời số lượng sản phẩm để tránh race condition"""
        product = self.db.query(Product).filter(
            Product.product_id == product_id,
            Product.is_active == True
        ).with_for_update().first()
        
        if not product or product.stock_quantity < quantity:
            return False
        
        return True
    
    def decrease_stock(self, product_id: int, quantity: int) -> bool:
        """Giảm số lượng tồn kho sau khi đặt hàng"""
        product = self.db.query(Product).filter(Product.product_id == product_id).with_for_update().first()
        if not product or product.stock_quantity < quantity:
            return False
        
        product.stock_quantity -= quantity
        self.db.add(product)
        # Không commit ở đây vì sẽ commit trong transaction của đặt hàng
        return True
    
    def get_by_ids(self, product_ids: List[int]) -> List[Product]:
        """Lấy nhiều sản phẩm theo danh sách ID"""
        if not product_ids:
            return []
        return self.db.query(Product).filter(
            Product.product_id.in_(product_ids),
            Product.is_active == True
        ).all()
    
    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """Tạo sản phẩm mới"""
        # Đảm bảo category_id tồn tại nếu được cung cấp
        if "category_id" in product_data:
            category = self.db.query(Category).filter(Category.category_id == product_data["category_id"]).first()
            if not category:
                raise ValueError(f"Category with id {product_data['category_id']} not found")
        
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Optional[Product]:
        """Cập nhật thông tin sản phẩm"""
        product = self.get_by_id(product_id)
        if product:
            # Đảm bảo category_id tồn tại nếu được cung cấp và thay đổi
            if "category_id" in product_data and product_data["category_id"] != product.category_id:
                category = self.db.query(Category).filter(Category.category_id == product_data["category_id"]).first()
                if not category:
                    raise ValueError(f"Category with id {product_data['category_id']} not found")

            for key, value in product_data.items():
                setattr(product, key, value)
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> Optional[Product]:
        """Xóa mềm sản phẩm bằng cách đặt is_active = False"""
        product = self.get_by_id(product_id)
        if product:
            product.is_active = False
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
        return product

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.category_id == category_id).first()
    
    def get_all(self) -> List[Category]:
        """Lấy tất cả danh mục"""
        return self.db.query(Category).all()
    
    def get_root_categories(self) -> List[Category]:
        """Lấy danh sách danh mục gốc (không có parent)"""
        return self.db.query(Category).filter(Category.parent_id == None).all()
    
    def get_subcategories(self, parent_id: int) -> List[Category]:
        """Lấy danh sách danh mục con của một danh mục cha"""
        return self.db.query(Category).filter(Category.parent_id == parent_id).all()

class ProductImageRepository(BaseRepository[ProductImage]):
    def __init__(self, db: Session):
        super().__init__(db, ProductImage)
    
    def get_by_product_id(self, product_id: int) -> List[ProductImage]:
        """Lấy tất cả hình ảnh của một sản phẩm, sắp xếp theo thứ tự hiển thị"""
        return self.db.query(ProductImage).filter(
            ProductImage.product_id == product_id
        ).order_by(ProductImage.display_order, ProductImage.is_primary.desc()).all()
    
    def get_primary_image(self, product_id: int) -> Optional[ProductImage]:
        """Lấy hình ảnh chính của sản phẩm"""
        return self.db.query(ProductImage).filter(
            ProductImage.product_id == product_id,
            ProductImage.is_primary == True
        ).first()

class TagRepository(BaseRepository[Tag]):
    def __init__(self, db: Session):
        super().__init__(db, Tag)
    
    def get_by_name(self, name: str) -> Optional[Tag]:
        """Lấy tag theo tên"""
        return self.db.query(Tag).filter(Tag.name == name).first()
    
    def get_or_create(self, name: str) -> Tag:
        """Lấy tag nếu tồn tại, nếu không tạo mới"""
        tag = self.get_by_name(name)
        if not tag:
            tag = Tag(name=name)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
        return tag
    
    def get_by_product_id(self, product_id: int) -> List[Tag]:
        """Lấy tất cả tag của một sản phẩm"""
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            return product.tags
        return []
    
