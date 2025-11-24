"""
Unit tests for PetService
Testing business logic for pet management
"""
import pytest
from services.pet_service import PetService
from models.pet import Pet

class TestPetService:
    """Test cases for PetService"""
    
    def test_create_pet_invalid_age(self, app, sample_user):
        """Test pet creation with negative age"""
        with app.app_context():
            pet_data = {
                'name': 'Buddy',
                'species': 'Dog',
                'breed': 'Beagle',
                'age': -3,
                'weight': 10.0
            }
            
            pet, error = PetService.create_pet(sample_user.id, pet_data)
            
            assert pet is None
            assert error is not None
            assert 'Age cannot be negative' in error
