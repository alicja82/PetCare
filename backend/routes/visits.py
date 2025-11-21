from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('visits', __name__, url_prefix='/api')

@bp.route('/pets/<int:pet_id>/visits', methods=['GET'])
@jwt_required()
def get_pet_visits(pet_id):
    """Get all vet visits for a specific pet"""
    from app import db
    from models.pet import Pet
    from models.vet_visit import VetVisit
    
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Get visits sorted by date (newest first)
    visits = VetVisit.query.filter_by(pet_id=pet_id).order_by(VetVisit.visit_date.desc()).all()
    
    return jsonify({
        'pet': pet.to_dict(),
        'visits': [visit.to_dict() for visit in visits]
    }), 200

@bp.route('/pets/<int:pet_id>/visits', methods=['POST'])
@jwt_required()
def create_visit(pet_id):
    """Create a new vet visit for a pet"""
    from app import db
    from models.pet import Pet
    from models.vet_visit import VetVisit
    
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('visit_date') or not data.get('reason'):
        return jsonify({'error': 'visit_date and reason are required'}), 400
    
    # Parse visit_date
    try:
        visit_date = datetime.fromisoformat(data.get('visit_date').replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return jsonify({'error': 'Invalid visit_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Create new visit
    new_visit = VetVisit(
        pet_id=pet_id,
        visit_date=visit_date,
        vet_name=data.get('vet_name'),
        clinic_name=data.get('clinic_name'),
        reason=data.get('reason'),
        diagnosis=data.get('diagnosis'),
        treatment=data.get('treatment'),
        medications=data.get('medications'),
        notes=data.get('notes')
    )
    
    db.session.add(new_visit)
    db.session.commit()
    
    return jsonify({
        'message': 'Vet visit created successfully',
        'visit': new_visit.to_dict()
    }), 201

@bp.route('/visits/<int:visit_id>', methods=['GET'])
@jwt_required()
def get_visit(visit_id):
    """Get a specific vet visit by ID"""
    from app import db
    from models.pet import Pet
    from models.vet_visit import VetVisit
    
    current_user_id = get_jwt_identity()
    
    visit = VetVisit.query.get(visit_id)
    if not visit:
        return jsonify({'error': 'Visit not found'}), 404
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=visit.pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'visit': visit.to_dict(),
        'pet': pet.to_dict()
    }), 200

@bp.route('/visits/<int:visit_id>', methods=['PUT'])
@jwt_required()
def update_visit(visit_id):
    """Update a vet visit"""
    from app import db
    from models.pet import Pet
    from models.vet_visit import VetVisit
    
    current_user_id = get_jwt_identity()
    
    visit = VetVisit.query.get(visit_id)
    if not visit:
        return jsonify({'error': 'Visit not found'}), 404
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=visit.pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields if provided
    if 'visit_date' in data:
        try:
            visit.visit_date = datetime.fromisoformat(data['visit_date'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid visit_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if 'vet_name' in data:
        visit.vet_name = data['vet_name']
    if 'clinic_name' in data:
        visit.clinic_name = data['clinic_name']
    if 'reason' in data:
        visit.reason = data['reason']
    if 'diagnosis' in data:
        visit.diagnosis = data['diagnosis']
    if 'treatment' in data:
        visit.treatment = data['treatment']
    if 'medications' in data:
        visit.medications = data['medications']
    if 'notes' in data:
        visit.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Visit updated successfully',
        'visit': visit.to_dict()
    }), 200

@bp.route('/visits/<int:visit_id>', methods=['DELETE'])
@jwt_required()
def delete_visit(visit_id):
    """Delete a vet visit"""
    from app import db
    from models.pet import Pet
    from models.vet_visit import VetVisit
    
    current_user_id = get_jwt_identity()
    
    visit = VetVisit.query.get(visit_id)
    if not visit:
        return jsonify({'error': 'Visit not found'}), 404
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=visit.pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(visit)
    db.session.commit()
    
    return jsonify({'message': 'Visit deleted successfully'}), 200
