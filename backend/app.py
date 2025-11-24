from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    with app.app_context():
        # Import routes
        from routes import auth, pets, schedules, visits
        
        # Register blueprints
        app.register_blueprint(auth.bp)
        app.register_blueprint(pets.bp)
        app.register_blueprint(schedules.bp)
        app.register_blueprint(visits.bp)
        
        # Create database tables
        db.create_all()
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'The requested resource was not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        # Log the error here in production
        app.logger.error(f'Unhandled exception: {str(error)}')
        return jsonify({'error': 'An error occurred', 'message': str(error)}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
