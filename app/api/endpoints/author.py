from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.dependency import get_db
from app import models
from app.schemas.author import AuthorCreate, AuthorUpdate, Author
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Author])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list authors use skip/limit
    """
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors


@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Get author detail
    """
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    return author


@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Create new author
    """

    existing_author = (
        db.query(models.Author).filter(models.Author.name == author.name).first()
    )
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists"
        )

    author_create = models.Author(name=author.name, bio=author.bio)

    db.add(author_create)
    db.commit()
    db.refresh(author_create)

    return author_create


@router.put(
    "/update/{author_id}", response_model=Author, status_code=status.HTTP_200_OK
)
def update_author(
    author_id: int, author_up: AuthorUpdate, db: Session = Depends(get_db)
):
    """
    Update author
    """

    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    if author_up.name is not None:
        existing_name = (
            db.query(models.Author).filter(models.Author.name == author_up.name).first()
        )
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another author with this name already exits",
            )
        author.name = author_up.name

    if author_up.bio is not None:
        author.bio = author_up.bio

    db.commit()
    db.refresh(author)
    return author


@router.delete("/delete/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Delete author
    """

    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    db.delete(author)
    db.commit()
