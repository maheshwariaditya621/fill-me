from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ⚠️ UPDATE THESE CREDENTIALS FOR YOUR MARIADB SERVER
# Format: mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
# Example: mysql+pymysql://root:password@localhost:3306/survey_db
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Babyaditya#007@localhost:3306/survey_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Handles extensive connection drops
    pool_recycle=3600    # Recycles connections every hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
