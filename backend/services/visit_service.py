"""
Vet visit service - Business logic for vet visits
"""
from app import db
from models.vet_visit import VetVisit
from datetime import datetime
from utils.validators import validate_date, validate_future_date, validate_string_length

class VisitService:
    
    @staticmethod
    def get_pet_visits(pet_id):
        """Get all visits for a pet"""
        return VetVisit.query.filter_by(pet_id=pet_id).order_by(VetVisit.visit_date.desc()).all()
    
    @staticmethod
    def create_visit(pet_id, data):
        """Create a new vet visit"""
        # Validate data
        visit_date, errors = VisitService._validate_visit_data(data)
        if errors:
            return None, errors
        
        # Create visit
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
        
        return new_visit, None
    
    @staticmethod
    def update_visit(visit, data):
        """Update a visit"""
        # Validate visit_date if provided
        if 'visit_date' in data:
            is_valid, visit_date, error = validate_date(data['visit_date'], 'Visit date')
            if not is_valid:
                return None, error
            
            is_valid, error = validate_future_date(visit_date, 'Visit date')
            if not is_valid:
                return None, error
            
            visit.visit_date = visit_date
        
        # Update other fields
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
        
        return visit, None
    
    @staticmethod
    def delete_visit(visit):
        """Delete a visit"""
        db.session.delete(visit)
        db.session.commit()
        return True
    
    @staticmethod
    def _validate_visit_data(data):
        """Validate visit data"""
        if not data.get('visit_date') or not data.get('reason'):
            return None, 'visit_date and reason are required'
        
        # Validate reason
        is_valid, error = validate_string_length(data.get('reason'), 'Reason', min_length=1, max_length=200)
        if not is_valid:
            return None, error
        
        # Validate visit_date
        is_valid, visit_date, error = validate_date(data.get('visit_date'), 'Visit date')
        if not is_valid:
            return None, error
        
        # Check if not in future
        is_valid, error = validate_future_date(visit_date, 'Visit date')
        if not is_valid:
            return None, error
        
        return visit_date, None
