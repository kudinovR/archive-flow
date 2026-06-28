from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.extensions import db, jwt, migrate


def test_extension_instances_are_initialized_as_singletons():
    assert isinstance(db, SQLAlchemy)
    assert isinstance(jwt, JWTManager)
    assert isinstance(migrate, Migrate)
