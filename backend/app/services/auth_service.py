from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


def register_user(data: dict) -> tuple[dict, int]:
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully", "id": str(user.id)}, 201


def login_user(data: dict) -> tuple[dict, int]:
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(identity=str(user.id))
    return {"access_token": token, "role": user.role}, 200
