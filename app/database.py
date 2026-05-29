from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5433/research_db"
)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(
        text(
            "CREATE EXTENSION IF NOT EXISTS vector"
        )
    )
    conn.commit()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
