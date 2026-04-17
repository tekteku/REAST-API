"""Router for authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, TokenResponse, LoginRequest, UserResponse
from app.security import verify_token

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user"
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    service = AuthService(db)
    return service.register_user(user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get access token"
)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login with username and password to get JWT token."""
    service = AuthService(db)
    return service.login(credentials.username, credentials.password)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token"
)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Refresh an access token."""
    token = credentials.credentials
    token_data = verify_token(token)
    
    service = AuthService(db)
    user = service.get_current_user(token_data)
    
    # Create new token
    from app.security import create_access_token
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )
    
    return TokenResponse(
        access_token=access_token,
        user=user
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user"
)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get information about the current authenticated user."""
    token = credentials.credentials
    token_data = verify_token(token)
    
    service = AuthService(db)
    return service.get_current_user(token_data)
