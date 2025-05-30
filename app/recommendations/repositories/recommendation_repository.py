from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.repositories import BaseRepository
from app.models.recommendation import ProductSimilarity, UserRecommendation
from app.models.user import User

class ProductSimilarityRepository(BaseRepository[ProductSimilarity]):
    def __init__(self, db: Session):
        super().__init__(db, ProductSimilarity)
    
    def get_similar_products(self, product_id: int, limit: int = 10) -> List[Tuple[int, float]]:
        """Lấy danh sách ID sản phẩm tương tự nhất với sản phẩm đang xem"""
        results = self.db.query(
            ProductSimilarity.product_id_b, 
            ProductSimilarity.similarity_score
        ).filter(
            ProductSimilarity.product_id_a == product_id
        ).order_by(
            desc(ProductSimilarity.similarity_score)
        ).limit(limit).all()
        
        return [(r.product_id_b, r.similarity_score) for r in results]
    
    def batch_upsert(self, similarity_data: List[Dict[str, Any]]) -> None:
        """Cập nhật hoặc chèn hàng loạt dữ liệu về độ tương tự sản phẩm"""
        # Xóa các bản ghi hiện có trước khi chèn mới
        # Lưu ý: Trong môi trường production, có thể cần chiến lược phức tạp hơn
        self.db.query(ProductSimilarity).delete()
        
        # Tạo và chèn các bản ghi mới
        similarities = [ProductSimilarity(**data) for data in similarity_data]
        self.db.add_all(similarities)
        self.db.commit()
        
    def delete_all(self) -> None:
        """Xóa tất cả dữ liệu về độ tương tự sản phẩm"""
        self.db.query(ProductSimilarity).delete()
        self.db.commit()

class UserRecommendationRepository(BaseRepository[UserRecommendation]):
    def __init__(self, db: Session):
        super().__init__(db, UserRecommendation)
    
    def get_recommendations_for_user(self, user: User, limit: int = 20) -> List[Tuple[int, float]]:
        """
        Lấy danh sách ID sản phẩm được gợi ý cho người dùng
        
        Parameters:
        -----------
        user : User
            Đối tượng User cần lấy gợi ý
        limit : int
            Số lượng gợi ý tối đa cần trả về
        
        Returns:
        --------
        List[Tuple[int, float]]
            Danh sách các cặp (product_id, score) được gợi ý
        """
        results = self.db.query(
            UserRecommendation.product_id, 
            UserRecommendation.recommendation_score
        ).filter(
            UserRecommendation.user_id == user.user_id
        ).order_by(
            UserRecommendation.rank
        ).limit(limit).all()
        
        return [(r.product_id, r.recommendation_score) for r in results]
    
    def batch_upsert(self, recommendation_data: List[Dict[str, Any]]) -> None:
        """Cập nhật hoặc chèn hàng loạt dữ liệu gợi ý sản phẩm cho người dùng"""
        # Xóa tất cả gợi ý hiện có trước khi chèn mới
        # Lưu ý: Trong môi trường production, có thể cần chiến lược phức tạp hơn
        self.db.query(UserRecommendation).delete()
        
        # Tạo và chèn các bản ghi mới
        recommendations = [UserRecommendation(**data) for data in recommendation_data]
        self.db.add_all(recommendations)
        self.db.commit()
    
    def delete_for_user(self, user_id: int) -> None:
        """Xóa tất cả gợi ý cho một người dùng cụ thể"""
        self.db.query(UserRecommendation).filter(UserRecommendation.user_id == user_id).delete()
        self.db.commit()
    
    def delete_all(self) -> None:
        """Xóa tất cả dữ liệu gợi ý"""
        self.db.query(UserRecommendation).delete()
        self.db.commit()