from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.author import Author
from app.models.categoty import Category
from app.models.book import Book



