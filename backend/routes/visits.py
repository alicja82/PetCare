from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.visit_service import VisitService
from services.pet_service import PetService
from middlewares.auth_middleware import verify_visit_owner

bp = Blueprint('visits', __name__, url_prefix='/api')

@bp.route('/pets/<int:pet_id>/visits', methods=['GET'])
@jwt_required()
def get_pet_visits(pet_id):
    """Get all vet visits for a specific pet"""
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    visits = VisitService.get_pet_visits(pet_id)
    
    return jsonify({
        'pet': pet.to_dict(),
        'visits': [visit.to_dict() for visit in visits]
    }), 200

@bp.route('/pets/<int:pet_id>/visits', methods=['POST'])
@jwt_required()
def create_visit(pet_id):
    """Create a new vet visit for a pet"""
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    data = request.get_json()
    
    # Create visit using service
    visit, error = VisitService.create_visit(pet_id, data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Vet visit created successfully',
        'visit': visit.to_dict()
    }), 201

@bp.route('/visits/<int:visit_id>', methods=['GET'])
@jwt_required()
@verify_visit_owner
def get_visit(visit_id, visit=None, pet=None):
    """Get a specific vet visit by ID"""
    return jsonify({
        'visit': visit.to_dict(),
        'pet': pet.to_dict()
    }), 200

@bp.route('/visits/<int:visit_id>', methods=['PUT'])
@jwt_required()
@verify_visit_owner
def update_visit(visit_id, visit=None, pet=None):
    """Update a vet visit"""
    data = request.get_json()
    
    # Update visit using service
    updated_visit, error = VisitService.update_visit(visit, data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Visit updated successfully',
        'visit': updated_visit.to_dict()
    }), 200

@bp.route('/visits/<int:visit_id>', methods=['DELETE'])
@jwt_required()
@verify_visit_owner
def delete_visit(visit_id, visit=None, pet=None):
    """Delete a vet visit"""
    VisitService.delete_visit(visit)
    
    return jsonify({'message': 'Visit deleted successfully'}), 200
