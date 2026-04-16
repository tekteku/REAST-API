"""Pydantic schemas for Loan endpoints."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timedelta


class LoanBase(BaseModel):
    """Base schema for loan data."""
    
    book_id: int = Field(..., ge=1)
    member_id: int = Field(..., ge=1)


class LoanCreate(LoanBase):
    """Schema for creating a new loan (borrowing a book)."""
    
    loan_duration_days: int = Field(default=14, ge=1, le=60, description="Loan duration in days")


class LoanReturn(BaseModel):
    """Schema for returning a book."""
    
    pass


class LoanResponse(LoanBase):
    """Schema for loan responses."""
    
    id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LoanDetailResponse(LoanResponse):
    """Detailed loan response with book and member info."""
    
    book: "BookSummary"
    member: "MemberSummary"


class BookSummary(BaseModel):
    """Summary of book info in loan response."""
    
    id: int
    title: str
    author: str
    isbn: str
    
    class Config:
        from_attributes = True


class MemberSummary(BaseModel):
    """Summary of member info in loan response."""
    
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


# Import for forward references
from app.schemas.book import BookResponse
from app.schemas.member import MemberResponse
