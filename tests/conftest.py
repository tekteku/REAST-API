"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.database import Base, get_db
from app.main import app
from app.models import Book, Member, Loan

# Use in-memory SQLite database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_book(db: Session):
    """Create a sample book for testing."""
    book = Book(
        isbn="978-0-596-00712-6",
        title="Learning Python",
        author="Mark Lutz",
        description="A comprehensive guide to Python programming",
        total_copies=3,
        available_copies=3
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@pytest.fixture
def sample_member(db: Session):
    """Create a sample member for testing."""
    member = Member(
        name="John Doe",
        email="john@example.com",
        phone="+1-555-0123",
        address="123 Main St, Anytown, USA",
        is_active=True
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@pytest.fixture
def sample_loan(db: Session, sample_book: Book, sample_member: Member):
    """Create a sample loan for testing."""
    loan = Loan(
        book_id=sample_book.id,
        member_id=sample_member.id,
        due_date=datetime.now() + timedelta(days=14),
        is_active=True
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@pytest.fixture
def multiple_books(db: Session):
    """Create multiple sample books."""
    books = [
        Book(
            isbn=f"978-0-596-0071{i}",
            title=f"Python Book {i}",
            author=f"Author {i}",
            total_copies=2,
            available_copies=2
        )
        for i in range(5)
    ]
    db.add_all(books)
    db.commit()
    return books
