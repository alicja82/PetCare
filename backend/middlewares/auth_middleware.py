"""
Authentication middleware and decorators
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def verify_pet_owner(get_pet_func):
    """
    Decorator to verify that the current user owns the pet
    Usage: @verify_pet_owner(lambda pet_id: Pet.query.get(pet_id))
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(pet_id, *args, **kwargs):
            from models.pet import Pet
            
            current_user_id = int(get_jwt_identity())
            pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
            
            if not pet:
                return jsonify({'error': 'Pet not found'}), 404
            
            # Pass pet to the function to avoid duplicate query
            return f(pet_id, pet=pet, *args, **kwargs)
        
        return decorated_function
    return decorator

def verify_schedule_owner(f):
    """
    Decorator to verify that the current user owns the schedule's pet
    """
    @wraps(f)
    def decorated_function(schedule_id, *args, **kwargs):
        from models.pet import Pet
        from models.feeding_schedule import FeedingSchedule
        
        current_user_id = int(get_jwt_identity())
        schedule = FeedingSchedule.query.get(schedule_id)
        
        if not schedule:
            return jsonify({'error': 'Schedule not found'}), 404
        
        pet = Pet.query.filter_by(id=schedule.pet_id, user_id=current_user_id).first()
        
        if not pet:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Pass schedule and pet to the function
        return f(schedule_id, schedule=schedule, pet=pet, *args, **kwargs)
    
    return decorated_function

def verify_visit_owner(f):
    """
    Decorator to verify that the current user owns the visit's pet
    """
    @wraps(f)
    def decorated_function(visit_id, *args, **kwargs):
        from models.pet import Pet
        from models.vet_visit import VetVisit
        
        current_user_id = int(get_jwt_identity())
        visit = VetVisit.query.get(visit_id)
        
        if not visit:
            return jsonify({'error': 'Visit not found'}), 404
        
        pet = Pet.query.filter_by(id=visit.pet_id, user_id=current_user_id).first()
        
        if not pet:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Pass visit and pet to the function
        return f(visit_id, visit=visit, pet=pet, *args, **kwargs)
    
    return decorated_function
