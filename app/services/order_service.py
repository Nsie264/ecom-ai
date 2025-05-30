from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import json
from datetime import datetime

from app.models.order import OrderStatus, PaymentMethod
from app.repositories.order_repository import OrderRepository, OrderItemRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.interaction_repository import CartRepository
from app.repositories.user_repository import UserAddressRepository

class OrderService:
    """Service xử lý logic nghiệp vụ cho đơn hàng"""
    
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)
        self.product_repo = ProductRepository(db)
        self.cart_repo = CartRepository(db)
        self.address_repo = UserAddressRepository(db)
    
    def get_orders_by_user(self, user_id: int, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Lấy danh sách đơn hàng của người dùng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
        page : int
            Số trang hiện tại
        page_size : int
            Số đơn hàng mỗi trang
            
        Returns:
        --------
        Dict[str, Any]
            Danh sách đơn hàng đã phân trang
        """
        # Tính toán offset cho phân trang
        skip = (page - 1) * page_size
        
        # Lấy danh sách đơn hàng
        orders = self.order_repo.get_by_user_id(user_id, skip=skip, limit=page_size)
        
        # Đếm tổng số đơn hàng
        total_count = self.order_repo.count_by_user_id(user_id)
        
        # Tính tổng số trang
        total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 0
        
        # Format kết quả
        formatted_orders = []
        for order in orders:
            order_items = self.order_item_repo.get_by_order_id(order.order_id)
            
            formatted_orders.append({
                "order_id": order.order_id,
                "order_date": order.order_date.isoformat(),
                "status": order.status.value,
                "total_amount": order.total_amount,
                "payment_method": order.payment_method.value,
                "item_count": len(order_items),
                "shipping_address": order.shipping_address  # Đã lưu dưới dạng JSON
            })
        
        return {
            "items": formatted_orders,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages
            }
        }
    
    def get_order_details(self, order_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Lấy chi tiết đơn hàng
        
        Parameters:
        -----------
        order_id : int
            ID của đơn hàng
        user_id : int, optional
            ID của người dùng (để kiểm tra quyền truy cập)
            
        Returns:
        --------
        Dict[str, Any]
            Chi tiết đơn hàng
        """
        # Lấy thông tin đơn hàng
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return {"success": False, "message": "Đơn hàng không tồn tại"}
        
        # Kiểm tra quyền truy cập (nếu có user_id)
        if user_id is not None and order.user_id != user_id:
            return {"success": False, "message": "Bạn không có quyền xem đơn hàng này"}
        
        # Lấy các mục trong đơn hàng
        order_items = self.order_item_repo.get_by_order_id(order_id)
        
        # Format kết quả
        formatted_items = []
        for item in order_items:
            # Lấy thông tin sản phẩm hiện tại (có thể không còn tồn tại)
            product = self.product_repo.get_by_id(item.product_id)
            
            formatted_items.append({
                "order_item_id": item.order_item_id,
                "product_id": item.product_id,
                "product_name": product.name if product else "Sản phẩm không còn tồn tại",
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase,
                "subtotal": item.price_at_purchase * item.quantity,
                "image_url": next((img.image_url for img in product.images if img.is_primary), 
                                 (product.images[0].image_url if product and product.images else None)) if product else None
            })
        
        return {
            "success": True,
            "order": {
                "order_id": order.order_id,
                "user_id": order.user_id,
                "order_date": order.order_date.isoformat(),
                "status": order.status.value,
                "total_amount": order.total_amount,
                "payment_method": order.payment_method.value,
                "shipping_address": order.shipping_address,  # Đã lưu dưới dạng JSON
                "notes": order.notes,
                "items": formatted_items
            }
        }
    
    def place_order(self, user_id: int, address_id: int, notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Đặt đơn hàng từ giỏ hàng hiện tại của người dùng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
        address_id : int
            ID của địa chỉ giao hàng
        notes : str, optional
            Ghi chú cho đơn hàng
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả đặt hàng
        """
        # Bắt đầu transaction
        try:
            # 1. Lấy giỏ hàng
            cart_items = self.cart_repo.get_by_user_id(user_id)
            if not cart_items:
                return {"success": False, "message": "Giỏ hàng trống, không thể đặt hàng"}
            
            # 2. Lấy địa chỉ giao hàng
            address = self.address_repo.get_by_id(address_id)
            if not address or address.user_id != user_id:
                return {"success": False, "message": "Địa chỉ giao hàng không hợp lệ"}
            
            # 3. Convert địa chỉ thành JSON để lưu
            shipping_address = {
                "address_id": address.address_id,
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "postal_code": address.postal_code,
                "phone": address.phone
            }
            
            # 4. Kiểm tra tồn kho và tính tổng tiền
            total_amount = 0.0
            order_items_data = []
            products_to_update = []
            
            for cart_item in cart_items:
                # Kiểm tra và khóa tồn kho
                if not self.product_repo.check_and_lock_stock(cart_item.product_id, cart_item.quantity):
                    # Rollback transaction
                    self.db.rollback()
                    return {"success": False, "message": f"Sản phẩm (ID: {cart_item.product_id}) không đủ số lượng trong kho"}
                
                # Lấy thông tin sản phẩm
                product = self.product_repo.get_by_id(cart_item.product_id)
                if not product or not product.is_active:
                    # Rollback transaction
                    self.db.rollback()
                    return {"success": False, "message": f"Sản phẩm (ID: {cart_item.product_id}) không còn tồn tại hoặc không hoạt động"}
                
                # Tính tiền cho mục này
                item_total = product.price * cart_item.quantity
                total_amount += item_total
                
                # Chuẩn bị dữ liệu order_item
                order_items_data.append({
                    "product_id": product.product_id,
                    "quantity": cart_item.quantity,
                    "price_at_purchase": product.price
                })
                
                # Thêm vào danh sách sản phẩm cần cập nhật tồn kho
                products_to_update.append((product.product_id, cart_item.quantity))
            
            # 5. Tạo đơn hàng
            order_data = {
                "user_id": user_id,
                "order_date": datetime.utcnow(),
                "total_amount": total_amount,
                "status": OrderStatus.PENDING,
                "payment_method": PaymentMethod.COD,  # Mặc định là COD
                "shipping_address": shipping_address,
                "notes": notes
            }
            
            order = self.order_repo.create_order(order_data)
            
            # 6. Tạo chi tiết đơn hàng
            for item_data in order_items_data:
                item_data["order_id"] = order.order_id
                self.order_item_repo.create_order_item(item_data)
            
            # 7. Cập nhật tồn kho
            for product_id, quantity in products_to_update:
                self.product_repo.decrease_stock(product_id, quantity)
            
            # 8. Xóa giỏ hàng
            self.cart_repo.clear_cart(user_id)
            
            # 9. Commit transaction
            self.db.commit()
            
            # 10. Trả về kết quả thành công
            return {
                "success": True,
                "message": "Đặt hàng thành công",
                "order_id": order.order_id,
                "total_amount": total_amount
            }
            
        except Exception as e:
            # Rollback nếu có lỗi
            self.db.rollback()
            return {"success": False, "message": f"Lỗi khi đặt hàng: {str(e)}"}
    
    def cancel_order(self, order_id: int, user_id: int) -> Dict[str, Any]:
        """
        Hủy đơn hàng nếu đơn hàng ở trạng thái PENDING
        
        Parameters:
        -----------
        order_id : int
            ID của đơn hàng
        user_id : int
            ID của người dùng (để kiểm tra quyền)
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả hủy đơn hàng
        """
        # Lấy thông tin đơn hàng
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return {"success": False, "message": "Đơn hàng không tồn tại"}
        
        # Kiểm tra quyền 
        if order.user_id != user_id:
            return {"success": False, "message": "Bạn không có quyền hủy đơn hàng này"}
        
        # Kiểm tra trạng thái đơn hàng
        if order.status != OrderStatus.PENDING:
            return {"success": False, "message": f"Không thể hủy đơn hàng ở trạng thái {order.status.value}"}
        
        try:
            # Bắt đầu transaction
            
            # 1. Cập nhật trạng thái đơn hàng thành CANCELLED
            order = self.order_repo.update_status(order_id, OrderStatus.CANCELLED)
            
            # 2. Hoàn trả số lượng tồn kho
            order_items = self.order_item_repo.get_by_order_id(order_id)
            for item in order_items:
                product = self.product_repo.get_by_id(item.product_id)
                if product:
                    # Tăng số lượng tồn kho
                    product.stock_quantity += item.quantity
                    self.db.add(product)
            
            # 3. Commit transaction
            self.db.commit()
            
            # 4. Trả về kết quả thành công
            return {
                "success": True,
                "message": "Hủy đơn hàng thành công",
                "order_id": order_id
            }
            
        except Exception as e:
            # Rollback nếu có lỗi
            self.db.rollback()
            return {"success": False, "message": f"Lỗi khi hủy đơn hàng: {str(e)}"}