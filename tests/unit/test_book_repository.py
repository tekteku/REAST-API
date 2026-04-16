"""Unit tests for book repository."""

import pytest
from sqlalchemy.orm import Session
from app.models import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate


class TestBookRepository:
    """Test suite for BookRepository."""
    
    def test_create_book(self, db: Session):
        """Test creating a new book."""
        repo = BookRepository(db)
        book_data = BookCreate(
            isbn="978-0-596-00712-6",
            title="Learning Python",
            author="Mark Lutz",
            description="A guide to Python",
            total_copies=3
        )
        
        book = repo.create_book(book_data)
        
        assert book.id is not None
        assert book.isbn == "978-0-596-00712-6"
        assert book.title == "Learning Python"
        assert book.total_copies == 3
        assert book.available_copies == 3
    
    def test_get_book(self, db: Session, sample_book: Book):
        """Test retrieving a book by ID."""
        repo = BookRepository(db)
        book = repo.get_book(sample_book.id)
        
        assert book is not None
        assert book.id == sample_book.id
        assert book.title == sample_book.title
    
    def test_get_book_not_found(self, db: Session):
        """Test retrieving a non-existent book."""
        repo = BookRepository(db)
        book = repo.get_book(999)
        
        assert book is None
    
    def test_get_book_by_isbn(self, db: Session, sample_book: Book):
        """Test retrieving a book by ISBN."""
        repo = BookRepository(db)
        book = repo.get_book_by_isbn(sample_book.isbn)
        
        assert book is not None
        assert book.isbn == sample_book.isbn
    
    def test_get_all_books(self, db: Session, multiple_books):
        """Test retrieving all books."""
        repo = BookRepository(db)
        books = repo.get_all_books()
        
        assert len(books) == 5
    
    def test_get_all_books_with_pagination(self, db: Session, multiple_books):
        """Test retrieving books with pagination."""
        repo = BookRepository(db)
        books = repo.get_all_books(skip=0, limit=2)
        
        assert len(books) == 2
    
    def test_search_books_by_title(self, db: Session, sample_book: Book):
        """Test searching books by title."""
        repo = BookRepository(db)
        books = repo.search_books("Learning")
        
        assert len(books) >= 1
        assert any(book.id == sample_book.id for book in books)
    
    def test_search_books_by_author(self, db: Session, sample_book: Book):
        """Test searching books by author."""
        repo = BookRepository(db)
        books = repo.search_books("Lutz")
        
        assert len(books) >= 1
        assert any(book.id == sample_book.id for book in books)
    
    def test_update_book(self, db: Session, sample_book: Book):
        """Test updating a book."""
        repo = BookRepository(db)
        update_data = BookUpdate(
            title="Updated Python Learning",
            total_copies=5
        )
        
        updated_book = repo.update_book(sample_book.id, update_data)
        
        assert updated_book.title == "Updated Python Learning"
        assert updated_book.total_copies == 5
    
    def test_delete_book(self, db: Session, sample_book: Book):
        """Test deleting a book."""
        repo = BookRepository(db)
        result = repo.delete_book(sample_book.id)
        
        assert result is True
        assert repo.get_book(sample_book.id) is None
    
    def test_get_available_books(self, db: Session, sample_book: Book):
        """Test retrieving available books."""
        repo = BookRepository(db)
        
        # Mark some copies as unavailable
        sample_book.available_copies = 1
        db.commit()
        
        available_books = repo.get_available_books()
        
        assert len(available_books) >= 1
        assert any(book.id == sample_book.id for book in available_books)
