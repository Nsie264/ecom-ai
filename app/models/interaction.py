from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship

from app.db.base import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    
    cart_item_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Tạo index cho việc tìm kiếm nhanh chóng
    __table_args__ = (
        Index('idx_cart_user_product', user_id, product_id, unique=True),
    )
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class ViewHistory(Base):
    __tablename__ = "view_history"
    
    view_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    view_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="view_history")
    product = relationship("Product", back_populates="view_history")

class Rating(Base):
    __tablename__ = "ratings"
    
    rating_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    score = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Tạo index cho việc tìm kiếm nhanh chóng
    __table_args__ = (
        Index('idx_rating_user_product', user_id, product_id, unique=True),
    )
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    search_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    query = Column(String(255), nullable=False)
    search_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="search_history")