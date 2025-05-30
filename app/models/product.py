from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, JSON, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

# Bảng trung gian cho mối quan hệ nhiều-nhiều giữa Product và Tag
product_tag = Table(
    'product_tag',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.product_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'), primary_key=True)
)

class Category(Base):
    __tablename__ = "categories"
    
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Products
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    stock_quantity = Column(Integer, default=0)
    attributes = Column(JSON)  # Lưu thông tin như kích thước, màu sắc, v.v. dưới dạng JSON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    view_history = relationship("ViewHistory", back_populates="product")
    ratings = relationship("Rating", back_populates="product")
    
    # Many-to-many relationship with tags
    tags = relationship("Tag", secondary=product_tag, back_populates="products")
    
    # Các mối quan hệ với sản phẩm tương tự (product_similarity)
    # Lưu ý: product_id_a là sản phẩm này, product_id_b là sản phẩm tương tự
    similar_products = relationship(
        "ProductSimilarity",
        foreign_keys="ProductSimilarity.product_id_a",
        back_populates="product_a"
    )
    
    # Lưu ý: product_id_b là sản phẩm này, product_id_a là sản phẩm tương tự
    similarity_references = relationship(
        "ProductSimilarity",
        foreign_keys="ProductSimilarity.product_id_b",
        back_populates="product_b"
    )
    
    # Relationship với UserRecommendation
    user_recommendations = relationship("UserRecommendation", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"
    
    image_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)  # Thứ tự hiển thị trong gallery
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="images")

class Tag(Base):
    __tablename__ = "tags"
    
    tag_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with products
    products = relationship("Product", secondary=product_tag, back_populates="tags")