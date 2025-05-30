"""
Script to initialize the database completely, including creating the database,
setting up all tables, and creating the admin user.
"""
import sys
import os
import logging
from sqlalchemy_utils import database_exists, create_database

# Add the parent directory to sys.path to allow importing from the app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_full_db():
    """
    Initialize the complete database with models and the first admin user
    """
    from app.core.config import settings
    from app.db.base import Base, engine, SessionLocal
    
    try:
        # Import all models to ensure they're registered with SQLAlchemy
        from app.models.user import User, UserAddress
        from app.models.product import Product, ProductImage, Category, Tag, product_tag
        from app.models.order import Order, OrderItem
        from app.models.interaction import ViewHistory, SearchHistory, Rating, CartItem
        from app.models.recommendation import ProductSimilarity, UserRecommendation, TrainingHistory
        
        logger.info("Creating database if it doesn't exist...")
        # Create database if it doesn't exist
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info(f"Database '{engine.url.database}' created.")
        
        logger.info("Creating all database tables...")
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # Create the admin user
        logger.info("Creating admin user if it doesn't exist...")
        db = SessionLocal()
        try:
            from app.repositories.user_repository import UserRepository
            from app.services.user_service import UserService
            
            user_repository = UserRepository(db)
            admin_email = settings.FIRST_ADMIN_EMAIL
            
            if not user_repository.get_by_email(admin_email):
                user_service = UserService(db)
                admin_data = {
                    "email": admin_email,
                    "password": settings.FIRST_ADMIN_PASSWORD,
                    "full_name": "Admin", 
                    "is_admin": True
                }
                
                from app.api.schemas.user import UserCreate
                user_create = UserCreate(**admin_data)
                user = user_service.create_user(user_create)
                logger.info(f"Admin user created with ID: {user.user_id}")
            else:
                logger.info("Admin user already exists, skipping creation")
                
        finally:
            db.close()
            
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_full_db()
    if success:
        logger.info("Database initialization completed successfully!")
    else:
        logger.error("Database initialization failed!")
        sys.exit(1)