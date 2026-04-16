"""Pydantic schemas for Member endpoints."""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime


class MemberBase(BaseModel):
    """Base schema for member data."""
    
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)


class MemberCreate(MemberBase):
    """Schema for creating a new member."""
    pass


class MemberUpdate(BaseModel):
    """Schema for updating a member."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)


class MemberResponse(MemberBase):
    """Schema for member responses."""
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MemberDetailResponse(MemberResponse):
    """Detailed member response."""
    
    pass
