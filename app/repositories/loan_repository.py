"""Repository for loan data access."""

from sqlalchemy.orm import Session
from app.models import Loan, Book, Member
from typing import List, Optional
from datetime import datetime


class LoanRepository:
    """Repository for loan database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_loan(self, loan_id: int) -> Optional[Loan]:
        """Get a loan by ID."""
        return self.db.query(Loan).filter(Loan.id == loan_id).first()
    
    def get_active_loan(self, book_id: int, member_id: int) -> Optional[Loan]:
        """Get active loan for a book and member."""
        return self.db.query(Loan).filter(
            Loan.book_id == book_id,
            Loan.member_id == member_id,
            Loan.is_active == True
        ).first()
    
    def get_member_active_loans(self, member_id: int) -> List[Loan]:
        """Get all active loans for a member."""
        return self.db.query(Loan).filter(
            Loan.member_id == member_id,
            Loan.is_active == True
        ).all()
    
    def get_member_loan_count(self, member_id: int) -> int:
        """Get count of active loans for a member."""
        return self.db.query(Loan).filter(
            Loan.member_id == member_id,
            Loan.is_active == True
        ).count()
    
    def get_all_loans(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get all loans with pagination."""
        return self.db.query(Loan).offset(skip).limit(limit).all()
    
    def get_overdue_loans(self) -> List[Loan]:
        """Get all overdue loans."""
        return self.db.query(Loan).filter(
            Loan.due_date < datetime.now(),
            Loan.is_active == True
        ).all()
    
    def create_loan(self, book_id: int, member_id: int, due_date: datetime) -> Loan:
        """Create a new loan."""
        db_loan = Loan(
            book_id=book_id,
            member_id=member_id,
            due_date=due_date
        )
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan
    
    def return_book(self, loan_id: int) -> Optional[Loan]:
        """Return a book (close the loan)."""
        db_loan = self.get_loan(loan_id)
        if not db_loan or not db_loan.is_active:
            return None
        
        db_loan.returned_at = datetime.now()
        db_loan.is_active = False
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan
    
    def get_loan_history(self, member_id: int, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get loan history for a member."""
        return self.db.query(Loan).filter(
            Loan.member_id == member_id
        ).offset(skip).limit(limit).all()
