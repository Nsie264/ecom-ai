import logging
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
import joblib
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class RecommendationModelTrainer:
    """Interface cơ bản cho các lớp trainer khác nhau."""
    
    def train(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Huấn luyện mô hình từ dữ liệu đã xử lý.
        
        Parameters:
        -----------
        processed_data : Dict[str, Any]
            Dữ liệu đã xử lý bởi DataPreprocessor
        
        Returns:
        --------
        Dict[str, Any]
            Kết quả huấn luyện bao gồm các vector đặc trưng
        """
        raise NotImplementedError("Các lớp con phải triển khai phương thức này")


class MatrixFactorizationTrainer(RecommendationModelTrainer):
    """
    Lớp huấn luyện mô hình Matrix Factorization sử dụng
    SVD (Singular Value Decomposition) từ scikit-learn.
    """
    
    def __init__(self, n_factors: int = 100, n_iterations: int = 10):
        """
        Khởi tạo trainer.
        
        Parameters:
        -----------
        n_factors : int
            Số lượng latent factors (khuyến nghị 50-150)
        n_iterations : int
            Số vòng lặp tối đa khi huấn luyện
        """
        self.n_factors = n_factors
        self.n_iterations = n_iterations
        self.model = None
    
    def train(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:

        logger.info(f"Bắt đầu huấn luyện mô hình Matrix Factorization với {self.n_factors} factors...")
        
        interaction_matrix = processed_data['interaction_matrix']
        
        # Kiểm tra kích thước ma trận tương tác
        if interaction_matrix.shape[0] == 0 or interaction_matrix.shape[1] == 0:
            logger.warning("Ma trận tương tác rỗng, không thể huấn luyện mô hình!")
            # Trả về ma trận factors rỗng
            return {
                'user_factors': np.array([]),
                'item_factors': np.array([]),
                'user_id_map': processed_data['user_id_map'],
                'product_id_map': processed_data['product_id_map'],
                'reverse_user_map': processed_data['reverse_user_map'],
                'reverse_product_map': processed_data['reverse_product_map']
            }
        
        # Điều chỉnh số latent factors nếu ma trận nhỏ
        n_factors = min(self.n_factors, min(interaction_matrix.shape) - 1)
        

        self.model = TruncatedSVD(n_components=n_factors, n_iter=self.n_iterations, random_state=42)
        item_factors = self.model.fit_transform(interaction_matrix)
        

        sigma = np.diag(self.model.singular_values_)
        VT = self.model.components_
        

        user_factors = interaction_matrix.dot(VT.T).dot(np.linalg.inv(sigma))
        
        logger.info(f"Hoàn thành huấn luyện mô hình. Kích thước ma trận user factors: {user_factors.shape}, item factors: {item_factors.shape}")
        

        self._save_model()
        
        return {
            'user_factors': user_factors,
            'item_factors': item_factors,
            'user_id_map': processed_data['user_id_map'],
            'product_id_map': processed_data['product_id_map'],
            'reverse_user_map': processed_data['reverse_user_map'],
            'reverse_product_map': processed_data['reverse_product_map']
        }
    
    def _save_model(self, path: Optional[str] = None) -> None:
        """Lưu mô hình để sử dụng sau này (tuỳ chọn)"""
        if self.model is None:
            logger.warning("Không có mô hình để lưu!")
            return
        
        if path is None:
            # Tạo thư mục models nếu chưa tồn tại
            os.makedirs('models', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"models/mf_model_{timestamp}.joblib"
            
        joblib.dump(self.model, path)
        logger.info(f"Đã lưu mô hình vào {path}")


class ModelEvaluator:
    """
    Lớp đánh giá hiệu năng của mô hình gợi ý.
    """
    
    def evaluate(self, model_result: Dict[str, Any], test_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Đánh giá hiệu năng mô hình trên tập test (tùy chọn).
        
        Lưu ý: Phiên bản này chỉ trả về một số liệu đơn giản.
        Trong thực tế, bạn có thể muốn đánh giá các chỉ số như Precision@k, Recall@k, NDCG, v.v.
        """

        n_users = len(model_result['user_id_map'])
        n_items = len(model_result['product_id_map'])
        
        return {
            'n_users': n_users,
            'n_items': n_items,
            'coverage': min(1.0, n_users * n_items / 1000000)  # Ví dụ đơn giản về coverage
        }