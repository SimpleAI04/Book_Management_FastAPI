from typing import Generator
from app.db.session import SeesionLocal

def get_db() -> Generator:
    db = SeesionLocal()
    try:
        yield db
    finally:
        db.close()