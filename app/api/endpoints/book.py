from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.api.dependency import get_db
from app import models
from app.schemas.book import Book, BookCreate, BookUpdate

router = APIRouter()


@router.get("/")
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    category_id: int | None = None,
    year: int | None = None,
    keyword: str | None = None,
    db: Session = Depends(get_db),
):
    """Get list of book, include filter

    - skip (int): Number of books to skip
    - limit (int): Number of books to return
    - author_id (int | None): Filter by author ID
    - category_id (int | None): Filter by category ID
    - year (int | None): Filter by year
    - keyword (str | None): Filter by keyword
    - db (Session): Database session
    """
    if author_id:
        result = db.query(models.Book).filter(models.Book.author_id == author_id)
        return result
    if category_id:
        result = db.query(models.Book).filter(models.Book.category_id == category_id)
        return result
    if year:
        result = db.query(models.Book).filter(models.Book.year == year)
        return result
    if keyword:
        result = db.query(models.Book).filter(models.Book.title.like(f"%{keyword}%"))
        return result

    result = db.query(models.Book).offset(skip).limit(limit).all()
    return result


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get category detail
    """
    res = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return res


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_cre: BookCreate, db: Session = Depends(get_db)):
    """
    Create new book
    """

    author = (
        db.query(models.Author).filter(models.Author.id == book_cre.author_id).first()
    )
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found"
        )

    category = (
        db.query(models.Category)
        .filter(models.Category.id == book_cre.category_id)
        .first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )

    book = models.Book(
        title=book_cre.title,
        description=book_cre.description,
        published_year=book_cre.published_year,
        author_id=book_cre.author_id,
        category_id=book_cre.category_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


@router.put("/update/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
def update_category(book_id: int, book_up: BookUpdate, db: Session = Depends(get_db)):
    """
    Update category
    """

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if book_up.author_id:
        author = (
            db.query(models.Author)
            .filter(models.Author.id == book_up.author_id)
            .first()
        )
        if not author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found"
            )
        book.author_id = book_up.author_id

    if book_up.category_id:
        category = (
            db.query(models.Category)
            .filter(models.Category.id == book_up.category_id)
            .first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
            )
        book.category_id = book_up.category_id

    if book_up.title:
        book.title = book_up.title

    if book_up.description:
        book.description = book_up.description

    if book_up.published_year:
        book.published_year = book_up.published_year

    db.commit()
    db.refresh(book)
    return book


@router.delete("/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(book_id: int, db: Session = Depends(get_db)):
    """
    Delete category
    """

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    db.delete(book)
    db.commit()
