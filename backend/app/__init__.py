from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, jwt, migrate


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    from .api import register_blueprints
    register_blueprints(app)

    return app