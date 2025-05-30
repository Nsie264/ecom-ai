import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from scipy.sparse import csr_matrix

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """
    Lớp chịu trách nhiệm tiền xử lý dữ liệu tương tác người dùng
    trước khi đưa vào huấn luyện.
    """
    
    def __init__(self):
        # Lưu trữ ánh xạ giữa ID gốc và chỉ số sử dụng trong ma trận
        self.user_id_map = {}  # {user_id: matrix_index}
        self.product_id_map = {}  # {product_id: matrix_index}
        self.reverse_user_map = {}  # {matrix_index: user_id}
        self.reverse_product_map = {}  # {matrix_index: product_id}
    
    def process(self, raw_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Xử lý dữ liệu thô thành các định dạng phù hợp để huấn luyện mô hình.
        
        Parameters:
        -----------
        raw_data : Dict[str, pd.DataFrame]
            Dictionary chứa các DataFrame: 'ratings', 'views', 'purchases'
            
        Returns:
        --------
        Dict[str, Any]
            Dictionary chứa dữ liệu đã xử lý, bao gồm:
            - 'interaction_matrix': Ma trận tương tác user-item
            - 'user_id_map': Ánh xạ từ user_id gốc sang chỉ số ma trận
            - 'product_id_map': Ánh xạ từ product_id gốc sang chỉ số ma trận
            - 'reverse_user_map': Ánh xạ từ chỉ số ma trận sang user_id gốc
            - 'reverse_product_map': Ánh xạ từ chỉ số ma trận sang product_id gốc
        """
        logger.info("Bắt đầu tiền xử lý dữ liệu...")
        
        # Kết hợp các loại tương tác với trọng số khác nhau
        # Ratings (1-5) giữ nguyên
        # Views: mỗi lượt xem tính là 0.5 điểm
        # Purchases: mỗi lượt mua tính là 5 điểm
        

        combined_df = raw_data['ratings'].copy() if not raw_data['ratings'].empty else pd.DataFrame(columns=['user_id', 'product_id', 'rating'])
        combined_df = combined_df.rename(columns={'rating': 'score'})
        

        if not raw_data['views'].empty:
            views_grouped = raw_data['views'].groupby(['user_id', 'product_id']).size().reset_index(name='view_count')
            views_grouped['score'] = views_grouped['view_count'] * 0.5
            views_grouped = views_grouped.drop('view_count', axis=1)
            

            combined_df = pd.concat([combined_df, views_grouped], ignore_index=True)
        

        if not raw_data['purchases'].empty:
            purchases_grouped = raw_data['purchases'].groupby(['user_id', 'product_id'])['quantity'].sum().reset_index()
            purchases_grouped['score'] = 5.0  
            

            combined_df = pd.concat([combined_df, purchases_grouped[['user_id', 'product_id', 'score']]], ignore_index=True)
        

        if not combined_df.empty:
            combined_df = combined_df.groupby(['user_id', 'product_id'])['score'].max().reset_index()
        
        # Tạo ánh xạ ID
        unique_users = combined_df['user_id'].unique()
        unique_products = combined_df['product_id'].unique()
        
        self.user_id_map = {int(uid): i for i, uid in enumerate(unique_users)}
        self.product_id_map = {int(pid): i for i, pid in enumerate(unique_products)}
        self.reverse_user_map = {i: int(uid) for i, uid in enumerate(unique_users)}
        self.reverse_product_map = {i: int(pid) for i, pid in enumerate(unique_products)}
        
        # Tạo ma trận tương tác
        if combined_df.empty:
            logger.warning("Không có dữ liệu tương tác để xử lý!")
            # Tạo ma trận rỗng
            interaction_matrix = csr_matrix((0, 0))
        else:
            # Chuyển đổi ID sang chỉ số ma trận
            combined_df['user_idx'] = combined_df['user_id'].map(self.user_id_map)
            combined_df['product_idx'] = combined_df['product_id'].map(self.product_id_map)
            
            # Tạo ma trận tương tác thưa (sparse matrix)
            interaction_matrix = csr_matrix(
                (combined_df['score'], (combined_df['user_idx'], combined_df['product_idx'])),
                shape=(len(unique_users), len(unique_products))
            )
        
        logger.info(f"Đã xử lý xong ma trận tương tác kích thước {interaction_matrix.shape}")
        
        return {
            'interaction_matrix': interaction_matrix,
            'user_id_map': self.user_id_map,
            'product_id_map': self.product_id_map,
            'reverse_user_map': self.reverse_user_map,
            'reverse_product_map': self.reverse_product_map
        }