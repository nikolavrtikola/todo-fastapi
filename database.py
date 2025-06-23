import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test123!@localhost/ToDoDatabase"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://","postgresql://",1)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()


