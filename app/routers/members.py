"""Router for member endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.repositories.member_repository import MemberRepository
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse, MemberDetailResponse

router = APIRouter(prefix="/members", tags=["members"])


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new member"
)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    """Register a new library member."""
    repo = MemberRepository(db)
    
    # Check if member with same email already exists
    existing_member = repo.get_member_by_email(member.email)
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member with email {member.email} already exists"
        )
    
    return repo.create_member(member)


@router.get(
    "/",
    response_model=List[MemberResponse],
    summary="List all members"
)
def list_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get a list of all active library members."""
    repo = MemberRepository(db)
    return repo.get_all_members(skip=skip, limit=limit)


@router.get(
    "/search",
    response_model=List[MemberResponse],
    summary="Search members"
)
def search_members(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Search members by name or email."""
    repo = MemberRepository(db)
    return repo.search_members(query=q, skip=skip, limit=limit)


@router.get(
    "/{member_id}",
    response_model=MemberDetailResponse,
    summary="Get member details"
)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """Get details of a specific member."""
    repo = MemberRepository(db)
    member = repo.get_member(member_id)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID {member_id} not found"
        )
    
    return member


@router.put(
    "/{member_id}",
    response_model=MemberResponse,
    summary="Update member information"
)
def update_member(
    member_id: int,
    member_update: MemberUpdate,
    db: Session = Depends(get_db)
):
    """Update member profile information."""
    repo = MemberRepository(db)
    member = repo.update_member(member_id, member_update)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID {member_id} not found"
        )
    
    return member


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a member"
)
def deactivate_member(member_id: int, db: Session = Depends(get_db)):
    """Deactivate a member account."""
    repo = MemberRepository(db)
    member = repo.deactivate_member(member_id)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID {member_id} not found"
        )
