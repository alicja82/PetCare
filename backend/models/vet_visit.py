from app import db
from datetime import datetime

class VetVisit(db.Model):
    __tablename__ = 'vet_visits'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    
    visit_date = db.Column(db.DateTime, nullable=False)
    vet_name = db.Column(db.String(100))
    clinic_name = db.Column(db.String(150))
    reason = db.Column(db.String(200), nullable=False)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    medications = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VetVisit Pet:{self.pet_id} on {self.visit_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'visit_date': self.visit_date.isoformat(),
            'vet_name': self.vet_name,
            'clinic_name': self.clinic_name,
            'reason': self.reason,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'medications': self.medications,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
