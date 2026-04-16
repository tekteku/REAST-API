"""Repository for user data access."""

from sqlalchemy.orm import Session
from app.models import User
from app.schemas.auth import UserCreate
from typing import Optional


class UserRepository:
    """Repository for user database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_active_user(self, user_id: int) -> Optional[User]:
        """Get an active user by ID."""
        return self.db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
    
    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        """Create a new user."""
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user."""
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        
        db_user.is_active = False
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
