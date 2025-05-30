import logging
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

from app.recommendations.repositories.recommendation_repository import (
    ProductSimilarityRepository,
    UserRecommendationRepository
)

logger = logging.getLogger(__name__)

class RecommendationResultWriter:
    """
    Lớp chịu trách nhiệm tính toán và lưu trữ kết quả huấn luyện mô hình
    vào cơ sở dữ liệu để sử dụng trong việc gợi ý sản phẩm.
    """
    
    def __init__(self, product_similarity_repo: ProductSimilarityRepository,
                 user_recommendation_repo: UserRecommendationRepository):
        self.product_similarity_repo = product_similarity_repo
        self.user_recommendation_repo = user_recommendation_repo
    
    def calculate_and_save_results(self, model_result: Dict[str, Any]) -> None:
        """
        Tính toán độ tương tự giữa các sản phẩm và gợi ý top-N cho người dùng,
        sau đó lưu vào cơ sở dữ liệu.
        
        Parameters:
        -----------
        model_result : Dict[str, Any]
            Kết quả từ việc huấn luyện mô hình, bao gồm:
            - 'user_factors': Ma trận latent factors cho users
            - 'item_factors': Ma trận latent factors cho items
            - 'user_id_map': Ánh xạ từ user_id gốc sang chỉ số ma trận
            - 'product_id_map': Ánh xạ từ product_id gốc sang chỉ số ma trận
            - 'reverse_user_map': Ánh xạ từ chỉ số ma trận sang user_id gốc
            - 'reverse_product_map': Ánh xạ từ chỉ số ma trận sang product_id gốc
        """
        logger.info("Bắt đầu tính toán và lưu kết quả huấn luyện...")
        
        # Kiểm tra kết quả huấn luyện
        if (model_result.get('user_factors') is None or len(model_result['user_factors']) == 0 or
            model_result.get('item_factors') is None or len(model_result['item_factors']) == 0):
            logger.warning("Kết quả huấn luyện không hợp lệ, không thể tính toán và lưu kết quả.")
            return
        
        # Lấy dữ liệu từ kết quả huấn luyện
        user_factors = model_result['user_factors']
        item_factors = model_result['item_factors']
        user_id_map = model_result['user_id_map']
        product_id_map = model_result['product_id_map']
        reverse_user_map = model_result['reverse_user_map']
        reverse_product_map = model_result['reverse_product_map']
        
        # 1. Tính độ tương tự giữa các sản phẩm sử dụng cosine similarity
        self._calculate_and_save_product_similarities(
            item_factors, product_id_map, reverse_product_map
        )
        
        # 2. Tính và lưu trữ gợi ý top-N cho mỗi người dùng
        self._calculate_and_save_user_recommendations(
            user_factors, item_factors, user_id_map, 
            product_id_map, reverse_user_map, reverse_product_map
        )
        
        logger.info("Hoàn thành việc tính toán và lưu kết quả huấn luyện")
    
    def _calculate_and_save_product_similarities(
        self, 
        item_factors: np.ndarray,
        product_id_map: Dict[int, int],
        reverse_product_map: Dict[int, int],
        top_n: int = 20,
        similarity_threshold: float = 0.01
    ) -> None:
        """
        Tính và lưu độ tương tự giữa các sản phẩm.
        
        Parameters:
        -----------
        item_factors : np.ndarray
            Ma trận latent factors cho các sản phẩm
        product_id_map : Dict[int, int]
            Ánh xạ product_id -> index trong item_factors
        reverse_product_map : Dict[int, int]
            Ánh xạ index -> product_id
        top_n : int
            Số lượng sản phẩm tương tự cần lưu cho mỗi sản phẩm
        similarity_threshold : float
            Ngưỡng độ tương tự tối thiểu để lưu vào cơ sở dữ liệu
        """
        logger.info(f"Tính toán độ tương tự giữa {len(product_id_map)} sản phẩm...")
        
        # Tính ma trận tương tự cosine giữa các sản phẩm
        similarity_matrix = cosine_similarity(item_factors)
        
        # Xóa dữ liệu cũ
        logger.info("Xóa dữ liệu tương tự sản phẩm cũ...")
        self.product_similarity_repo.delete_all()
        
        # Chuẩn bị dữ liệu mới
        similarity_data = []
        
        # Duyệt qua từng sản phẩm
        for idx_a in range(len(item_factors)):
            # Lấy product_id gốc của sản phẩm A
            product_id_a = reverse_product_map.get(idx_a)
            if product_id_a is None:
                continue
                
            # Lấy top-N sản phẩm tương tự với sản phẩm A
            # Loại trừ bản thân sản phẩm A (self-similarity)
            similarities = [(idx_b, similarity_matrix[idx_a, idx_b]) 
                           for idx_b in range(len(item_factors)) if idx_a != idx_b]
            
            # Sắp xếp theo độ tương tự giảm dần
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Lấy top-N
            top_similar = similarities[:top_n]
            
            # Tạo bản ghi mới
            for idx_b, sim_score in top_similar:
                # Lấy product_id gốc của sản phẩm B
                product_id_b = reverse_product_map.get(idx_b)
                if product_id_b is None:
                    continue
                
                # Chỉ lưu những cặp có độ tương tự trên ngưỡng
                if sim_score >= similarity_threshold:
                    similarity_data.append({
                        'product_id_a': product_id_a,
                        'product_id_b': product_id_b,
                        'similarity_score': float(sim_score),
                        'updated_at': datetime.utcnow()
                    })
        
        # Lưu vào cơ sở dữ liệu
        if similarity_data:
            logger.info(f"Lưu {len(similarity_data)} bản ghi độ tương tự sản phẩm mới")
            self.product_similarity_repo.batch_upsert(similarity_data)
        else:
            logger.warning("Không có dữ liệu độ tương tự sản phẩm để lưu")
    
    def _calculate_and_save_user_recommendations(
        self,
        user_factors: np.ndarray,
        item_factors: np.ndarray,
        user_id_map: Dict[int, int],
        product_id_map: Dict[int, int],
        reverse_user_map: Dict[int, int],
        reverse_product_map: Dict[int, int],
        top_n: int = 50
    ) -> None:
        """
        Tính và lưu gợi ý top-N cho mỗi người dùng.
        
        Parameters:
        -----------
        user_factors : np.ndarray
            Ma trận latent factors cho người dùng
        item_factors : np.ndarray
            Ma trận latent factors cho sản phẩm
        user_id_map, product_id_map, reverse_user_map, reverse_product_map : Dict
            Các ánh xạ giữa ID gốc và index trong ma trận
        top_n : int
            Số lượng gợi ý cần lưu cho mỗi người dùng
        """
        logger.info(f"Tính toán gợi ý cho {len(user_id_map)} người dùng...")
        
        # Xóa dữ liệu cũ
        logger.info("Xóa dữ liệu gợi ý cũ...")
        self.user_recommendation_repo.delete_all()
        
        # Chuẩn bị dữ liệu mới
        recommendation_data = []
        
        # Duyệt qua từng người dùng
        for user_idx, user_vector in enumerate(user_factors):
            # Lấy user_id gốc
            user_id = reverse_user_map.get(user_idx)
            if user_id is None:
                continue
            
            # Tính điểm dự đoán cho tất cả sản phẩm
            # scores = user_vector.dot(item_factors.T)
            scores = np.dot(user_vector, item_factors.T)
            
            # Lấy top-N sản phẩm
            top_indices = np.argsort(-scores)[:top_n]
            
            # Tạo bản ghi mới
            for rank, item_idx in enumerate(top_indices):
                # Lấy product_id gốc
                product_id = reverse_product_map.get(item_idx)
                if product_id is None:
                    continue
                
                recommendation_data.append({
                    'user_id': user_id,
                    'product_id': product_id,
                    'recommendation_score': float(scores[item_idx]),
                    'rank': rank + 1,  # Rank bắt đầu từ 1
                    'updated_at': datetime.utcnow()
                })
        
        # Lưu vào cơ sở dữ liệu
        if recommendation_data:
            logger.info(f"Lưu {len(recommendation_data)} bản ghi gợi ý mới")
            self.user_recommendation_repo.batch_upsert(recommendation_data)
        else:
            logger.warning("Không có dữ liệu gợi ý để lưu")