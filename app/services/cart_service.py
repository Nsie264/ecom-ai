from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.repositories.interaction_repository import CartRepository
from app.repositories.product_repository import ProductRepository

class CartService:
    """Service xử lý logic nghiệp vụ cho giỏ hàng"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
    
    def get_cart(self, user_id: int) -> Dict[str, Any]:
        """
        Lấy thông tin giỏ hàng của người dùng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
            
        Returns:
        --------
        Dict[str, Any]
            Thông tin giỏ hàng bao gồm danh sách sản phẩm và tổng tiền
        """
        # Lấy các mục trong giỏ hàng
        cart_items = self.cart_repo.get_by_user_id(user_id)
        
        # Lấy danh sách ID sản phẩm
        product_ids = [item.product_id for item in cart_items]
        
        # Lấy thông tin chi tiết sản phẩm
        products = self.product_repo.get_by_ids(product_ids)
        
        # Tạo map sản phẩm để dễ truy cập
        product_map = {p.product_id: p for p in products}
        
        # Tính tổng tiền và format kết quả
        total_amount = 0.0
        items = []
        
        for cart_item in cart_items:
            product = product_map.get(cart_item.product_id)
            
            if product and product.is_active:
                # Tính giá tiền của mục này
                item_total = product.price * cart_item.quantity
                total_amount += item_total
                
                # Lấy ảnh chính của sản phẩm
                primary_image = next((img.image_url for img in product.images if img.is_primary), 
                                    (product.images[0].image_url if product.images else None))
                
                # Thêm vào danh sách kết quả
                items.append({
                    "cart_item_id": cart_item.cart_item_id,
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": cart_item.quantity,
                    "subtotal": item_total,
                    "image_url": primary_image,
                    "stock_quantity": product.stock_quantity,
                    "is_in_stock": product.stock_quantity >= cart_item.quantity
                })
        
        return {
            "items": items,
            "total_amount": total_amount,
            "item_count": len(items)
        }
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        """
        Thêm sản phẩm vào giỏ hàng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
        product_id : int
            ID của sản phẩm cần thêm
        quantity : int
            Số lượng sản phẩm cần thêm
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả thao tác và giỏ hàng cập nhật
        """
        # Kiểm tra sản phẩm tồn tại và đang hoạt động
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            return {"success": False, "message": "Sản phẩm không tồn tại hoặc không còn hoạt động"}
        
        # Kiểm tra số lượng tồn kho
        if product.stock_quantity < quantity:
            return {"success": False, "message": f"Số lượng sản phẩm trong kho không đủ (hiện có {product.stock_quantity})"}
        
        # Thêm vào giỏ hàng
        self.cart_repo.add_item(user_id, product_id, quantity)
        
        # Trả về giỏ hàng đã cập nhật
        updated_cart = self.get_cart(user_id)
        return {
            "success": True,
            "message": f"Đã thêm {quantity} {product.name} vào giỏ hàng",
            "cart": updated_cart
        }
    
    def update_cart_item(self, user_id: int, product_id: int, quantity: int) -> Dict[str, Any]:
        """
        Cập nhật số lượng sản phẩm trong giỏ hàng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
        product_id : int
            ID của sản phẩm cần cập nhật
        quantity : int
            Số lượng mới
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả thao tác và giỏ hàng cập nhật
        """
        # Kiểm tra sản phẩm có trong giỏ hàng không
        cart_item = self.cart_repo.get_by_user_and_product(user_id, product_id)
        if not cart_item:
            return {"success": False, "message": "Sản phẩm không có trong giỏ hàng"}
        
        # Xử lý trường hợp xóa khỏi giỏ hàng
        if quantity <= 0:
            self.cart_repo.remove_item(user_id, product_id)
            updated_cart = self.get_cart(user_id)
            return {
                "success": True,
                "message": "Đã xóa sản phẩm khỏi giỏ hàng",
                "cart": updated_cart
            }
        
        # Kiểm tra sản phẩm tồn tại và đang hoạt động
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            return {"success": False, "message": "Sản phẩm không tồn tại hoặc không còn hoạt động"}
        
        # Kiểm tra số lượng tồn kho
        if product.stock_quantity < quantity:
            return {"success": False, "message": f"Số lượng sản phẩm trong kho không đủ (hiện có {product.stock_quantity})"}
        
        # Cập nhật số lượng
        self.cart_repo.update_quantity(user_id, product_id, quantity)
        
        # Trả về giỏ hàng đã cập nhật
        updated_cart = self.get_cart(user_id)
        return {
            "success": True,
            "message": f"Đã cập nhật số lượng {product.name} thành {quantity}",
            "cart": updated_cart
        }
    
    def remove_from_cart(self, user_id: int, product_id: int) -> Dict[str, Any]:
        """
        Xóa sản phẩm khỏi giỏ hàng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
        product_id : int
            ID của sản phẩm cần xóa
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả thao tác và giỏ hàng cập nhật
        """
        # Kiểm tra sản phẩm có trong giỏ hàng không
        cart_item = self.cart_repo.get_by_user_and_product(user_id, product_id)
        if not cart_item:
            return {"success": False, "message": "Sản phẩm không có trong giỏ hàng"}
        
        # Lấy tên sản phẩm để hiển thị trong thông báo
        product = self.product_repo.get_by_id(product_id)
        product_name = product.name if product else "Sản phẩm"
        
        # Xóa khỏi giỏ hàng
        self.cart_repo.remove_item(user_id, product_id)
        
        # Trả về giỏ hàng đã cập nhật
        updated_cart = self.get_cart(user_id)
        return {
            "success": True,
            "message": f"Đã xóa {product_name} khỏi giỏ hàng",
            "cart": updated_cart
        }
    
    def clear_cart(self, user_id: int) -> Dict[str, Any]:
        """
        Xóa toàn bộ giỏ hàng của người dùng
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả thao tác
        """
        self.cart_repo.clear_cart(user_id)
        
        return {
            "success": True,
            "message": "Đã xóa toàn bộ giỏ hàng",
            "cart": {"items": [], "total_amount": 0.0, "item_count": 0}
        }