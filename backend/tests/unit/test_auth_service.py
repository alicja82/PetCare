"""
Unit tests for AuthService
Testing business logic for user authentication
"""
import pytest
from services.auth_service import AuthService
from models.user import User

class TestAuthService:
    """Test cases for AuthService"""
    
    def test_register_user_success(self, app):
        """Test successful user registration"""
        with app.app_context():
            user_data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'SecurePass123!'
            }
            
            user, token, error = AuthService.register_user(user_data)
            
            assert user is not None
            assert token is not None
            assert error is None
            assert user.username == 'newuser'
            assert user.email == 'newuser@example.com'
