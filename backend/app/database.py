import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read from the environment so the same code runs both ways:
#   * in Docker, compose injects DATABASE_URL pointing at the `db` service host;
#   * for local dev (no Docker), it falls back to a localhost Postgres.
# The service name `db` vs `localhost` is THE classic compose bug — env keeps
# both worlds working without editing code.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/assistant"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()