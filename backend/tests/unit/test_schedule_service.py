"""
Unit tests for ScheduleService
Testing business logic for feeding schedule management
"""
import pytest
from services.schedule_service import ScheduleService
from models.feeding_schedule import FeedingSchedule
from datetime import time

class TestScheduleService:
    """Test cases for ScheduleService"""
    
    def test_create_schedule_success(self, app, sample_pet):
        """Test successful schedule creation"""
        with app.app_context():
            schedule_data = {
                'food_type': 'Dry dog food',
                'amount': '200g',
                'time': '08:00',
                'frequency': 'Daily'
            }
            
            schedule, error = ScheduleService.create_schedule(sample_pet.id, schedule_data)
            
            assert schedule is not None
            assert error is None
            assert schedule.food_type == 'Dry dog food'
            assert schedule.amount == '200g'
            assert schedule.pet_id == sample_pet.id
