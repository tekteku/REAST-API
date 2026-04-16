"""Repository for member data access."""

from sqlalchemy.orm import Session
from app.models import Member
from app.schemas.member import MemberCreate, MemberUpdate
from typing import List, Optional


class MemberRepository:
    """Repository for member database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_member(self, member_id: int) -> Optional[Member]:
        """Get a member by ID."""
        return self.db.query(Member).filter(Member.id == member_id).first()
    
    def get_member_by_email(self, email: str) -> Optional[Member]:
        """Get a member by email."""
        return self.db.query(Member).filter(Member.email == email).first()
    
    def get_all_members(self, skip: int = 0, limit: int = 100) -> List[Member]:
        """Get all members with pagination."""
        return self.db.query(Member).filter(
            Member.is_active == True
        ).offset(skip).limit(limit).all()
    
    def search_members(self, query: str, skip: int = 0, limit: int = 100) -> List[Member]:
        """Search members by name or email."""
        search_pattern = f"%{query}%"
        return self.db.query(Member).filter(
            (Member.name.ilike(search_pattern)) |
            (Member.email.ilike(search_pattern)),
            Member.is_active == True
        ).offset(skip).limit(limit).all()
    
    def create_member(self, member: MemberCreate) -> Member:
        """Create a new member."""
        db_member = Member(
            name=member.name,
            email=member.email,
            phone=member.phone,
            address=member.address
        )
        self.db.add(db_member)
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
    
    def update_member(self, member_id: int, member_update: MemberUpdate) -> Optional[Member]:
        """Update a member."""
        db_member = self.get_member(member_id)
        if not db_member:
            return None
        
        update_data = member_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_member, key, value)
        
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
    
    def deactivate_member(self, member_id: int) -> Optional[Member]:
        """Deactivate a member."""
        db_member = self.get_member(member_id)
        if not db_member:
            return None
        
        db_member.is_active = False
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
    
    def activate_member(self, member_id: int) -> Optional[Member]:
        """Activate a member."""
        db_member = self.db.query(Member).filter(Member.id == member_id).first()
        if not db_member:
            return None
        
        db_member.is_active = True
        self.db.commit()
        self.db.refresh(db_member)
        return db_member
