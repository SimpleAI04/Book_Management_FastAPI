from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    """Schema for create author"""

    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None


class AuthorDBBase(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class Author(AuthorDBBase):
    """schema return for client"""
