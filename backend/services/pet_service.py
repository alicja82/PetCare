"""
Pet service - Business logic for pet management
"""
from app import db
from models.pet import Pet
from utils.validators import validate_age, validate_weight, validate_string_length

class PetService:
    
    @staticmethod
    def get_user_pets(user_id):
        """Get all pets for a user"""
        return Pet.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_pet_by_id(pet_id, user_id):
        """Get a specific pet by ID for a user"""
        return Pet.query.filter_by(id=pet_id, user_id=user_id).first()
    
    @staticmethod
    def create_pet(user_id, data, photo_url=None):
        """Create a new pet"""
        # Validate data
        errors = PetService._validate_pet_data(data, is_create=True)
        if errors:
            return None, errors
        
        # Handle tags
        tags = data.get('tags', [])
        if isinstance(tags, list):
            tags = ','.join(tags)
        
        # Create pet
        new_pet = Pet(
            name=data.get('name'),
            species=data.get('species'),
            breed=data.get('breed'),
            age=data.get('age'),
            weight=data.get('weight'),
            photo_url=photo_url,
            tags=tags,
            notes=data.get('notes'),
            user_id=user_id
        )
        
        db.session.add(new_pet)
        db.session.commit()
        
        return new_pet, None
    
    @staticmethod
    def update_pet(pet, data, photo_url=None):
        """Update an existing pet"""
        # Validate data
        errors = PetService._validate_pet_data(data, is_create=False)
        if errors:
            return None, errors
        
        # Update fields if provided
        if 'name' in data:
            pet.name = data['name']
        if 'species' in data:
            pet.species = data['species']
        if 'breed' in data:
            pet.breed = data['breed']
        if 'age' in data:
            pet.age = data['age']
        if 'weight' in data:
            pet.weight = data['weight']
        if 'notes' in data:
            pet.notes = data['notes']
        if 'tags' in data:
            tags = data['tags']
            if isinstance(tags, list):
                tags = ','.join(tags)
            pet.tags = tags
        if photo_url:
            pet.photo_url = photo_url
        
        db.session.commit()
        
        return pet, None
    
    @staticmethod
    def delete_pet(pet):
        """Delete a pet"""
        db.session.delete(pet)
        db.session.commit()
        return True
    
    @staticmethod
    def _validate_pet_data(data, is_create=True):
        """Validate pet data"""
        errors = []
        
        # Required fields for creation
        if is_create:
            if not data.get('name') or not data.get('species'):
                errors.append('Name and species are required')
                return errors
        
        # Validate name
        if 'name' in data:
            is_valid, error = validate_string_length(data.get('name'), 'Name', min_length=1, max_length=100)
            if not is_valid:
                errors.append(error)
        
        # Validate species
        if 'species' in data:
            is_valid, error = validate_string_length(data.get('species'), 'Species', min_length=1, max_length=50)
            if not is_valid:
                errors.append(error)
        
        # Validate age
        if data.get('age'):
            is_valid, error = validate_age(data.get('age'))
            if not is_valid:
                errors.append(error)
        
        # Validate weight
        if data.get('weight'):
            is_valid, error = validate_weight(data.get('weight'))
            if not is_valid:
                errors.append(error)
        
        return errors if errors else None
