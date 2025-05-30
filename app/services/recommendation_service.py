from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.recommendations.repositories.recommendation_repository import (
    ProductSimilarityRepository, UserRecommendationRepository
)
from app.repositories.product_repository import ProductRepository
from app.repositories.interaction_repository import ViewHistoryRepository
from app.repositories.training_history_repository import TrainingHistoryRepository

class RecommendationService:
    """Service xử lý logic nghiệp vụ cho việc gợi ý sản phẩm (Module 3)"""
    
    def __init__(self, db: Session):
        self.db = db
        self.product_similarity_repo = ProductSimilarityRepository(db)
        self.user_recommendation_repo = UserRecommendationRepository(db)
        self.product_repo = ProductRepository(db)
        self.view_history_repo = ViewHistoryRepository(db)
        self.training_history_repo = TrainingHistoryRepository(db)
    
    def get_similar_products(self, product_id: int, limit: int = 10) -> Dict[str, Any]:
        """
        Lấy danh sách sản phẩm tương tự với một sản phẩm cụ thể.
        Chức năng này được hiển thị trên trang chi tiết sản phẩm.
        
        Parameters:
        -----------
        product_id : int
            ID của sản phẩm cần tìm các sản phẩm tương tự
        limit : int
            Số lượng sản phẩm tương tự tối đa cần trả về
            
        Returns:
        --------
        Dict[str, Any]
            Danh sách sản phẩm tương tự và thông tin liên quan
        """
        # Kiểm tra xem sản phẩm có tồn tại không
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            return {
                "success": False,
                "message": "Sản phẩm không tồn tại hoặc không còn hoạt động"
            }
        
        # Lấy danh sách ID sản phẩm tương tự từ repository
        similar_products_with_scores = self.product_similarity_repo.get_similar_products(product_id, limit)
        
        # Nếu không có sản phẩm tương tự, trả về danh sách trống
        if not similar_products_with_scores:
            return {
                "success": True,
                "product_id": product_id,
                "product_name": product.name,
                "similar_products": []
            }
        
        # Lấy ID của các sản phẩm tương tự
        similar_product_ids = [p_id for p_id, _ in similar_products_with_scores]
        
        # Lấy thông tin chi tiết của các sản phẩm tương tự
        similar_products_details = self.product_repo.get_by_ids(similar_product_ids)
        
        # Tạo map để nhanh chóng tra cứu điểm tương tự theo product_id
        similarity_scores = {p_id: score for p_id, score in similar_products_with_scores}
        
        # Format kết quả
        formatted_products = []
        for product in similar_products_details:
            # Lấy ảnh chính của sản phẩm
            primary_image = next((img.image_url for img in product.images if img.is_primary), 
                               (product.images[0].image_url if product.images else None))
            
            formatted_products.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "similarity_score": similarity_scores.get(product.product_id, 0),
                "image_url": primary_image
            })
        
        # Sắp xếp lại theo điểm tương tự
        formatted_products.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return {
            "success": True,
            "product_id": product_id,
            "product_name": product.name,
            "similar_products": formatted_products[:limit]
        }
    
    def get_personalized_recommendations(self, user_id: int, limit: int = 20) -> Dict[str, Any]:
        """
        Lấy danh sách sản phẩm được gợi ý cá nhân hóa cho người dùng.
        
        Parameters:
        -----------
        user_id : int
            ID của người dùng cần lấy gợi ý
        limit : int
            Số lượng sản phẩm gợi ý tối đa cần trả về
            
        Returns:
        --------
        Dict[str, Any]
            Danh sách sản phẩm được gợi ý và thông tin liên quan
        """
        # Lấy đối tượng User đầy đủ từ repository
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository(self.db)
        user = user_repo.get_by_id(user_id)
        
        if not user:
            return {
                "success": False,
                "message": "Không tìm thấy thông tin người dùng"
            }

        # Lấy danh sách ID sản phẩm được gợi ý từ repository
        
        recommended_products_with_scores = self.user_recommendation_repo.get_recommendations_for_user(user, limit)
        
        # Nếu không có gợi ý, thử sử dụng chiến lược fallback
        if not recommended_products_with_scores:
            return self._get_fallback_recommendations(user, limit)
        
        # Lấy ID của các sản phẩm được gợi ý
        recommended_product_ids = [p_id for p_id, _ in recommended_products_with_scores]
        
        # Lấy thông tin chi tiết của các sản phẩm được gợi ý
        recommended_products_details = self.product_repo.get_by_ids(recommended_product_ids)
        
        # Tạo map để nhanh chóng tra cứu điểm gợi ý theo product_id
        recommendation_scores = {p_id: score for p_id, score in recommended_products_with_scores}
        
        # Format kết quả
        formatted_recommendations = []
        for product in recommended_products_details:
            # Lấy ảnh chính của sản phẩm
            primary_image = next((img.image_url for img in product.images if img.is_primary), 
                               (product.images[0].image_url if product.images else None))
            
            formatted_recommendations.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "recommendation_score": recommendation_scores.get(product.product_id, 0),
                "image_url": primary_image
            })
        
        return {
            "success": True,
            "user_id": user.user_id,
            "recommendations": formatted_recommendations,
            "recommendation_type": "personalized"
        }
    
    def _get_fallback_recommendations(self, user, limit: int = 20) -> Dict[str, Any]:
        """
        Chiến lược dự phòng khi không có gợi ý cá nhân hóa
        
        Parameters:
        -----------
        user : User
            Đối tượng User cần lấy gợi ý dự phòng
        limit : int
            Số lượng sản phẩm gợi ý tối đa cần trả về
            
        Strategy:
        1. Lấy lịch sử xem gần đây của người dùng
        2. Nếu có, lấy sản phẩm được xem gần nhất và tìm các sản phẩm tương tự
        3. Nếu không, trả về các sản phẩm mới nhất
        """
        # Lấy lịch sử xem gần đây của người dùng
        recent_views = self.view_history_repo.get_by_user_id(user.user_id, limit=5)
        
        # Nếu người dùng đã xem sản phẩm
        if recent_views:
            # Lấy sản phẩm được xem gần nhất
            most_recent_view = recent_views[0]
            
            # Lấy các sản phẩm tương tự với sản phẩm đã xem gần nhất
            similar_products_result = self.get_similar_products(most_recent_view.product_id, limit)
            
            if similar_products_result.get("success") and similar_products_result.get("similar_products"):
                return {
                    "success": True,
                    "user_id": user.user_id,
                    "recommendations": similar_products_result.get("similar_products"),
                    "recommendation_type": "based_on_history",
                    "based_on_product_id": most_recent_view.product_id,
                    "based_on_product_name": similar_products_result.get("product_name")
                }
        
        # Fallback: Lấy sản phẩm mới nhất
        latest_products = self.product_repo.get_multi(limit=limit, order_by="created_at", descending=True)
        
        # Format kết quả
        formatted_latest = []
        for product in latest_products:
            # Lấy ảnh chính của sản phẩm
            primary_image = next((img.image_url for img in product.images if img.is_primary), 
                               (product.images[0].image_url if product.images else None))
            
            formatted_latest.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "image_url": primary_image
            })
        
        return {
            "success": True,
            "user_id": user.user_id,
            "recommendations": formatted_latest,
            "recommendation_type": "latest_products"
        }
    
    def trigger_training_job(self, admin_id: str) -> Dict[str, Any]:
        """
        Kích hoạt job huấn luyện mô hình theo yêu cầu từ admin
        
        Parameters:
        -----------
        admin_id : str
            ID của admin đã kích hoạt quá trình huấn luyện
            
        Returns:
        --------
        Dict[str, Any]
            Kết quả kích hoạt job
        """
        try:
            from app.recommendations.training.job import TrainingJob
            
            # Gọi job huấn luyện với admin_id
            result = TrainingJob.run_manual(admin_id=admin_id, db=self.db)
            
            return {
                "success": True,
                "message": "Đã kích hoạt job huấn luyện mô hình thành công",
                "job_result": result
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi kích hoạt job huấn luyện: {str(e)}"
            }
    
    def get_training_history(self, limit: int = 10) -> Dict[str, Any]:
        """
        Lấy lịch sử các lần huấn luyện mô hình gợi ý
        
        Parameters:
        -----------
        limit : int
            Số lượng bản ghi lịch sử tối đa cần trả về
            
        Returns:
        --------
        Dict[str, Any]
            Danh sách lịch sử huấn luyện mô hình
        """
        try:
            # Lấy lịch sử huấn luyện từ repository
            history_records = self.training_history_repo.get_training_history(limit)
            
            # Format kết quả
            formatted_history = []
            for record in history_records:
                formatted_history.append({
                    "history_id": record.history_id,
                    "start_time": record.start_time.isoformat(),
                    "end_time": record.end_time.isoformat() if record.end_time else None,
                    "status": record.status,
                    "triggered_by": record.triggered_by,
                    "message": record.message
                })
            
            return {
                "success": True,
                "history": formatted_history
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi lấy lịch sử huấn luyện: {str(e)}"
            }
    
    def get_training_job_by_id(self, history_id: int) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết về một lần huấn luyện cụ thể
        
        Parameters:
        -----------
        history_id : int
            ID của bản ghi lịch sử huấn luyện cần lấy thông tin
            
        Returns:
        --------
        Dict[str, Any]
            Thông tin chi tiết về lần huấn luyện
        """
        try:
            # Lấy chi tiết bản ghi huấn luyện từ repository
            training_job = self.training_history_repo.get_training_job(history_id)
            
            if not training_job:
                return {
                    "success": False,
                    "message": f"Không tìm thấy thông tin huấn luyện với ID: {history_id}"
                }
            
            # Format kết quả
            formatted_job = {
                "history_id": training_job.history_id,
                "start_time": training_job.start_time.isoformat(),
                "end_time": training_job.end_time.isoformat() if training_job.end_time else None,
                "status": training_job.status,
                "triggered_by": training_job.triggered_by,
                "message": training_job.message,
                "duration": str(training_job.end_time - training_job.start_time) if training_job.end_time else "Running"
            }
            
            return {
                "success": True,
                "training_job": formatted_job
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi lấy thông tin huấn luyện: {str(e)}"
            }
    
    def get_training_job_details(self, history_id: int) -> Dict[str, Any]:
        """
        Lấy chi tiết của một bản ghi huấn luyện cụ thể
        
        Parameters:
        -----------
        history_id : int
            ID của bản ghi huấn luyện cần lấy thông tin
            
        Returns:
        --------
        Dict[str, Any]
            Thông tin chi tiết của bản ghi huấn luyện
        """
        try:
            # Lấy bản ghi huấn luyện từ repository
            training_record = self.training_history_repo.get_training_job(history_id)
            
            if not training_record:
                return {
                    "success": False,
                    "message": f"Không tìm thấy bản ghi huấn luyện với ID {history_id}"
                }
            
            # Format kết quả
            training_details = {
                "history_id": training_record.history_id,
                "start_time": training_record.start_time.isoformat() if training_record.start_time else None,
                "end_time": training_record.end_time.isoformat() if training_record.end_time else None,
                "status": training_record.status,
                "triggered_by": training_record.triggered_by,
                "message": training_record.message,
                "duration_seconds": (training_record.end_time - training_record.start_time).total_seconds() 
                                   if (training_record.end_time and training_record.start_time) else None
            }
            
            return {
                "success": True,
                "training_details": training_details
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi lấy chi tiết bản ghi huấn luyện: {str(e)}"
            }