from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, time

bp = Blueprint('schedules', __name__, url_prefix='/api')

@bp.route('/pets/<int:pet_id>/schedule', methods=['GET'])
@jwt_required()
def get_pet_schedule(pet_id):
    """Get all feeding schedules for a specific pet"""
    from app import db
    from models.pet import Pet
    from models.feeding_schedule import FeedingSchedule
    
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    schedules = FeedingSchedule.query.filter_by(pet_id=pet_id).all()
    
    return jsonify({
        'pet': pet.to_dict(),
        'schedules': [schedule.to_dict() for schedule in schedules]
    }), 200

@bp.route('/pets/<int:pet_id>/schedule', methods=['POST'])
@jwt_required()
def create_schedule(pet_id):
    """Create a new feeding schedule for a pet"""
    from app import db
    from models.pet import Pet
    from models.feeding_schedule import FeedingSchedule
    
    current_user_id = get_jwt_identity()
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('food_type') or not data.get('time'):
        return jsonify({'error': 'food_type and time are required'}), 400
    
    # Parse time (format: "HH:MM")
    try:
        time_str = data.get('time')
        hour, minute = map(int, time_str.split(':'))
        feeding_time = time(hour, minute)
    except (ValueError, AttributeError):
        return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400
    
    # Create new schedule
    new_schedule = FeedingSchedule(
        pet_id=pet_id,
        food_type=data.get('food_type'),
        amount=data.get('amount'),
        time=feeding_time,
        frequency=data.get('frequency'),
        notes=data.get('notes')
    )
    
    db.session.add(new_schedule)
    db.session.commit()
    
    return jsonify({
        'message': 'Feeding schedule created successfully',
        'schedule': new_schedule.to_dict()
    }), 201

@bp.route('/schedule/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_schedule(schedule_id):
    """Update a feeding schedule"""
    from app import db
    from models.pet import Pet
    from models.feeding_schedule import FeedingSchedule
    
    current_user_id = get_jwt_identity()
    
    schedule = FeedingSchedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=schedule.pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields if provided
    if 'food_type' in data:
        schedule.food_type = data['food_type']
    if 'amount' in data:
        schedule.amount = data['amount']
    if 'time' in data:
        try:
            time_str = data['time']
            hour, minute = map(int, time_str.split(':'))
            schedule.time = time(hour, minute)
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400
    if 'frequency' in data:
        schedule.frequency = data['frequency']
    if 'notes' in data:
        schedule.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Schedule updated successfully',
        'schedule': schedule.to_dict()
    }), 200

@bp.route('/schedule/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(schedule_id):
    """Delete a feeding schedule"""
    from app import db
    from models.pet import Pet
    from models.feeding_schedule import FeedingSchedule
    
    current_user_id = get_jwt_identity()
    
    schedule = FeedingSchedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
    
    # Verify pet belongs to user
    pet = Pet.query.filter_by(id=schedule.pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(schedule)
    db.session.commit()
    
    return jsonify({'message': 'Schedule deleted successfully'}), 200

@bp.route('/schedule/day/<date>', methods=['GET'])
@jwt_required()
def get_schedules_by_day(date):
    """Get all feeding schedules for a specific day (all user's pets)"""
    from app import db
    from models.pet import Pet
    from models.feeding_schedule import FeedingSchedule
    
    current_user_id = get_jwt_identity()
    
    # Get all user's pets
    user_pets = Pet.query.filter_by(user_id=current_user_id).all()
    pet_ids = [pet.id for pet in user_pets]
    
    # Get all schedules for these pets
    schedules = FeedingSchedule.query.filter(FeedingSchedule.pet_id.in_(pet_ids)).all()
    
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
    from app import db
    from models.pet import Pet
    from models.feeding_schedule import FeedingSchedule
    
    current_user_id = get_jwt_identity()
    
    # Validate month
    if month < 1 or month > 12:
        return jsonify({'error': 'Invalid month. Must be 1-12'}), 400
    
    # Get all user's pets
    user_pets = Pet.query.filter_by(user_id=current_user_id).all()
    pet_ids = [pet.id for pet in user_pets]
    
    # Get all schedules for these pets
    schedules = FeedingSchedule.query.filter(FeedingSchedule.pet_id.in_(pet_ids)).all()
    
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
