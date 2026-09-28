from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.core.config import (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
)


DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME,
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()