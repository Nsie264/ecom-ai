from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import logging
import pandas as pd
from sqlalchemy.orm import Session

from app.repositories.interaction_repository import ViewHistoryRepository, RatingRepository
from app.repositories.order_repository import OrderItemRepository

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Lớp chịu trách nhiệm tải dữ liệu tương tác người dùng từ cơ sở dữ liệu
    để huấn luyện mô hình gợi ý.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.view_history_repo = ViewHistoryRepository(db)
        self.rating_repo = RatingRepository(db)
        self.order_item_repo = OrderItemRepository(db)
    
    def get_interaction_data(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """
        Tải dữ liệu tương tác (xem, đánh giá, mua hàng) từ cơ sở dữ liệu
        và trả về dưới dạng các DataFrame Pandas.
        
        Parameters:
        -----------
        start_date : datetime, optional
            Thời điểm bắt đầu khoảng thời gian cần lấy dữ liệu
        end_date : datetime, optional
            Thời điểm kết thúc khoảng thời gian cần lấy dữ liệu
            
        Returns:
        --------
        Dict[str, pd.DataFrame]
            Dictionary chứa các DataFrame: 'ratings', 'views', 'purchases'
        """
        # Mặc định lấy dữ liệu trong 6 tháng gần nhất
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=180)
        
        logger.info(f"Tải dữ liệu tương tác từ {start_date} đến {end_date}")
        
        # Tải dữ liệu đánh giá
        ratings_data = self.rating_repo.get_by_date_range(start_date, end_date)
        ratings_df = pd.DataFrame([
            {
                'user_id': r.user_id,
                'product_id': r.product_id,
                'rating': r.score,
                'timestamp': r.created_at.timestamp()
            } for r in ratings_data
        ])
        logger.info(f"Đã tải {len(ratings_df)} đánh giá")
        
        # Tải dữ liệu lịch sử xem
        views_data = self.view_history_repo.get_recent_views_by_date_range(start_date, end_date)
        views_df = pd.DataFrame([
            {
                'user_id': v.user_id,
                'product_id': v.product_id,
                'timestamp': v.view_timestamp.timestamp()
            } for v in views_data
        ])
        logger.info(f"Đã tải {len(views_df)} lượt xem")
        
        # Tải dữ liệu mua hàng từ các item trong đơn hàng

        from sqlalchemy import text
        
        query = text("""
            SELECT o.user_id, oi.product_id, oi.quantity, o.order_date
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.order_date BETWEEN :start_date AND :end_date
            AND o.status != 'CANCELLED'
        """)
        
        result = self.db.execute(query, {"start_date": start_date, "end_date": end_date})
        purchases_data = result.fetchall()
        
        purchases_df = pd.DataFrame([
            {
                'user_id': p.user_id,
                'product_id': p.product_id,
                'quantity': p.quantity,
                'timestamp': p.order_date.timestamp()
            } for p in purchases_data
        ])
        logger.info(f"Đã tải {len(purchases_df)} lượt mua hàng")
        
        return {
            'ratings': ratings_df,
            'views': views_df,
            'purchases': purchases_df
        }
    
    def get_product_data(self) -> pd.DataFrame:
        """
        Tải thông tin sản phẩm (có thể dùng cho content-based filtering)
        
        Returns:
        --------
        pd.DataFrame
            DataFrame chứa thông tin sản phẩm
        """
        # Truy vấn SQL trực tiếp để lấy dữ liệu sản phẩm và danh mục
        from sqlalchemy import text
        
        query = text("""
            SELECT p.product_id, p.name, p.price, p.attributes, 
                   c.name as category_name, c.category_id
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.is_active = TRUE
        """)
        
        result = self.db.execute(query)
        products_data = result.fetchall()
        
        products_df = pd.DataFrame([
            {
                'product_id': p.product_id,
                'name': p.name,
                'price': p.price,
                'attributes': p.attributes,  # JSON
                'category_id': p.category_id,
                'category_name': p.category_name
            } for p in products_data
        ])
        
        logger.info(f"Đã tải {len(products_df)} sản phẩm")
        return products_df