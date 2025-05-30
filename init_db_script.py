"""
Database initialization script.
This script creates the database if it doesn't exist and sets up all tables.
"""
import sys
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError

# Add the parent directory to sys.path to allow importing from the app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.base import Base, engine
from app.models import user, product, order, interaction, recommendation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Initialize the database with all tables.
    """
    try:
        # Extract the database connection URL without the database name
        db_url_parts = settings.DATABASE_URI.split('/')
        server_url = '/'.join(db_url_parts[:-1])
        db_name = db_url_parts[-1]
        
        # Create a connection to the server (without specifying a database)
        server_engine = create_engine(f"{server_url}/")
        
        # Create the database if it doesn't exist
        if not database_exists(settings.DATABASE_URI):
            try:
                with server_engine.connect() as conn:
                    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
                    logger.info(f"Database '{db_name}' created successfully!")
            except SQLAlchemyError as e:
                # Try creating through SQLAlchemy utils if the direct SQL fails
                create_database(settings.DATABASE_URI)
                logger.info(f"Database '{db_name}' created through SQLAlchemy-Utils!")
                
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # Close connections
        server_engine.dispose()
        engine.dispose()
        
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    logger.info("Initializing database...")
    success = init_db()
    if success:
        logger.info("Database initialization completed successfully!")
    else:
        logger.error("Database initialization failed!")
        sys.exit(1)