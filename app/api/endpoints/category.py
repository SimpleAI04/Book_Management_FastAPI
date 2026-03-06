from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import models
from app.schemas.category import Category, CategotyCreate, CategoryUpdate
from app.api.dependency import get_db

router = APIRouter()


@router.get("/", response_model=List[Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list categories use skip/limit
    """
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get category detail
    """
    category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return category


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategotyCreate, db: Session = Depends(get_db)):
    """
    Create new category
    """

    existing_category = (
        db.query(models.Category).filter(models.Category.name == category.name).first()
    )
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists"
        )

    category = models.Category(name=category.name, description=category.description)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.put(
    "/update/{category_id}", response_model=Category, status_code=status.HTTP_200_OK
)
def update_category(
    category_id: int, category_up: CategoryUpdate, db: Session = Depends(get_db)
):
    """
    Update category
    """

    category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if category_up.name is not None:
        existing_name = (
            db.query(models.Category)
            .filter(models.Category.name == category_up.name)
            .first()
        )
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another category with this name already exits",
            )
        category.name = category_up.name

    if category_up.description is not None:
        category.description = category_up.description

    db.commit()
    db.refresh(category)
    return category


@router.delete("/delete/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete category
    """

    category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    db.delete(category)
    db.commit()
