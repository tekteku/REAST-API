"""Integration tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestAuthEndpoints:
    """Integration tests for auth endpoints."""
    
    def test_register_user(self, client: TestClient):
        """Test user registration via API."""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "Password123",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    def test_register_weak_password(self, client: TestClient):
        """Test registration with weak password."""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "weak"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_success(self, client: TestClient):
        """Test successful login."""
        # Register first
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "Password123"
            }
        )
        
        # Login
        response = client.post(
            "/auth/login",
            json={
                "username": "testuser",
                "password": "Password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "testuser"
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        # Register first
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "Password123"
            }
        )
        
        # Try to login with wrong password
        response = client.post(
            "/auth/login",
            json={
                "username": "testuser",
                "password": "WrongPassword"
            }
        )
        
        assert response.status_code == 401
    
    def test_get_current_user(self, client: TestClient):
        """Test getting current user info."""
        # Register and login
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "Password123"
            }
        )
        
        login_response = client.post(
            "/auth/login",
            json={
                "username": "testuser",
                "password": "Password123"
            }
        )
        
        token = login_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
    
    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token."""
        response = client.get("/auth/me")
        
        assert response.status_code == 403
    
    def test_refresh_token(self, client: TestClient):
        """Test refreshing access token."""
        # Register and login
        client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "Password123"
            }
        )
        
        login_response = client.post(
            "/auth/login",
            json={
                "username": "testuser",
                "password": "Password123"
            }
        )
        
        token = login_response.json()["access_token"]
        
        # Refresh token
        response = client.post(
            "/auth/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
