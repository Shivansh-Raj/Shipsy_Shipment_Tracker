from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Initializes the database engine
engine = create_engine(settings.DATABASE_URL)
# Create a session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    """
        Yields a session and closes it after used.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
