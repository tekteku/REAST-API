"""Router for book endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookDetailResponse

router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book"
)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book in the library."""
    repo = BookRepository(db)
    
    # Check if book with same ISBN already exists
    existing_book = repo.get_book_by_isbn(book.isbn)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ISBN {book.isbn} already exists"
        )
    
    return repo.create_book(book)


@router.get(
    "/",
    response_model=List[BookResponse],
    summary="List all books"
)
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    available_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get a list of all books in the library."""
    repo = BookRepository(db)
    
    if available_only:
        return repo.get_available_books(skip=skip, limit=limit)
    
    return repo.get_all_books(skip=skip, limit=limit)


@router.get(
    "/search",
    response_model=List[BookResponse],
    summary="Search books"
)
def search_books(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Search books by title, author, or ISBN."""
    repo = BookRepository(db)
    return repo.search_books(query=q, skip=skip, limit=limit)


@router.get(
    "/{book_id}",
    response_model=BookDetailResponse,
    summary="Get book details"
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get details of a specific book."""
    repo = BookRepository(db)
    book = repo.get_book(book_id)
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    return book


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update a book"
)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):
    """Update book information."""
    repo = BookRepository(db)
    book = repo.update_book(book_id, book_update)
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    return book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book"
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book from the library."""
    repo = BookRepository(db)
    
    if not repo.delete_book(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
