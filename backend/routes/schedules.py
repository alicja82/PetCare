from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.schedule_service import ScheduleService
from services.pet_service import PetService
from middlewares.auth_middleware import verify_schedule_owner

bp = Blueprint('schedules', __name__, url_prefix='/api')

@bp.route('/pets/<int:pet_id>/schedule', methods=['GET'])
@jwt_required()
def get_pet_schedule(pet_id):
    """Get all feeding schedules for a specific pet"""
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    schedules = ScheduleService.get_pet_schedules(pet_id)
    
    return jsonify({
        'pet': pet.to_dict(),
        'schedules': [schedule.to_dict() for schedule in schedules]
    }), 200

@bp.route('/pets/<int:pet_id>/schedule', methods=['POST'])
@jwt_required()
def create_schedule(pet_id):
    """Create a new feeding schedule for a pet"""
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = PetService.get_pet_by_id(pet_id, current_user_id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    data = request.get_json()
    
    # Create schedule using service
    schedule, error = ScheduleService.create_schedule(pet_id, data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Feeding schedule created successfully',
        'schedule': schedule.to_dict()
    }), 201

@bp.route('/schedule/<int:schedule_id>', methods=['PUT'])
@jwt_required()
@verify_schedule_owner
def update_schedule(schedule_id, schedule=None, pet=None):
    """Update a feeding schedule"""
    data = request.get_json()
    
    # Update schedule using service
    updated_schedule, error = ScheduleService.update_schedule(schedule, data)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Schedule updated successfully',
        'schedule': updated_schedule.to_dict()
    }), 200

@bp.route('/schedule/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
@verify_schedule_owner
def delete_schedule(schedule_id, schedule=None, pet=None):
    """Delete a feeding schedule"""
    ScheduleService.delete_schedule(schedule)
    
    return jsonify({'message': 'Schedule deleted successfully'}), 200

@bp.route('/schedule/day/<date>', methods=['GET'])
@jwt_required()
def get_schedules_by_day(date):
    """Get all feeding schedules for a specific day (all user's pets)"""
    current_user_id = get_jwt_identity()
    
    # Get all user's pets
    user_pets = PetService.get_user_pets(current_user_id)
    pet_ids = [pet.id for pet in user_pets]
    
    # Get all schedules for these pets
    schedules = ScheduleService.get_schedules_for_user_pets(pet_ids)
    
    # Group by pet
    schedules_by_pet = {}
    for schedule in schedules:
        pet = next((p for p in user_pets if p.id == schedule.pet_id), None)
        if pet:
            if pet.name not in schedules_by_pet:
                schedules_by_pet[pet.name] = {
                    'pet': pet.to_dict(),
                    'schedules': []
                }
            schedules_by_pet[pet.name]['schedules'].append(schedule.to_dict())
    
    return jsonify({
        'date': date,
        'schedules_by_pet': schedules_by_pet
    }), 200

@bp.route('/schedule/month/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def get_schedules_by_month(year, month):
    """Get all feeding schedules for a specific month (all user's pets)"""
    current_user_id = get_jwt_identity()
    
    # Validate month
    if month < 1 or month > 12:
        return jsonify({'error': 'Invalid month. Must be 1-12'}), 400
    
    # Get all user's pets
    user_pets = PetService.get_user_pets(current_user_id)
    pet_ids = [pet.id for pet in user_pets]
    
    # Get all schedules for these pets
    schedules = ScheduleService.get_schedules_for_user_pets(pet_ids)
    
    # Build response
    result = {
        'year': year,
        'month': month,
        'schedules': []
    }
    
    for schedule in schedules:
        pet = next((p for p in user_pets if p.id == schedule.pet_id), None)
        if pet:
            schedule_dict = schedule.to_dict()
            schedule_dict['pet_name'] = pet.name
            result['schedules'].append(schedule_dict)
    
    return jsonify(result), 200
