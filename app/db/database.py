import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from sqlalchemy.orm import declarative_base
Base = declarative_base()

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment")
# synchronous engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
