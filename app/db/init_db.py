from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.recommendations.training.job import TrainingJob
from app.db.base import engine, SessionLocal
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tạo scheduler và đăng ký job huấn luyện
scheduler = BackgroundScheduler()

def init_scheduler():
    """Khởi tạo scheduler cho việc huấn luyện mô hình định kỳ"""
    
    if not scheduler.running:
        # Cấu hình job huấn luyện mô hình chạy hàng ngày vào giờ đã cấu hình (mặc định: 1 giờ sáng)
        scheduler.add_job(
            TrainingJob.run,
            trigger=CronTrigger(hour=settings.TRAINING_HOUR),
            id='training_job',
            name='Huấn luyện mô hình gợi ý',
            replace_existing=True
        )
        
        # Khởi động scheduler
        scheduler.start()
        logger.info(f"Scheduler đã được khởi tạo và sẽ chạy huấn luyện vào lúc {settings.TRAINING_HOUR}:00 mỗi ngày")
    
    return scheduler

def create_first_admin():
    """
    Tạo tài khoản admin đầu tiên nếu chưa tồn tại trong hệ thống
    """
    try:
        # Tạo session
        db = SessionLocal()
        
        # Kiểm tra xem đã có admin nào chưa
        user_repository = UserRepository(db)
        admin_email = settings.FIRST_ADMIN_EMAIL
        
        if not user_repository.get_by_email(admin_email):
            # Tạo admin đầu tiên
            user_service = UserService(db)
            admin_data = {
                "email": admin_email,
                "password": settings.FIRST_ADMIN_PASSWORD,
                "full_name": "Admin", # Changed from "name" to "full_name"
                "is_admin": True
            }
            
            # Sử dụng Pydantic model để tạo user qua service
            from app.api.schemas.user import UserCreate
            user_create = UserCreate(**admin_data)
            user_service.create_user(user_create)
            
            logger.info(f"Đã tạo tài khoản admin đầu tiên với email: {admin_email}")
        
    except Exception as e:
        logger.error(f"Lỗi khi tạo tài khoản admin đầu tiên: {e}")
    
    finally:
        if 'db' in locals():
            db.close()