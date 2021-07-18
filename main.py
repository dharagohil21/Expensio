from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from src.common.models import db


def init_app(config_module: str):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config_module)

    # database configuration
    db.init_app(app)

    return app