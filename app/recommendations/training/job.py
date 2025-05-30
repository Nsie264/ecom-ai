import logging
import time
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.recommendations.training.data_loader import DataLoader
from app.recommendations.training.data_preprocessor import DataPreprocessor
from app.recommendations.training.model_trainer import MatrixFactorizationTrainer, ModelEvaluator
from app.recommendations.training.result_writer import RecommendationResultWriter
from app.recommendations.repositories.recommendation_repository import ProductSimilarityRepository, UserRecommendationRepository
from app.repositories.training_history_repository import TrainingHistoryRepository

logger = logging.getLogger(__name__)

class TrainingJob:
    """
    Lớp điều phối toàn bộ quá trình huấn luyện mô hình gợi ý:
    1. Tải dữ liệu từ cơ sở dữ liệu
    2. Tiền xử lý dữ liệu
    3. Huấn luyện mô hình
    4. Đánh giá mô hình (tùy chọn)
    5. Lưu kết quả vào cơ sở dữ liệu
    """
    
    @classmethod
    def run(cls) -> Dict[str, Any]:
        """
        Chạy toàn bộ quy trình huấn luyện mô hình.
        Phương thức này được scheduler gọi định kỳ.
        """
        start_time = time.time()
        logger.info("=== BẮT ĐẦU QUÁ TRÌNH HUẤN LUYỆN MÔ HÌNH GỢI Ý ===")
        
        # Tạo session database mới
        db = SessionLocal()
        
        # Tạo bản ghi lịch sử huấn luyện
        history_repo = TrainingHistoryRepository(db)
        history = history_repo.create_training_job(triggered_by="SCHEDULED")
        
        try:
            # 1. Tải dữ liệu
            logger.info("1. Bắt đầu tải dữ liệu tương tác...")
            data_loader = DataLoader(db)
            raw_data = data_loader.get_interaction_data()
            logger.info(f"Đã tải xong dữ liệu: {sum(len(df) for df in raw_data.values())} bản ghi tương tác")
            
            # 2. Tiền xử lý dữ liệu
            logger.info("2. Bắt đầu tiền xử lý dữ liệu...")
            preprocessor = DataPreprocessor()
            processed_data = preprocessor.process(raw_data)
            logger.info(f"Đã xử lý xong dữ liệu: Ma trận tương tác kích thước {processed_data['interaction_matrix'].shape}")
            
            # 3. Huấn luyện mô hình
            logger.info("3. Bắt đầu huấn luyện mô hình...")
            trainer = MatrixFactorizationTrainer(n_factors=100, n_iterations=20)
            model_result = trainer.train(processed_data)
            
            # 4. Đánh giá mô hình (tùy chọn)
            logger.info("4. Đánh giá mô hình...")
            evaluator = ModelEvaluator()
            evaluation_result = evaluator.evaluate(model_result, processed_data)
            logger.info(f"Kết quả đánh giá: {evaluation_result}")
            
            # 5. Lưu kết quả huấn luyện vào DB
            logger.info("5. Lưu kết quả huấn luyện vào cơ sở dữ liệu...")
            product_similarity_repo = ProductSimilarityRepository(db)
            user_recommendation_repo = UserRecommendationRepository(db)
            result_writer = RecommendationResultWriter(
                product_similarity_repo, user_recommendation_repo
            )
            result_writer.calculate_and_save_results(model_result)
            
            # Cập nhật bản ghi lịch sử huấn luyện thành công
            history_repo.update_training_job(
                history_id=history.history_id,
                status="SUCCESS",
                message=f"Completed successfully. Evaluation: {evaluation_result}"
            )
            
            # Đóng kết nối DB
            db.close()
            
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"=== HOÀN THÀNH QUÁ TRÌNH HUẤN LUYỆN MÔ HÌNH (thời gian: {execution_time:.2f} giây) ===")
            
            return {
                "success": True,
                "execution_time": execution_time,
                "timestamp": datetime.utcnow().isoformat(),
                "evaluation": evaluation_result,
                "history_id": history.history_id
            }
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình huấn luyện mô hình: {str(e)}", exc_info=True)
            
            # Cập nhật bản ghi lịch sử huấn luyện thất bại
            history_repo.update_training_job(
                history_id=history.history_id,
                status="FAILED",
                message=str(e)
            )
            
            try:
                db.close()
            except:
                pass
                
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "history_id": history.history_id
            }
    
    @classmethod
    def run_manual(cls, admin_id: str, db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Chạy quá trình huấn luyện mô hình theo yêu cầu thủ công (từ API).
        
        Parameters:
        -----------
        admin_id : str
            ID của admin đã kích hoạt quá trình huấn luyện
        db : Session, optional
            Session database hiện có (nếu được gọi từ API controller)
        """
        should_close_db = False
        if db is None:
            db = SessionLocal()
            should_close_db = True
        
        # Tạo bản ghi lịch sử huấn luyện
        history_repo = TrainingHistoryRepository(db)
        history = history_repo.create_training_job(triggered_by=f"MANUAL_ADMIN_{admin_id}")
        
        try:
            start_time = time.time()
            logger.info(f"=== BẮT ĐẦU QUÁ TRÌNH HUẤN LUYỆN MÔ HÌNH THỦ CÔNG (Admin ID: {admin_id}) ===")
            
            # 1. Tải dữ liệu
            data_loader = DataLoader(db)
            raw_data = data_loader.get_interaction_data()
            
            # 2. Tiền xử lý dữ liệu
            preprocessor = DataPreprocessor()
            processed_data = preprocessor.process(raw_data)
            
            # 3. Huấn luyện mô hình
            trainer = MatrixFactorizationTrainer(n_factors=100, n_iterations=20)
            model_result = trainer.train(processed_data)
            
            # 4. Đánh giá mô hình
            evaluator = ModelEvaluator()
            evaluation_result = evaluator.evaluate(model_result, processed_data)
            
            # 5. Lưu kết quả
            product_similarity_repo = ProductSimilarityRepository(db)
            user_recommendation_repo = UserRecommendationRepository(db)
            result_writer = RecommendationResultWriter(
                product_similarity_repo, user_recommendation_repo
            )
            result_writer.calculate_and_save_results(model_result)
            
            # Cập nhật bản ghi lịch sử huấn luyện thành công
            history_repo.update_training_job(
                history_id=history.history_id,
                status="SUCCESS",
                message=f"Completed successfully. Evaluation: {evaluation_result}"
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"=== HOÀN THÀNH QUÁ TRÌNH HUẤN LUYỆN MÔ HÌNH THỦ CÔNG (thời gian: {execution_time:.2f} giây) ===")
            
            # Đóng DB session nếu tự tạo
            if should_close_db:
                db.close()
                
            # Trả về kết quả
            return {
                "success": True, 
                "message": "Hoàn thành quá trình huấn luyện thủ công",
                "history_id": history.history_id,
                "execution_time": execution_time
            }
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình huấn luyện thủ công: {str(e)}", exc_info=True)
            
            # Cập nhật bản ghi lịch sử huấn luyện thất bại
            history_repo.update_training_job(
                history_id=history.history_id,
                status="FAILED",
                message=str(e)
            )
            
            if should_close_db:
                try:
                    db.close()
                except:
                    pass
                    
            return {
                "success": False, 
                "error": str(e),
                "history_id": history.history_id
            }