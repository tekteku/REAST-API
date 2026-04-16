"""Unit tests for user repository."""

import pytest
from sqlalchemy.orm import Session
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate
from app.security import get_password_hash


class TestUserRepository:
    """Test suite for UserRepository."""
    
    def test_create_user(self, db: Session):
        """Test creating a new user."""
        repo = UserRepository(db)
        password_hash = get_password_hash("TestPassword123")
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        
        user = repo.create_user(user_data, password_hash)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_admin is False
    
    def test_get_user(self, db: Session):
        """Test retrieving a user by ID."""
        repo = UserRepository(db)
        password_hash = get_password_hash("TestPassword123")
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        created_user = repo.create_user(user_data, password_hash)
        
        retrieved_user = repo.get_user(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
    
    def test_get_user_by_username(self, db: Session):
        """Test retrieving a user by username."""
        repo = UserRepository(db)
        password_hash = get_password_hash("TestPassword123")
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        repo.create_user(user_data, password_hash)
        
        user = repo.get_user_by_username("testuser")
        
        assert user is not None
        assert user.username == "testuser"
    
    def test_get_user_by_email(self, db: Session):
        """Test retrieving a user by email."""
        repo = UserRepository(db)
        password_hash = get_password_hash("TestPassword123")
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        repo.create_user(user_data, password_hash)
        
        user = repo.get_user_by_email("test@example.com")
        
        assert user is not None
        assert user.email == "test@example.com"
    
    def test_get_active_user(self, db: Session):
        """Test retrieving an active user."""
        repo = UserRepository(db)
        password_hash = get_password_hash("TestPassword123")
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        created_user = repo.create_user(user_data, password_hash)
        
        active_user = repo.get_active_user(created_user.id)
        
        assert active_user is not None
        assert active_user.is_active is True
    
    def test_deactivate_user(self, db: Session):
        """Test deactivating a user."""
        repo = UserRepository(db)
        password_hash = get_password_hash("TestPassword123")
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )
        created_user = repo.create_user(user_data, password_hash)
        
        deactivated = repo.deactivate_user(created_user.id)
        
        assert deactivated.is_active is False
