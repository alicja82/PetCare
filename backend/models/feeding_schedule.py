from extensions import db
from datetime import datetime

class FeedingSchedule(db.Model):
    __tablename__ = 'feeding_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    
    food_type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50))  # e.g., "200g", "1 cup"
    time = db.Column(db.Time, nullable=False)  # scheduled time
    frequency = db.Column(db.String(50))  # e.g., "daily", "twice a day"
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FeedingSchedule Pet:{self.pet_id} at {self.time}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'food_type': self.food_type,
            'amount': self.amount,
            'time': self.time.strftime('%H:%M'),
            'frequency': self.frequency,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
