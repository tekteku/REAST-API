"""Unit tests for loan service business logic."""

import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta
from app.models import Book, Member, Loan
from app.services.loan_service import LoanService


class TestLoanService:
    """Test suite for LoanService."""
    
    def test_borrow_book_success(self, db: Session, sample_book: Book, sample_member: Member):
        """Test successfully borrowing a book."""
        service = LoanService(db)
        
        loan = service.borrow_book(sample_book.id, sample_member.id, 14)
        
        assert loan.id is not None
        assert loan.book_id == sample_book.id
        assert loan.member_id == sample_member.id
        assert loan.is_active is True
        
        # Check book availability decreased
        db.refresh(sample_book)
        assert sample_book.available_copies == 2
    
    def test_borrow_book_member_not_found(self, db: Session, sample_book: Book):
        """Test borrowing book with non-existent member."""
        service = LoanService(db)
        
        with pytest.raises(HTTPException) as exc:
            service.borrow_book(sample_book.id, 999, 14)
        
        assert exc.value.status_code == 404
    
    def test_borrow_book_book_not_found(self, db: Session, sample_member: Member):
        """Test borrowing non-existent book."""
        service = LoanService(db)
        
        with pytest.raises(HTTPException) as exc:
            service.borrow_book(999, sample_member.id, 14)
        
        assert exc.value.status_code == 404
    
    def test_borrow_book_no_availability(self, db: Session, sample_book: Book, sample_member: Member):
        """Test borrowing when book has no available copies."""
        service = LoanService(db)
        
        sample_book.available_copies = 0
        db.commit()
        
        with pytest.raises(HTTPException) as exc:
            service.borrow_book(sample_book.id, sample_member.id, 14)
        
        assert exc.value.status_code == 400
    
    def test_borrow_book_member_inactive(self, db: Session, sample_book: Book, sample_member: Member):
        """Test borrowing when member is inactive."""
        service = LoanService(db)
        
        sample_member.is_active = False
        db.commit()
        
        with pytest.raises(HTTPException) as exc:
            service.borrow_book(sample_book.id, sample_member.id, 14)
        
        assert exc.value.status_code == 400
    
    def test_borrow_book_max_loans_exceeded(self, db: Session, sample_book: Book, sample_member: Member):
        """Test borrowing when member has reached max loans."""
        service = LoanService(db)
        
        # Create 3 loans (max limit)
        for i in range(3):
            book = Book(
                isbn=f"978-0-596-0071{i}",
                title=f"Book {i}",
                author=f"Author {i}",
                total_copies=1,
                available_copies=1
            )
            db.add(book)
            db.commit()
            
            loan = Loan(
                book_id=book.id,
                member_id=sample_member.id,
                due_date=datetime.now() + timedelta(days=14),
                is_active=True
            )
            db.add(loan)
            db.commit()
        
        # Try to borrow 4th book
        book4 = Book(
            isbn="978-0-596-00714",
            title="Book 4",
            author="Author 4",
            total_copies=1,
            available_copies=1
        )
        db.add(book4)
        db.commit()
        
        with pytest.raises(HTTPException) as exc:
            service.borrow_book(book4.id, sample_member.id, 14)
        
        assert exc.value.status_code == 400
        assert "maximum loans limit" in exc.value.detail
    
    def test_borrow_same_book_twice(self, db: Session, sample_book: Book, sample_member: Member):
        """Test member cannot borrow same book twice."""
        service = LoanService(db)
        
        # Borrow once
        service.borrow_book(sample_book.id, sample_member.id, 14)
        
        # Try to borrow again
        with pytest.raises(HTTPException) as exc:
            service.borrow_book(sample_book.id, sample_member.id, 14)
        
        assert exc.value.status_code == 400
        assert "already has this book borrowed" in exc.value.detail
    
    def test_return_book_success(self, db: Session, sample_loan: Loan, sample_book: Book):
        """Test successfully returning a book."""
        service = LoanService(db)
        
        # Reduce available copies first
        sample_book.available_copies -= 1
        db.commit()
        
        returned_loan = service.return_book(sample_loan.id)
        
        assert returned_loan.is_active is False
        assert returned_loan.returned_at is not None
        
        # Check book availability increased
        db.refresh(sample_book)
        assert sample_book.available_copies == 3
    
    def test_return_book_not_found(self, db: Session):
        """Test returning non-existent loan."""
        service = LoanService(db)
        
        with pytest.raises(HTTPException) as exc:
            service.return_book(999)
        
        assert exc.value.status_code == 404
    
    def test_return_book_already_returned(self, db: Session, sample_loan: Loan):
        """Test returning already returned book."""
        service = LoanService(db)
        
        sample_loan.is_active = False
        sample_loan.returned_at = datetime.now()
        db.commit()
        
        with pytest.raises(HTTPException) as exc:
            service.return_book(sample_loan.id)
        
        assert exc.value.status_code == 400
    
    def test_calculate_fine_no_overdue(self, db: Session, sample_loan: Loan):
        """Test fine calculation for on-time return."""
        service = LoanService(db)
        
        # Set due date in future
        sample_loan.due_date = datetime.now() + timedelta(days=5)
        db.commit()
        
        fine = service.calculate_fine(sample_loan)
        
        assert fine == 0.0
    
    def test_calculate_fine_with_overdue(self, db: Session, sample_loan: Loan):
        """Test fine calculation for overdue return."""
        service = LoanService(db)
        
        # Set due date in past
        sample_loan.due_date = datetime.now() - timedelta(days=3)
        sample_loan.returned_at = datetime.now()
        db.commit()
        
        fine = service.calculate_fine(sample_loan)
        
        assert fine >= 3.0  # At least $3 for 3 days overdue
