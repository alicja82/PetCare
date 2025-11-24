"""
Integration tests for Pets endpoints
Testing complete pet management flow through API
"""
import pytest
import json
from flask_jwt_extended import create_access_token

class TestPetsEndpoints:
    """Test cases for pets API endpoints"""
    
    def get_auth_headers(self, app, user_id):
        """Helper to get authorization headers"""
        with app.app_context():
            token = create_access_token(identity=str(user_id))
        return {'Authorization': f'Bearer {token}'}
    
    def test_create_pet_endpoint(self, client, app, sample_user):
        """Test POST /api/pets endpoint"""
        headers = self.get_auth_headers(app, sample_user.id)
        
        response = client.post('/api/pets/',
            json={
                'name': 'Rex',
                'species': 'Dog',
                'breed': 'German Shepherd',
                'age': 5,
                'weight': 35.0
            },
            headers=headers
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['pet']['name'] == 'Rex'
        assert data['pet']['species'] == 'Dog'
