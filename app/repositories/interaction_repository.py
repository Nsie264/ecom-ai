from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.repositories import BaseRepository
from app.models.interaction import CartItem, ViewHistory, Rating, SearchHistory

class CartRepository(BaseRepository[CartItem]):
    def __init__(self, db: Session):
        super().__init__(db, CartItem)
    
    def get_by_user_id(self, user_id: int) -> List[CartItem]:
        """Lấy tất cả sản phẩm trong giỏ hàng của người dùng"""
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    def get_by_user_and_product(self, user_id: int, product_id: int) -> Optional[CartItem]:
        """Tìm một sản phẩm cụ thể trong giỏ hàng của người dùng"""
        return self.db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).first()
    
    def add_item(self, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """Thêm sản phẩm vào giỏ hàng (hoặc cập nhật số lượng nếu đã tồn tại)"""
        cart_item = self.get_by_user_and_product(user_id, product_id)
        
        if cart_item:
            cart_item.quantity += quantity
            cart_item.updated_at = datetime.utcnow()
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
        
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item
    
    def update_quantity(self, user_id: int, product_id: int, quantity: int) -> Optional[CartItem]:
        """Cập nhật số lượng sản phẩm trong giỏ hàng"""
        cart_item = self.get_by_user_and_product(user_id, product_id)
        
        if cart_item:
            if quantity <= 0:
                return self.remove_item(user_id, product_id)
            
            cart_item.quantity = quantity
            cart_item.updated_at = datetime.utcnow()
            self.db.add(cart_item)
            self.db.commit()
            self.db.refresh(cart_item)
        
        return cart_item
    
    def remove_item(self, user_id: int, product_id: int) -> bool:
        """Xóa một sản phẩm khỏi giỏ hàng"""
        cart_item = self.get_by_user_and_product(user_id, product_id)
        
        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()
            return True
        return False
    
    def clear_cart(self, user_id: int) -> bool:
        """Xóa toàn bộ giỏ hàng của người dùng"""
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.db.commit()
        return True
    
    def count_items(self, user_id: int) -> int:
        """Đếm số lượng mặt hàng trong giỏ hàng"""
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).count()

class ViewHistoryRepository(BaseRepository[ViewHistory]):
    def __init__(self, db: Session):
        super().__init__(db, ViewHistory)
    
    def get_by_user_id(self, user_id: int, limit: int = 50) -> List[ViewHistory]:
        """Lấy lịch sử xem sản phẩm của người dùng, sắp xếp theo thời gian mới nhất"""
        return self.db.query(ViewHistory).filter(
            ViewHistory.user_id == user_id
        ).order_by(desc(ViewHistory.view_timestamp)).limit(limit).all()
    
    def add_view(self, user_id: int, product_id: int) -> ViewHistory:
        """Thêm một lượt xem mới vào lịch sử"""
        view = ViewHistory(
            user_id=user_id,
            product_id=product_id,
            view_timestamp=datetime.utcnow()
        )
        self.db.add(view)
        self.db.commit()
        self.db.refresh(view)
        return view
    
    def get_product_view_count(self, product_id: int) -> int:
        """Đếm tổng số lượt xem của một sản phẩm"""
        return self.db.query(ViewHistory).filter(ViewHistory.product_id == product_id).count()
    
    def get_recent_views_by_date_range(self, start_date: datetime, end_date: datetime) -> List[ViewHistory]:
        """Lấy lịch sử xem trong một khoảng thời gian (dùng cho huấn luyện mô hình)"""
        return self.db.query(ViewHistory).filter(
            ViewHistory.view_timestamp >= start_date,
            ViewHistory.view_timestamp <= end_date
        ).all()

class RatingRepository(BaseRepository[Rating]):
    def __init__(self, db: Session):
        super().__init__(db, Rating)
    
    def get_by_product_id(self, product_id: int, skip: int = 0, limit: int = 20) -> List[Rating]:
        """Lấy danh sách đánh giá của một sản phẩm"""
        return self.db.query(Rating).filter(
            Rating.product_id == product_id
        ).order_by(desc(Rating.created_at)).offset(skip).limit(limit).all()
    
    def get_by_user_and_product(self, user_id: int, product_id: int) -> Optional[Rating]:
        """Tìm đánh giá của người dùng cho một sản phẩm cụ thể"""
        return self.db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.product_id == product_id
        ).first()
    
    def create_or_update_rating(self, user_id: int, product_id: int, score: int, comment: Optional[str] = None) -> Rating:
        """Tạo đánh giá mới hoặc cập nhật đánh giá hiện có"""
        rating = self.get_by_user_and_product(user_id, product_id)
        
        if rating:
            rating.score = score
            rating.comment = comment
            rating.updated_at = datetime.utcnow()
        else:
            rating = Rating(
                user_id=user_id,
                product_id=product_id,
                score=score,
                comment=comment
            )
        
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating
    
    def get_average_rating(self, product_id: int) -> float:
        """Tính điểm đánh giá trung bình của một sản phẩm"""
        from sqlalchemy import func
        result = self.db.query(func.avg(Rating.score).label('average')).filter(
            Rating.product_id == product_id
        ).scalar()
        return float(result) if result else 0.0
    
    def get_rating_count(self, product_id: int) -> int:
        """Đếm số lượng đánh giá của một sản phẩm"""
        return self.db.query(Rating).filter(Rating.product_id == product_id).count()
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Rating]:
        """Lấy đánh giá trong một khoảng thời gian (dùng cho huấn luyện mô hình)"""
        return self.db.query(Rating).filter(
            Rating.created_at >= start_date,
            Rating.created_at <= end_date
        ).all()

class SearchHistoryRepository(BaseRepository[SearchHistory]):
    def __init__(self, db: Session):
        super().__init__(db, SearchHistory)
    
    def add_search(self, user_id: int, query: str) -> SearchHistory:
        """Thêm một truy vấn tìm kiếm vào lịch sử"""
        search = SearchHistory(
            user_id=user_id,
            query=query,
            search_timestamp=datetime.utcnow()
        )
        self.db.add(search)
        self.db.commit()
        self.db.refresh(search)
        return search
    
    def get_by_user_id(self, user_id: int, limit: int = 10) -> List[SearchHistory]:
        """Lấy lịch sử tìm kiếm của người dùng, sắp xếp theo thời gian mới nhất"""
        return self.db.query(SearchHistory).filter(
            SearchHistory.user_id == user_id
        ).order_by(desc(SearchHistory.search_timestamp)).limit(limit).all()
    
    def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy các từ khóa tìm kiếm phổ biến"""
        from sqlalchemy import func
        results = self.db.query(
            SearchHistory.query, 
            func.count(SearchHistory.query).label('count')
        ).group_by(SearchHistory.query).order_by(desc('count')).limit(limit).all()
        
        return [{"query": r.query, "count": r.count} for r in results]