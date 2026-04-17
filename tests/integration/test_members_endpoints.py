"""Integration tests for members endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.models import Member


class TestMembersEndpoints:
    """Integration tests for member endpoints."""
    
    def test_create_member(self, client: TestClient):
        """Test creating a member via API."""
        response = client.post(
            "/members/",
            json={
                "name": "Taher",
                "email": "taherch2025@gmail.com",
                "phone": "+1-555-0123",
                "address": "123 Main St"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Taher"
        assert data["is_active"] is True
    
    def test_create_member_duplicate_email(self, client: TestClient, sample_member: Member):
        """Test creating member with duplicate email."""
        response = client.post(
            "/members/",
            json={
                "name": "Different Name",
                "email": sample_member.email,
                "phone": "+1-555-9999"
            }
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_list_members(self, client: TestClient, sample_member: Member):
        """Test listing all members."""
        response = client.get("/members/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_search_members(self, client: TestClient, sample_member: Member):
        """Test searching members."""
        response = client.get("/members/search?q=John")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(member["id"] == sample_member.id for member in data)
    
    def test_get_member(self, client: TestClient, sample_member: Member):
        """Test getting a specific member."""
        response = client.get(f"/members/{sample_member.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_member.id
        assert data["email"] == sample_member.email
    
    def test_get_member_not_found(self, client: TestClient):
        """Test getting non-existent member."""
        response = client.get("/members/999")
        
        assert response.status_code == 404
    
    def test_update_member(self, client: TestClient, sample_member: Member):
        """Test updating a member."""
        response = client.put(
            f"/members/{sample_member.id}",
            json={
                "phone": "+1-555-9999",
                "address": "456 Oak Ave"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "+1-555-9999"
        assert data["address"] == "456 Oak Ave"
    
    def test_deactivate_member(self, client: TestClient, sample_member: Member):
        """Test deactivating a member."""
        response = client.delete(f"/members/{sample_member.id}")
        
        assert response.status_code == 204
        
        # Verify member is deactivated
        get_response = client.get(f"/members/{sample_member.id}")
        assert get_response.status_code == 404  # Active members only
