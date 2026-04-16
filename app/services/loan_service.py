"""Service layer for loan business logic."""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.repositories.member_repository import MemberRepository
from app.models import Loan, Book, Member
from typing import Optional, Tuple
from fastapi import HTTPException, status


class LoanService:
    """Service for loan business operations."""
    
    MAX_LOANS_PER_MEMBER = 3
    DEFAULT_LOAN_DURATION_DAYS = 14
    
    def __init__(self, db: Session):
        self.db = db
        self.loan_repo = LoanRepository(db)
        self.book_repo = BookRepository(db)
        self.member_repo = MemberRepository(db)
    
    def borrow_book(
        self,
        book_id: int,
        member_id: int,
        loan_duration_days: int = DEFAULT_LOAN_DURATION_DAYS
    ) -> Loan:
        """
        Borrow a book for a member (business logic layer).
        
        Validates:
        - Member exists and is active
        - Book exists
        - Book has available copies
        - Member hasn't reached max loans
        """
        # Validate member exists and is active
        member = self.member_repo.get_member(member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Member with ID {member_id} not found"
            )
        
        if not member.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is inactive"
            )
        
        # Validate book exists
        book = self.book_repo.get_book(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        # Check book availability
        if book.available_copies <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book '{book.title}' is not available"
            )
        
        # Check if member already has this book borrowed
        existing_loan = self.loan_repo.get_active_loan(book_id, member_id)
        if existing_loan:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Member already has this book borrowed"
            )
        
        # Check member's loan limit
        current_loans = self.loan_repo.get_member_loan_count(member_id)
        if current_loans >= self.MAX_LOANS_PER_MEMBER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Member has reached maximum loans limit ({self.MAX_LOANS_PER_MEMBER})"
            )
        
        # Create loan
        due_date = datetime.now() + timedelta(days=loan_duration_days)
        loan = self.loan_repo.create_loan(book_id, member_id, due_date)
        
        # Update book availability
        book.available_copies -= 1
        self.db.commit()
        
        return loan
    
    def return_book(self, loan_id: int) -> Loan:
        """
        Return a borrowed book (close the loan and update availability).
        """
        loan = self.loan_repo.get_loan(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with ID {loan_id} not found"
            )
        
        if not loan.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This book has already been returned"
            )
        
        # Return the book
        returned_loan = self.loan_repo.return_book(loan_id)
        
        # Update book availability
        book = self.book_repo.get_book(loan.book_id)
        if book:
            book.available_copies += 1
            self.db.commit()
        
        return returned_loan
    
    def get_member_active_loans(self, member_id: int) -> list:
        """Get all active loans for a member."""
        member = self.member_repo.get_member(member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Member with ID {member_id} not found"
            )
        
        return self.loan_repo.get_member_active_loans(member_id)
    
    def get_overdue_loans(self) -> list:
        """Get all overdue loans."""
        return self.loan_repo.get_overdue_loans()
    
    def calculate_fine(self, loan: Loan) -> float:
        """Calculate fine for a late book (simple calculation)."""
        if loan.returned_at is None:
            return_date = datetime.now()
        else:
            return_date = loan.returned_at
        
        days_overdue = (return_date - loan.due_date).days
        if days_overdue <= 0:
            return 0.0
        
        # $1 per day overdue
        return float(days_overdue)
