"""Unit tests for authentication service."""

import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate
from app.security import verify_password


class TestAuthService:
    """Test suite for AuthService."""
    
    def test_register_user(self, db: Session):
        """Test user registration."""
        service = AuthService(db)
        
        user_data = UserCreate(
            username="newuser",
            email="newuser@example.com",
            password="Password123"
        )
        
        user = service.register_user(user_data)
        
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.is_active is True
    
    def test_register_duplicate_username(self, db: Session):
        """Test registering with duplicate username."""
        service = AuthService(db)
        
        user_data1 = UserCreate(
            username="testuser",
            email="user1@example.com",
            password="Password123"
        )
        service.register_user(user_data1)
        
        user_data2 = UserCreate(
            username="testuser",
            email="user2@example.com",
            password="Password123"
        )
        
        with pytest.raises(HTTPException) as exc:
            service.register_user(user_data2)
        
        assert exc.value.status_code == 400
        assert "already registered" in exc.value.detail
    
    def test_register_duplicate_email(self, db: Session):
        """Test registering with duplicate email."""
        service = AuthService(db)
        
        user_data1 = UserCreate(
            username="user1",
            email="same@example.com",
            password="Password123"
        )
        service.register_user(user_data1)
        
        user_data2 = UserCreate(
            username="user2",
            email="same@example.com",
            password="Password123"
        )
        
        with pytest.raises(HTTPException) as exc:
            service.register_user(user_data2)
        
        assert exc.value.status_code == 400
        assert "already registered" in exc.value.detail
    
    def test_login_success(self, db: Session):
        """Test successful login."""
        service = AuthService(db)
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Password123"
        )
        service.register_user(user_data)
        
        token_response = service.login("testuser", "Password123")
        
        assert token_response.access_token is not None
        assert token_response.token_type == "bearer"
        assert token_response.user.username == "testuser"
    
    def test_login_invalid_username(self, db: Session):
        """Test login with invalid username."""
        service = AuthService(db)
        
        with pytest.raises(HTTPException) as exc:
            service.login("nonexistent", "Password123")
        
        assert exc.value.status_code == 401
    
    def test_login_invalid_password(self, db: Session):
        """Test login with invalid password."""
        service = AuthService(db)
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Password123"
        )
        service.register_user(user_data)
        
        with pytest.raises(HTTPException) as exc:
            service.login("testuser", "WrongPassword")
        
        assert exc.value.status_code == 401
    
    def test_login_inactive_user(self, db: Session):
        """Test login with inactive user."""
        service = AuthService(db)
        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Password123"
        )
        user = service.register_user(user_data)
        
        # Deactivate user
        from app.repositories.user_repository import UserRepository
        user_repo = UserRepository(db)
        user_repo.deactivate_user(user.id)
        
        with pytest.raises(HTTPException) as exc:
            service.login("testuser", "Password123")
        
        assert exc.value.status_code == 403
