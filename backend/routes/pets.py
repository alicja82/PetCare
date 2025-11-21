# Placeholder for pets routes
from flask import Blueprint

bp = Blueprint('pets', __name__, url_prefix='/api/pets')

@bp.route('/', methods=['GET'])
def get_pets():
    return {'message': 'Pets endpoint - placeholder'}
