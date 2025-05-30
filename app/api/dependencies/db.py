from typing import Generator

from app.db.base import SessionLocal

def get_db() -> Generator:
    """
    Dependency để cung cấp database session cho route handlers.
    Sử dụng như một FastAPI dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()