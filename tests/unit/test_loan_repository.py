"""Unit tests for loan repository."""

import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Loan, Book, Member
from app.repositories.loan_repository import LoanRepository


class TestLoanRepository:
    """Test suite for LoanRepository."""
    
    def test_create_loan(self, db: Session, sample_book: Book, sample_member: Member):
        """Test creating a new loan."""
        repo = LoanRepository(db)
        due_date = datetime.now() + timedelta(days=14)
        
        loan = repo.create_loan(sample_book.id, sample_member.id, due_date)
        
        assert loan.id is not None
        assert loan.book_id == sample_book.id
        assert loan.member_id == sample_member.id
        assert loan.is_active is True
    
    def test_get_loan(self, db: Session, sample_loan: Loan):
        """Test retrieving a loan by ID."""
        repo = LoanRepository(db)
        loan = repo.get_loan(sample_loan.id)
        
        assert loan is not None
        assert loan.id == sample_loan.id
    
    def test_get_loan_not_found(self, db: Session):
        """Test retrieving a non-existent loan."""
        repo = LoanRepository(db)
        loan = repo.get_loan(999)
        
        assert loan is None
    
    def test_get_active_loan(self, db: Session, sample_loan: Loan):
        """Test retrieving active loan for book and member."""
        repo = LoanRepository(db)
        loan = repo.get_active_loan(sample_loan.book_id, sample_loan.member_id)
        
        assert loan is not None
        assert loan.is_active is True
    
    def test_get_member_active_loans(self, db: Session, sample_member: Member, sample_loan: Loan):
        """Test retrieving all active loans for a member."""
        repo = LoanRepository(db)
        loans = repo.get_member_active_loans(sample_member.id)
        
        assert len(loans) >= 1
        assert any(l.id == sample_loan.id for l in loans)
    
    def test_get_member_loan_count(self, db: Session, sample_member: Member, sample_loan: Loan):
        """Test getting count of active loans."""
        repo = LoanRepository(db)
        count = repo.get_member_loan_count(sample_member.id)
        
        assert count >= 1
    
    def test_get_all_loans(self, db: Session, sample_loan: Loan):
        """Test retrieving all loans."""
        repo = LoanRepository(db)
        loans = repo.get_all_loans()
        
        assert len(loans) >= 1
    
    def test_get_overdue_loans(self, db: Session, sample_loan: Loan):
        """Test retrieving overdue loans."""
        repo = LoanRepository(db)
        
        # Set due date to past
        sample_loan.due_date = datetime.now() - timedelta(days=1)
        db.commit()
        
        overdue = repo.get_overdue_loans()
        
        assert len(overdue) >= 1
        assert any(l.id == sample_loan.id for l in overdue)
    
    def test_return_book(self, db: Session, sample_loan: Loan):
        """Test returning a book."""
        repo = LoanRepository(db)
        returned_loan = repo.return_book(sample_loan.id)
        
        assert returned_loan.is_active is False
        assert returned_loan.returned_at is not None
    
    def test_get_loan_history(self, db: Session, sample_member: Member, sample_loan: Loan):
        """Test retrieving loan history for a member."""
        repo = LoanRepository(db)
        history = repo.get_loan_history(sample_member.id)
        
        assert len(history) >= 1
        assert any(l.id == sample_loan.id for l in history)
