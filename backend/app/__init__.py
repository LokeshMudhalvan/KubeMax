from flask import Flask 
from flask_cors import CORS 
from flask_jwt_extended import JWTManager
from .config import Config
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    logging.basicConfig(level=logging.INFO)
    
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    return app 