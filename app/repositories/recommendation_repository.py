from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional

from app.models.recommendation import ProductSimilarity, UserRecommendation

class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    # Phương thức cho ProductSimilarity
    def get_similar_products(self, product_id: int, limit: int = 10) -> List[ProductSimilarity]:
        """Lấy danh sách các sản phẩm tương tự với sản phẩm có ID được chỉ định"""
        return self.db.query(ProductSimilarity).filter(
            ProductSimilarity.product_id_a == product_id
        ).order_by(desc(ProductSimilarity.similarity_score)).limit(limit).all()
    
    def save_product_similarity(self, product_id_a: int, product_id_b: int, 
                                similarity_score: float) -> ProductSimilarity:
        """Lưu hoặc cập nhật độ tương tự giữa hai sản phẩm"""
        # Kiểm tra xem bản ghi đã tồn tại chưa
        similarity = self.db.query(ProductSimilarity).filter(
            ProductSimilarity.product_id_a == product_id_a,
            ProductSimilarity.product_id_b == product_id_b
        ).first()
        
        if similarity:
            # Cập nhật nếu đã tồn tại
            similarity.similarity_score = similarity_score
        else:
            # Tạo mới nếu chưa tồn tại
            similarity = ProductSimilarity(
                product_id_a=product_id_a,
                product_id_b=product_id_b,
                similarity_score=similarity_score
            )
            self.db.add(similarity)
        
        self.db.commit()
        self.db.refresh(similarity)
        return similarity
    
    def delete_all_product_similarities(self) -> None:
        """Xóa tất cả các bản ghi về độ tương tự giữa các sản phẩm"""
        self.db.query(ProductSimilarity).delete()
        self.db.commit()
    
    # Phương thức cho UserRecommendation
    def get_user_recommendations(self, user_id: int, limit: int = 10) -> List[UserRecommendation]:
        """Lấy danh sách sản phẩm được gợi ý cho người dùng có ID được chỉ định"""
        return self.db.query(UserRecommendation).filter(
            UserRecommendation.user_id == user_id
        ).order_by(UserRecommendation.rank).limit(limit).all()
    
    def save_user_recommendation(self, user_id: int, product_id: int, 
                                recommendation_score: float, rank: int) -> UserRecommendation:
        """Lưu hoặc cập nhật gợi ý sản phẩm cho người dùng"""
        # Kiểm tra xem bản ghi đã tồn tại chưa
        recommendation = self.db.query(UserRecommendation).filter(
            UserRecommendation.user_id == user_id,
            UserRecommendation.product_id == product_id
        ).first()
        
        if recommendation:
            # Cập nhật nếu đã tồn tại
            recommendation.recommendation_score = recommendation_score
            recommendation.rank = rank
        else:
            # Tạo mới nếu chưa tồn tại
            recommendation = UserRecommendation(
                user_id=user_id,
                product_id=product_id,
                recommendation_score=recommendation_score,
                rank=rank
            )
            self.db.add(recommendation)
        
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation
    
    def delete_user_recommendations(self, user_id: Optional[int] = None) -> None:
        """
        Xóa tất cả gợi ý của một người dùng cụ thể nếu user_id được cung cấp,
        hoặc xóa tất cả gợi ý của tất cả người dùng nếu user_id không được cung cấp
        """
        query = self.db.query(UserRecommendation)
        if user_id:
            query = query.filter(UserRecommendation.user_id == user_id)
        
        query.delete()
        self.db.commit()