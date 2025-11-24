"""
Integration tests for Schedule endpoints
Testing complete feeding schedule flow through API
"""
import pytest
import json
from flask_jwt_extended import create_access_token

class TestScheduleEndpoints:
    """Test cases for schedule API endpoints"""
    
    def get_auth_headers(self, app, user_id):
        """Helper to get authorization headers"""
        with app.app_context():
            token = create_access_token(identity=str(user_id))
        return {'Authorization': f'Bearer {token}'}
    
    def test_create_schedule_endpoint(self, client, app, sample_user, sample_pet):
        """Test POST /api/pets/<id>/schedule endpoint"""
        headers = self.get_auth_headers(app, sample_user.id)
        
        response = client.post(f'/api/pets/{sample_pet.id}/schedule',
            json={
                'food_type': 'Premium dog food',
                'amount': '250g',
                'time': '09:00',
                'frequency': 'Daily'
            },
            headers=headers
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['schedule']['food_type'] == 'Premium dog food'
        assert data['schedule']['time'] == '09:00'
