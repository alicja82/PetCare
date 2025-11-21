from flask import Flask
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
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
