"""Unit tests for member repository."""

import pytest
from sqlalchemy.orm import Session
from app.models import Member
from app.repositories.member_repository import MemberRepository
from app.schemas.member import MemberCreate, MemberUpdate


class TestMemberRepository:
    """Test suite for MemberRepository."""
    
    def test_create_member(self, db: Session):
        """Test creating a new member."""
        repo = MemberRepository(db)
        member_data = MemberCreate(
            name="Taher",
            email="taher@example.com",
            phone="+1-555-0123",
            address="123 Main St"
        )
        
        member = repo.create_member(member_data)
        
        assert member.id is not None
        assert member.name == "Taher"
        assert member.email == "taher@example.com"
        assert member.is_active is True
    
    def test_get_member(self, db: Session, sample_member: Member):
        """Test retrieving a member by ID."""
        repo = MemberRepository(db)
        member = repo.get_member(sample_member.id)
        
        assert member is not None
        assert member.id == sample_member.id
        assert member.email == sample_member.email
    
    def test_get_member_not_found(self, db: Session):
        """Test retrieving a non-existent member."""
        repo = MemberRepository(db)
        member = repo.get_member(999)
        
        assert member is None
    
    def test_get_member_by_email(self, db: Session, sample_member: Member):
        """Test retrieving a member by email."""
        repo = MemberRepository(db)
        member = repo.get_member_by_email(sample_member.email)
        
        assert member is not None
        assert member.email == sample_member.email
    
    def test_get_all_members(self, db: Session, sample_member: Member):
        """Test retrieving all active members."""
        repo = MemberRepository(db)
        members = repo.get_all_members()
        
        assert len(members) >= 1
        assert any(m.id == sample_member.id for m in members)
    
    def test_search_members_by_name(self, db: Session, sample_member: Member):
        """Test searching members by name."""
        repo = MemberRepository(db)
        members = repo.search_members("John")
        
        assert len(members) >= 1
        assert any(m.id == sample_member.id for m in members)
    
    def test_search_members_by_email(self, db: Session, sample_member: Member):
        """Test searching members by email."""
        repo = MemberRepository(db)
        members = repo.search_members("john@example")
        
        assert len(members) >= 1
        assert any(m.id == sample_member.id for m in members)
    
    def test_update_member(self, db: Session, sample_member: Member):
        """Test updating a member."""
        repo = MemberRepository(db)
        update_data = MemberUpdate(
            phone="+1-555-9999",
            address="456 Oak Ave"
        )
        
        updated_member = repo.update_member(sample_member.id, update_data)
        
        assert updated_member.phone == "+1-555-9999"
        assert updated_member.address == "456 Oak Ave"
    
    def test_deactivate_member(self, db: Session, sample_member: Member):
        """Test deactivating a member."""
        repo = MemberRepository(db)
        deactivated_member = repo.deactivate_member(sample_member.id)
        
        assert deactivated_member.is_active is False
    
    def test_activate_member(self, db: Session, sample_member: Member):
        """Test activating a member."""
        repo = MemberRepository(db)
        
        # First deactivate
        repo.deactivate_member(sample_member.id)
        
        # Then activate
        activated_member = repo.activate_member(sample_member.id)
        
        assert activated_member.is_active is True
    
    def test_inactive_members_excluded(self, db: Session, sample_member: Member):
        """Test that inactive members are excluded from listing."""
        repo = MemberRepository(db)
        
        repo.deactivate_member(sample_member.id)
        members = repo.get_all_members()
        
        assert len(members) == 0
