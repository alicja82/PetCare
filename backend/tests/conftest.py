# Test configuration and fixtures
import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from models.user import User
from models.pet import Pet
from models.feeding_schedule import FeedingSchedule
from models.vet_visit import VetVisit

@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    from app import bcrypt
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=bcrypt.generate_password_hash('TestPass123!').decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def sample_pet(app, sample_user):
    """Create a sample pet for testing."""
    pet = Pet(
        name='Buddy',
        species='Dog',
        breed='Golden Retriever',
        age=3,
        weight=30.5,
        user_id=sample_user.id
    )
    db.session.add(pet)
    db.session.commit()
    return pet
