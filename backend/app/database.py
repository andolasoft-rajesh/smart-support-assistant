from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:Barsa%40123@localhost:5433/smart-support-assistant"


engine = create_engine(
    DATABASE_URL
)
print("DATABASE URL:", DATABASE_URL)
print("ENGINE:", engine)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()