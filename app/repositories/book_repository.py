"""Repository for book data access."""

from sqlalchemy.orm import Session
from app.models import Book
from app.schemas.book import BookCreate, BookUpdate
from typing import List, Optional


class BookRepository:
    """Repository for book database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_book(self, book_id: int) -> Optional[Book]:
        """Get a book by ID."""
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get all books with pagination."""
        return self.db.query(Book).offset(skip).limit(limit).all()
    
    def search_books(self, query: str, skip: int = 0, limit: int = 100) -> List[Book]:
        """Search books by title or author."""
        search_pattern = f"%{query}%"
        return self.db.query(Book).filter(
            (Book.title.ilike(search_pattern)) |
            (Book.author.ilike(search_pattern)) |
            (Book.isbn.ilike(search_pattern))
        ).offset(skip).limit(limit).all()
    
    def create_book(self, book: BookCreate) -> Book:
        """Create a new book."""
        db_book = Book(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            description=book.description,
            total_copies=book.total_copies,
            available_copies=book.total_copies
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        """Update a book."""
        db_book = self.get_book(book_id)
        if not db_book:
            return None
        
        update_data = book_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def delete_book(self, book_id: int) -> bool:
        """Delete a book."""
        db_book = self.get_book(book_id)
        if not db_book:
            return False
        
        self.db.delete(db_book)
        self.db.commit()
        return True
    
    def get_available_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get only available books."""
        return self.db.query(Book).filter(
            Book.available_copies > 0
        ).offset(skip).limit(limit).all()
