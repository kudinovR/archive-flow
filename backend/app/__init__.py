from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, jwt, migrate, init_redis


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    init_redis(app)

    CORS(app, origins=app.config["CORS_ORIGINS"])

    from .models import User, Document, Category
    from .api import register_blueprints

    register_blueprints(app)
    return app
