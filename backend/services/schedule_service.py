"""
Feeding schedule service - Business logic for feeding schedules
"""
from app import db
from models.feeding_schedule import FeedingSchedule
from datetime import time
from utils.validators import validate_time, validate_string_length

class ScheduleService:
    
    @staticmethod
    def get_pet_schedules(pet_id):
        """Get all schedules for a pet"""
        return FeedingSchedule.query.filter_by(pet_id=pet_id).all()
    
    @staticmethod
    def create_schedule(pet_id, data):
        """Create a new feeding schedule"""
        # Validate data
        errors = ScheduleService._validate_schedule_data(data)
        if errors:
            return None, errors
        
        # Parse time
        time_str = data.get('time')
        hour, minute = map(int, time_str.split(':'))
        feeding_time = time(hour, minute)
        
        # Create schedule
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
        
        return new_schedule, None
    
    @staticmethod
    def update_schedule(schedule, data):
        """Update a schedule"""
        # Update fields if provided
        if 'food_type' in data:
            schedule.food_type = data['food_type']
        if 'amount' in data:
            schedule.amount = data['amount']
        if 'time' in data:
            is_valid, error = validate_time(data['time'])
            if not is_valid:
                return None, error
            time_str = data['time']
            hour, minute = map(int, time_str.split(':'))
            schedule.time = time(hour, minute)
        if 'frequency' in data:
            schedule.frequency = data['frequency']
        if 'notes' in data:
            schedule.notes = data['notes']
        
        db.session.commit()
        
        return schedule, None
    
    @staticmethod
    def delete_schedule(schedule):
        """Delete a schedule"""
        db.session.delete(schedule)
        db.session.commit()
        return True
    
    @staticmethod
    def get_schedules_for_user_pets(pet_ids):
        """Get all schedules for user's pets"""
        return FeedingSchedule.query.filter(FeedingSchedule.pet_id.in_(pet_ids)).all()
    
    @staticmethod
    def _validate_schedule_data(data):
        """Validate schedule data"""
        if not data.get('food_type') or not data.get('time'):
            return 'food_type and time are required'
        
        # Validate food_type
        is_valid, error = validate_string_length(data.get('food_type'), 'Food type', min_length=1, max_length=100)
        if not is_valid:
            return error
        
        # Validate time
        is_valid, error = validate_time(data.get('time'))
        if not is_valid:
            return error
        
        return None
