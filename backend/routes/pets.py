from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.pet_service import PetService
from utils.file_helper import FileUploadHelper

bp = Blueprint('pets', __name__, url_prefix='/api/pets')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_pets():
    """Get all pets for the current user"""
    current_user_id = int(get_jwt_identity())
    pets = PetService.get_user_pets(current_user_id)
    
    return jsonify({
        'pets': [pet.to_dict() for pet in pets]
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_pet():
    """Create a new pet"""
    current_user_id = int(get_jwt_identity())
    
    # Handle photo upload
    photo_url = None
    if 'photo' in request.files:
        photo_url = FileUploadHelper.save_photo(request.files['photo'])
    
    # Get data from form or JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    # Create pet using service
    pet, errors = PetService.create_pet(current_user_id, data, photo_url)
    
    if errors:
        return jsonify({'error': errors}), 400
    
    return jsonify({
        'message': 'Pet created successfully',
        'pet': pet.to_dict()
    }), 201

@bp.route('/<int:pet_id>', methods=['GET'])
@jwt_required()
def get_pet(pet_id):
    """Get a specific pet by ID"""
    current_user_id = int(get_jwt_identity())
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify({'pet': pet.to_dict()}), 200

@bp.route('/<int:pet_id>', methods=['PUT'])
@jwt_required()
def update_pet(pet_id):
    """Update a pet"""
    current_user_id = int(get_jwt_identity())
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Handle photo upload
    photo_url = None
    if 'photo' in request.files:
        # Delete old photo
        if pet.photo_url:
            FileUploadHelper.delete_photo(pet.photo_url)
        photo_url = FileUploadHelper.save_photo(request.files['photo'])
    
    # Get data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    # Update pet using service
    updated_pet, errors = PetService.update_pet(pet, data, photo_url)
    
    if errors:
        return jsonify({'error': errors}), 400
    
    return jsonify({
        'message': 'Pet updated successfully',
        'pet': updated_pet.to_dict()
    }), 200

@bp.route('/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    """Delete a pet"""
    current_user_id = int(get_jwt_identity())
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Delete photo
    if pet.photo_url:
        FileUploadHelper.delete_photo(pet.photo_url)
    
    # Delete pet using service
    PetService.delete_pet(pet)
    
    return jsonify({'message': 'Pet deleted successfully'}), 200
