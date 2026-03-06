from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategotyCreate(CategoryBase):
    """Schema for create category"""

    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class Category(CategoryDBBase):
    """schema return for client"""
    pass