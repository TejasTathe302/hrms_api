from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://hrms:rTqCDIwq2OP1QY8GkCqztTn38Tvmf11s@dpg-d6q4kcnkijhs73dsbo5g-a.oregon-postgres.render.com/hrms_lazx"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
