from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Tạo engine kết nối đến cơ sở dữ liệu MySQL
engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)

# Tạo SessionLocal để mỗi request sẽ có một session riêng
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo Base class cho tất cả các model
Base = declarative_base()

# Utility function để lấy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()