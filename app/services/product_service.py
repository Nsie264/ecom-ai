from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.repositories.product_repository import (
    ProductRepository, CategoryRepository, ProductImageRepository, TagRepository
)
from app.repositories.interaction_repository import ViewHistoryRepository
from app.models.product import Product, Category, ProductImage

class ProductService:
    """Service xử lý logic nghiệp vụ liên quan đến sản phẩm"""
    
    def __init__(self, db: Session):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)
        self.image_repo = ProductImageRepository(db)
        self.tag_repo = TagRepository(db)
        self.view_history_repo = ViewHistoryRepository(db)
    
    def get_product_by_id(self, product_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin chi tiết sản phẩm và ghi lại lượt xem nếu có user_id
        
        Parameters:
        -----------
        product_id : int
            ID của sản phẩm cần lấy
        user_id : int, optional
            ID của người dùng đang xem sản phẩm (nếu đã đăng nhập)
            
        Returns:
        --------
        Optional[Dict[str, Any]]
            Thông tin chi tiết sản phẩm
        """
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            return None
        
        # Ghi lại lượt xem nếu người dùng đã đăng nhập
        if user_id:
            self.view_history_repo.add_view(user_id, product_id)
        
        # Lấy ảnh sản phẩm
        images = self.image_repo.get_by_product_id(product_id)
        
        # Lấy tags sản phẩm
        tags = self.tag_repo.get_by_product_id(product_id)
        
        # Tạo đối tượng kết quả
        result = {
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "category_name": product.category.name if product.category else None,
            "stock_quantity": product.stock_quantity,
            "attributes": product.attributes,
            "is_active": product.is_active,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "images": [
                {
                    "image_id": img.image_id,
                    "product_id": product.product_id,
                    "image_url": img.image_url,
                    "is_primary": getattr(img, 'is_primary', False),
                    "display_order": getattr(img, 'display_order', 0)
                } for img in images
            ],
            "tags": [tag.name for tag in tags]
        }
        
        return result
    
    def search_products(
        self,
        search_query: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        order_by: str = "created_at",
        descending: bool = True,
        page: int = 1,
        page_size: int = 20,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Tìm kiếm sản phẩm với các bộ lọc khác nhau
        
        Parameters:
        -----------
        search_query : str, optional
            Từ khóa tìm kiếm
        category_id : int, optional
            ID danh mục cần lọc
        min_price, max_price : float, optional
            Khoảng giá cần lọc
        order_by : str
            Trường để sắp xếp (price, name, created_at)
        descending : bool
            Sắp xếp giảm dần hay không
        page, page_size : int
            Tham số phân trang
        user_id : int, optional
            ID người dùng (để ghi lại lịch sử tìm kiếm)
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả tìm kiếm với phân trang
        """
        # Tính toán offset cho phân trang
        skip = (page - 1) * page_size
        
        # Lấy danh sách sản phẩm thỏa mãn điều kiện lọc
        products = self.product_repo.get_multi(
            skip=skip,
            limit=page_size,
            category_id=category_id,
            search_query=search_query,
            min_price=min_price,
            max_price=max_price,
            order_by=order_by,
            descending=descending
        )
        
        # Đếm tổng số sản phẩm thỏa mãn điều kiện (không tính phân trang)
        total_count = self.product_repo.get_count(
            category_id=category_id,
            search_query=search_query,
            min_price=min_price,
            max_price=max_price
        )
        
        # Tính tổng số trang
        total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 0
        
        # Ghi lại lịch sử tìm kiếm nếu có user_id và search_query
        if user_id and search_query:
            from app.repositories.interaction_repository import SearchHistoryRepository
            search_repo = SearchHistoryRepository(self.db)
            search_repo.add_search(user_id, search_query)
        
        # Format kết quả
        result = {
            "items": [
                {
                    "product_id": p.product_id,
                    "name": p.name,
                    "price": p.price,
                    "category_id": p.category_id,
                    "category_name": p.category.name if p.category else None,
                    "image_url": next((img.image_url for img in p.images if img.is_primary), 
                                    (p.images[0].image_url if p.images else None))
                } for p in products
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages
            },
            "filters": {
                "search_query": search_query,
                "category_id": category_id,
                "min_price": min_price,
                "max_price": max_price,
                "order_by": order_by,
                "descending": descending
            }
        }
        
        return result
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả danh mục sản phẩm theo cấu trúc phẳng
        
        Returns:
        --------
        List[Dict[str, Any]]
            Danh sách danh mục dạng phẳng
        """
        # Lấy tất cả danh mục
        categories = self.category_repo.get_all()
        
        # Chuyển đổi thành danh sách phẳng
        result = [
            {
                "id": category.category_id,
                "name": category.name,
                "description": category.description
            }
            for category in categories
        ]
        
        return result