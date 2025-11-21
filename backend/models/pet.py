from extensions import db
from datetime import datetime

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)  # dog, cat, bird, etc.
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)  # in kg
    photo_url = db.Column(db.String(255))
    tags = db.Column(db.String(255))  # comma-separated tags
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    feeding_schedules = db.relationship('FeedingSchedule', backref='pet', lazy=True, cascade='all, delete-orphan')
    vet_visits = db.relationship('VetVisit', backref='pet', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Pet {self.name} ({self.species})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'age': self.age,
            'weight': self.weight,
            'photo_url': self.photo_url,
            'tags': self.tags.split(',') if self.tags else [],
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }
