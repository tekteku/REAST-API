"""Pydantic schemas for Book endpoints."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    """Base schema for book data."""
    
    isbn: str = Field(..., min_length=10, max_length=20, description="ISBN number")
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    total_copies: int = Field(default=1, ge=1)


class BookCreate(BookBase):
    """Schema for creating a new book."""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    total_copies: Optional[int] = Field(None, ge=1)


class BookResponse(BookBase):
    """Schema for book responses."""
    
    id: int
    available_copies: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BookDetailResponse(BookResponse):
    """Detailed book response with additional info."""
    
    pass
