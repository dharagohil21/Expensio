from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from src.common.models import db
from flask_jwt_extended import JWTManager


def init_app(config_module: str):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config_module)

    # database configuration
    db.init_app(app)
    jwt = JWTManager(app)

    return app
