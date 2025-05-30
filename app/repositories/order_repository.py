from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.repositories import BaseRepository
from app.models.order import Order, OrderItem, OrderStatus

class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: Session):
        super().__init__(db, Order)
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Lấy đơn hàng theo ID"""
        return self.db.query(Order).filter(Order.order_id == order_id).first()
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Order]:
        """Lấy danh sách đơn hàng của người dùng"""
        return self.db.query(Order).filter(
            Order.user_id == user_id
        ).order_by(desc(Order.order_date)).offset(skip).limit(limit).all()
    
    def count_by_user_id(self, user_id: int) -> int:
        """Đếm tổng số đơn hàng của người dùng"""
        return self.db.query(Order).filter(Order.user_id == user_id).count()
    
    def create_order(self, order_data: Dict[str, Any]) -> Order:
        """Tạo đơn hàng mới"""
        order = Order(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def update_status(self, order_id: int, status: OrderStatus) -> Optional[Order]:
        """Cập nhật trạng thái đơn hàng"""
        order = self.get_by_id(order_id)
        if order:
            order.status = status
            order.updated_at = datetime.utcnow()
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
        return order
    
    def get_orders_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 20) -> List[Order]:
        """Lấy danh sách đơn hàng theo trạng thái"""
        return self.db.query(Order).filter(
            Order.status == status
        ).order_by(desc(Order.order_date)).offset(skip).limit(limit).all()
    
    def get_recent_orders(self, days: int = 30) -> List[Order]:
        """Lấy danh sách đơn hàng trong khoảng thời gian gần đây (dùng cho huấn luyện mô hình)"""
        start_date = datetime.utcnow() - datetime.timedelta(days=days)
        return self.db.query(Order).filter(
            Order.order_date >= start_date
        ).order_by(Order.order_date).all()

class OrderItemRepository(BaseRepository[OrderItem]):
    def __init__(self, db: Session):
        super().__init__(db, OrderItem)
    
    def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        """Lấy tất cả các mục trong đơn hàng"""
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    def create_order_item(self, order_item_data: Dict[str, Any]) -> OrderItem:
        """Tạo mục đơn hàng mới"""
        order_item = OrderItem(**order_item_data)
        self.db.add(order_item)
        # Không commit ở đây vì sẽ được commit trong transaction tạo đơn hàng
        return order_item
    
    def create_batch(self, order_items_data: List[Dict[str, Any]]) -> List[OrderItem]:
        """Tạo nhiều mục đơn hàng cùng lúc"""
        order_items = [OrderItem(**item_data) for item_data in order_items_data]
        self.db.add_all(order_items)
        # Không commit ở đây vì sẽ được commit trong transaction tạo đơn hàng
        return order_items
    
    def get_best_selling_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy danh sách sản phẩm bán chạy nhất"""
        from sqlalchemy import func
        from app.models.product import Product
        
        results = self.db.query(
            OrderItem.product_id,
            func.sum(OrderItem.quantity).label('total_quantity'),
            Product.name
        ).join(
            Product, OrderItem.product_id == Product.product_id
        ).group_by(
            OrderItem.product_id,
            Product.name
        ).order_by(
            desc('total_quantity')
        ).limit(limit).all()
        
        return [
            {
                "product_id": r.product_id, 
                "name": r.name, 
                "total_quantity": r.total_quantity
            } for r in results
        ]