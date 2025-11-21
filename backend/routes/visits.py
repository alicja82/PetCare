# Placeholder for visits routes
from flask import Blueprint

bp = Blueprint('visits', __name__, url_prefix='/api/visits')

@bp.route('/', methods=['GET'])
def get_visits():
    return {'message': 'Visits endpoint - coming soon'}
