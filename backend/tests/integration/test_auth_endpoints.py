"""
Integration tests for Auth endpoints
Testing complete authentication flow through API
"""
import pytest
import json

class TestAuthEndpoints:
    """Test cases for authentication API endpoints"""
    
    def test_register_endpoint(self, client):
        """Test POST /api/auth/register endpoint"""
        response = client.post('/api/auth/register', 
            json={
                'username': 'apiuser',
                'email': 'apiuser@example.com',
                'password': 'SecurePass123!'
            }
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['user']['username'] == 'apiuser'
