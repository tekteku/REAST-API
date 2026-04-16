"""FastAPI main application factory and startup configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.database import engine, Base
from app.models import Book, Member, Loan, User
from app.routers import books, members, loans, auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Library REST API",
    description="A REST API for managing library books, members, and loans with JWT authentication",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(members.router)
app.include_router(loans.router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Library API")
    # Create tables
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Library API")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to Library REST API",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
