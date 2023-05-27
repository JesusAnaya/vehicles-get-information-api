from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from settings import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
