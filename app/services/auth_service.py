"""Service layer for authentication business logic."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, LoginRequest, TokenResponse, UserResponse
from app.security import verify_password, get_password_hash, create_access_token
from app.models import User
from datetime import timedelta


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user."""
        # Check if username exists
        existing_user = self.user_repo.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email exists
        existing_email = self.user_repo.get_user_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)
        user = self.user_repo.create_user(user_data, hashed_password)
        
        return UserResponse.from_orm(user)
    
    def login(self, username: str, password: str) -> TokenResponse:
        """Authenticate user and return token."""
        # Get user
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Create token
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse.from_orm(user)
        )
    
    def get_current_user(self, token_data: dict) -> User:
        """Get current user from token data."""
        user_id = token_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = self.user_repo.get_active_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        return user
