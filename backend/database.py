import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv("clave-agent.env")

DATABASE_URL = os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    pass


if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
else:
    engine = None
    SessionLocal = None


def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL no está configurada en clave-agent.env"
        )

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()