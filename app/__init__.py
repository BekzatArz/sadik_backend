from flask import Flask
from app.extensions import db, migrate
from flask_cors import CORS
from app.routes import register_routes
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    cors_origins = [
        'http://localhost:5173',
        'http://192.168.144.22:5173',
        'http://192.168.1.121:5000',
        'http://26.249.250.5:5173',
    ]
    CORS(app, origins=cors_origins, supports_credentials=True)
    
    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    return app
    
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)