# database.py
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager

load_dotenv()

# Create the engine
engine = create_engine(os.getenv("POSTGRES_URL"), echo=True)

# Create all tables (optional, usually at app startup)
def init_db():
    from Entities.SQL.Models import models  # Import your models here
    SQLModel.metadata.create_all(engine)

# Dependency for FastAPI
def get_session():
    with Session(engine) as session:
        yield session
