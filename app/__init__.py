from flask import Flask
from app.database import db
from app.routes import api_bp

def create_app():
    """Application factory engine"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../workout_spec_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind active extensions
    db.init_app(app)

    # Mount the endpoints blueprint
    app.register_blueprint(api_bp)

    # Initialize tables inside application environment safely
    with app.app_context():
        db.create_all()

    return app
