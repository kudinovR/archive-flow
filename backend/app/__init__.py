from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, jwt, migrate, init_redis
from .services.token_blacklist import is_token_revoked


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

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(_jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)
    
    return app
