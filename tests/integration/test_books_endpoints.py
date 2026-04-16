"""Integration tests for books endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Book


class TestBooksEndpoints:
    """Integration tests for book endpoints."""
    
    def test_create_book(self, client: TestClient):
        """Test creating a book via API."""
        response = client.post(
            "/books/",
            json={
                "isbn": "978-0-596-00712-6",
                "title": "Learning Python",
                "author": "Mark Lutz",
                "description": "A guide",
                "total_copies": 3
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Learning Python"
        assert data["available_copies"] == 3
    
    def test_create_book_duplicate_isbn(self, client: TestClient, sample_book: Book):
        """Test creating book with duplicate ISBN."""
        response = client.post(
            "/books/",
            json={
                "isbn": sample_book.isbn,
                "title": "Different Title",
                "author": "Different Author",
                "total_copies": 1
            }
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_list_books(self, client: TestClient, sample_book: Book):
        """Test listing all books."""
        response = client.get("/books/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_list_books_pagination(self, client: TestClient, multiple_books):
        """Test list books with pagination."""
        response = client.get("/books/?skip=0&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
    
    def test_search_books(self, client: TestClient, sample_book: Book):
        """Test searching books."""
        response = client.get("/books/search?q=Learning")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(book["id"] == sample_book.id for book in data)
    
    def test_get_book(self, client: TestClient, sample_book: Book):
        """Test getting a specific book."""
        response = client.get(f"/books/{sample_book.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_book.id
        assert data["title"] == sample_book.title
    
    def test_get_book_not_found(self, client: TestClient):
        """Test getting non-existent book."""
        response = client.get("/books/999")
        
        assert response.status_code == 404
    
    def test_update_book(self, client: TestClient, sample_book: Book):
        """Test updating a book."""
        response = client.put(
            f"/books/{sample_book.id}",
            json={
                "title": "Updated Title",
                "total_copies": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["total_copies"] == 5
    
    def test_delete_book(self, client: TestClient, sample_book: Book):
        """Test deleting a book."""
        response = client.delete(f"/books/{sample_book.id}")
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/books/{sample_book.id}")
        assert get_response.status_code == 404
    
    def test_get_available_books(self, client: TestClient, sample_book: Book):
        """Test listing only available books."""
        response = client.get("/books/?available_only=true")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(book["available_copies"] > 0 for book in data)
