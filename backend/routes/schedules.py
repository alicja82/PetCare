# Placeholder for schedules routes
from flask import Blueprint

bp = Blueprint('schedules', __name__, url_prefix='/api/schedule')

@bp.route('/', methods=['GET'])
def get_schedules():
    return {'message': 'Schedules endpoint - placeholder'}
