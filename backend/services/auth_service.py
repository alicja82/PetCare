"""
Authentication service - Business logic for user authentication
"""
from models.user import User
from flask_jwt_extended import create_access_token
from utils.validators import validate_email, validate_username, validate_password

class AuthService:
    
    @staticmethod
    def register_user(data):
        """Register a new user"""
        from app import db, bcrypt
        
        # Validate input
        errors = AuthService._validate_registration_data(data)
        if errors:
            return None, None, errors
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return None, None, 'Username already exists'
        
        if User.query.filter_by(email=data['email']).first():
            return None, None, 'Email already exists'
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create token
        access_token = create_access_token(identity=new_user.id)
        
        return new_user, access_token, None
    
    @staticmethod
    def login_user(data):
        """Login user and return JWT token"""
        from app import bcrypt
        
        # Validate input
        if not data or not data.get('username') or not data.get('password'):
            return None, None, 'Username and password are required'
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user:
            return None, None, 'Invalid username or password'
        
        # Check password
        if not bcrypt.check_password_hash(user.password_hash, data['password']):
            return None, None, 'Invalid username or password'
        
        # Create token
        access_token = create_access_token(identity=user.id)
        
        return user, access_token, None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def _validate_registration_data(data):
        """Validate registration data"""
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return 'Username, email and password are required'
        
        # Validate username
        is_valid, error = validate_username(data.get('username'))
        if not is_valid:
            return error
        
        # Validate email
        is_valid, error = validate_email(data.get('email'))
        if not is_valid:
            return error
        
        # Validate password
        is_valid, error = validate_password(data.get('password'))
        if not is_valid:
            return error
        
        return None
