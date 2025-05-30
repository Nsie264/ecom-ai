from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Index, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base

class ProductSimilarity(Base):
    __tablename__ = "product_similarity"
    
    # Composite primary key từ 2 sản phẩm
    product_id_a = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    product_id_b = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    
    # Độ tương tự giữa 2 sản phẩm (0-1)
    similarity_score = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product_a = relationship("Product", foreign_keys=[product_id_a], back_populates="similar_products")
    product_b = relationship("Product", foreign_keys=[product_id_b], back_populates="similarity_references")
    
    # Thêm index để tìm kiếm nhanh các sản phẩm tương tự
    __table_args__ = (
        Index('idx_product_similarity_a_score', product_id_a, similarity_score.desc()),
    )

class UserRecommendation(Base):
    __tablename__ = "user_recommendations"
    
    # Composite primary key từ user và product
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    
    # Điểm gợi ý (càng cao càng phù hợp)
    recommendation_score = Column(Float, nullable=False)
    # Thứ tự hiển thị trong danh sách gợi ý (thấp hơn hiển thị trước)
    rank = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    product = relationship("Product", back_populates="user_recommendations")
    
    # Thêm index để lấy nhanh các gợi ý xếp hạng cao nhất
    __table_args__ = (
        Index('idx_user_recommendation_user_rank', user_id, rank),
    )

class TrainingHistory(Base):
    __tablename__ = "training_history"
    
    history_id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)  # RUNNING, SUCCESS, FAILED
    triggered_by = Column(String(50), nullable=False)  # SCHEDULED hoặc MANUAL_ADMIN_ID
    message = Column(Text, nullable=True)  # Thông báo lỗi nếu có
    
    __table_args__ = (
        Index('idx_training_history_status', status),
        Index('idx_training_history_start_time', start_time.desc()),
    )