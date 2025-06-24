from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

SQLITE_URL = "sqlite:///./intranet.db"
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)
