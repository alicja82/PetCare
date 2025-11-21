from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os

bp = Blueprint('pets', __name__, url_prefix='/api/pets')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/', methods=['GET'])
@jwt_required()
def get_pets():
    """Get all pets for the current user"""
    from app import db
    from models.pet import Pet
    
    current_user_id = get_jwt_identity()
    pets = Pet.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'pets': [pet.to_dict() for pet in pets]
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_pet():
    """Create a new pet"""
    from app import db
    from models.pet import Pet
    
    current_user_id = get_jwt_identity()
    
    # Check if request has file
    photo_url = None
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Create upload folder if it doesn't exist
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            photo_url = f'/uploads/{filename}'
    
    # Get data from form or JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    # Validate required fields
    if not data.get('name') or not data.get('species'):
        return jsonify({'error': 'Name and species are required'}), 400
    
    # Handle tags - convert list to comma-separated string
    tags = data.get('tags', [])
    if isinstance(tags, list):
        tags = ','.join(tags)
    
    # Create new pet
    new_pet = Pet(
        name=data.get('name'),
        species=data.get('species'),
        breed=data.get('breed'),
        age=data.get('age'),
        weight=data.get('weight'),
        photo_url=photo_url,
        tags=tags,
        notes=data.get('notes'),
        user_id=current_user_id
    )
    
    db.session.add(new_pet)
    db.session.commit()
    
    return jsonify({
        'message': 'Pet created successfully',
        'pet': new_pet.to_dict()
    }), 201

@bp.route('/<int:pet_id>', methods=['GET'])
@jwt_required()
def get_pet(pet_id):
    """Get a specific pet by ID"""
    from app import db
    from models.pet import Pet
    
    current_user_id = get_jwt_identity()
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify({'pet': pet.to_dict()}), 200

@bp.route('/<int:pet_id>', methods=['PUT'])
@jwt_required()
def update_pet(pet_id):
    """Update a pet"""
    from app import db
    from models.pet import Pet
    
    current_user_id = get_jwt_identity()
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Handle photo upload
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            # Delete old photo if exists
            if pet.photo_url:
                old_photo_path = os.path.join(current_app.root_path, pet.photo_url.lstrip('/'))
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            pet.photo_url = f'/uploads/{filename}'
    
    # Get data from form or JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    # Update fields if provided
    if 'name' in data:
        pet.name = data['name']
    if 'species' in data:
        pet.species = data['species']
    if 'breed' in data:
        pet.breed = data['breed']
    if 'age' in data:
        pet.age = data['age']
    if 'weight' in data:
        pet.weight = data['weight']
    if 'notes' in data:
        pet.notes = data['notes']
    if 'tags' in data:
        tags = data['tags']
        if isinstance(tags, list):
            tags = ','.join(tags)
        pet.tags = tags
    
    db.session.commit()
    
    return jsonify({
        'message': 'Pet updated successfully',
        'pet': pet.to_dict()
    }), 200

@bp.route('/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    """Delete a pet"""
    from app import db
    from models.pet import Pet
    
    current_user_id = get_jwt_identity()
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    # Delete photo if exists
    if pet.photo_url:
        photo_path = os.path.join(current_app.root_path, pet.photo_url.lstrip('/'))
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    db.session.delete(pet)
    db.session.commit()
    
    return jsonify({'message': 'Pet deleted successfully'}), 200
