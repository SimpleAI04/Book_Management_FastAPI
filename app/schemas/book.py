from pydantic import BaseModel
from datetime import datetime

from app.schemas.author import Author
from app.schemas.category import Category


class BookBase(BaseModel):
    title: str
    description: str | None = None
    published_year: int
    author_id: int
    category_id: int


class BookCreate(BookBase):
    """Schema for create book"""

    pass


class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    published_year: int | None = None
    author_id: int | None = None
    category_id: int | None = None
    cover_image: str | None = None


class BookDBBase(BookBase):
    id: int
    title: str | None = None
    description: str | None = None
    published_year: int | None = None
    author_id: int | None = None
    category_id: int | None = None
    cover_image: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Book(BookDBBase):
    author: Author
    category: Category
