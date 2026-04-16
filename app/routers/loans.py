"""Router for loan endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate, LoanResponse, LoanDetailResponse

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post(
    "/borrow",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Borrow a book"
)
def borrow_book(loan: LoanCreate, db: Session = Depends(get_db)):
    """
    Borrow a book for a member.
    
    Business rules:
    - Member must be active
    - Book must be available
    - Member cannot have more than 3 active loans
    - Member cannot borrow the same book twice
    """
    service = LoanService(db)
    return service.borrow_book(
        book_id=loan.book_id,
        member_id=loan.member_id,
        loan_duration_days=loan.loan_duration_days
    )


@router.post(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Return a borrowed book"
)
def return_book(
    loan_id: int = Path(..., ge=1, description="Loan ID"),
    db: Session = Depends(get_db)
):
    """Return a borrowed book and close the loan."""
    service = LoanService(db)
    return service.return_book(loan_id)


@router.get(
    "/",
    response_model=List[LoanResponse],
    summary="List all loans"
)
def list_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get a list of all loans (active and returned)."""
    repo = LoanRepository(db)
    return repo.get_all_loans(skip=skip, limit=limit)


@router.get(
    "/member/{member_id}",
    response_model=List[LoanResponse],
    summary="Get member's active loans"
)
def get_member_active_loans(
    member_id: int = Path(..., ge=1, description="Member ID"),
    db: Session = Depends(get_db)
):
    """Get all active loans for a specific member."""
    service = LoanService(db)
    return service.get_member_active_loans(member_id)


@router.get(
    "/member/{member_id}/history",
    response_model=List[LoanResponse],
    summary="Get member's loan history"
)
def get_member_loan_history(
    member_id: int = Path(..., ge=1, description="Member ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get complete loan history for a member."""
    repo = LoanRepository(db)
    return repo.get_loan_history(member_id, skip=skip, limit=limit)


@router.get(
    "/overdue",
    response_model=List[LoanResponse],
    summary="Get overdue loans"
)
def get_overdue_loans(db: Session = Depends(get_db)):
    """Get all overdue loans."""
    service = LoanService(db)
    return service.get_overdue_loans()
