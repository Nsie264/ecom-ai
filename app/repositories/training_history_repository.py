from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.models.recommendation import TrainingHistory

class TrainingHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_training_job(self, triggered_by: str) -> TrainingHistory:
        """Tạo một bản ghi mới cho việc huấn luyện với trạng thái RUNNING"""
        history = TrainingHistory(
            start_time=datetime.now(),
            status="RUNNING",
            triggered_by=triggered_by
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def update_training_job(self, history_id: int, status: str, message: Optional[str] = None) -> TrainingHistory:
        """Cập nhật kết quả của một job huấn luyện"""
        history = self.db.query(TrainingHistory).filter(TrainingHistory.history_id == history_id).first()
        if history:
            history.end_time = datetime.now()
            history.status = status
            if message:
                history.message = message
            self.db.commit()
            self.db.refresh(history)
        return history

    def get_training_history(self, limit: int = 20) -> List[TrainingHistory]:
        """Lấy lịch sử huấn luyện, sắp xếp theo thời gian gần nhất"""
        return self.db.query(TrainingHistory).order_by(desc(TrainingHistory.start_time)).limit(limit).all()

    def get_training_job(self, history_id: int) -> Optional[TrainingHistory]:
        """Lấy thông tin về một job huấn luyện cụ thể"""
        return self.db.query(TrainingHistory).filter(TrainingHistory.history_id == history_id).first()