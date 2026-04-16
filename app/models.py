"""SQLAlchemy ORM models for the library database."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class Book(Base):
    """Book model representing books in the library."""
    
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    loans = relationship("Loan", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"


class Member(Base):
    """Member model representing library members."""
    
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    loans = relationship("Loan", back_populates="member", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member(id={self.id}, name={self.name}, email={self.email})>"


class Loan(Base):
    """Loan model representing book loans to members."""
    
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    borrowed_at = Column(DateTime, server_default=func.now())
    due_date = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")
    
    def __repr__(self):
        return f"<Loan(id={self.id}, book_id={self.book_id}, member_id={self.member_id})>"
