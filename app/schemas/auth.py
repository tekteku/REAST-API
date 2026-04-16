"""Pydantic schemas for authentication."""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for user data."""
    
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration."""
    
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(UserBase):
    """Schema for user responses."""
    
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request."""
    
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Schema for token response."""
    
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Schema for token data."""
    
    username: Optional[str] = None
    user_id: Optional[int] = None
