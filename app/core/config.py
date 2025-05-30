import os
from typing import Any, Dict, Optional, List
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class Settings(BaseSettings):
    # Cấu hình ứng dụng
    APP_NAME: str = os.getenv("APP_NAME", "eCommerce AI")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Cấu hình cơ sở dữ liệu
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASS: str = os.getenv("DB_PASS", "")
    DB_NAME: str = os.getenv("DB_NAME", "ecom_ai")
    DATABASE_URI: Optional[str] = None
    
    # Cấu hình JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # Adding the missing JWT algorithm
    
    # Cấu hình Admin đầu tiên
    FIRST_ADMIN_EMAIL: str = os.getenv("FIRST_ADMIN_EMAIL", "admin@example.com")
    FIRST_ADMIN_PASSWORD: str = os.getenv("FIRST_ADMIN_PASSWORD", "admin123")
    
    # Training configuration
    TRAINING_HOUR: int = int(os.getenv("TRAINING_HOUR", "1"))  # Default to 1 AM
    
    # CORS configuration
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
            
        return f"mysql+pymysql://{info.data.get('DB_USER')}:{info.data.get('DB_PASS')}@{info.data.get('DB_HOST')}:{info.data.get('DB_PORT')}/{info.data.get('DB_NAME')}"

settings = Settings()