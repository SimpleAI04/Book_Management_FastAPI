from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.SQLALACHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    if settings.SQLALACHEMY_DATABASE_URL.startswith("sqlite")
    else {},
)

SeesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
