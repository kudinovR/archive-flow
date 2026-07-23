from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()


def register_user(data: dict) -> tuple[dict, int]:
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 409

    user = User(
        email=email,
        password_hash=ph.hash(password)
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

    if not user:
        return {"error": "Invalid email or password"}, 401

    try:
        ph.verify(user.password_hash, password)
    except VerifyMismatchError:
        return {"error": "Invalid email or password"}, 401
    
     # Rehash check
    try:
        if ph.check_needs_rehash(user.password_hash):
            user.password_hash = ph.hash(password)
            db.session.commit()
    except Exception:
        db.session.rollback()
    
    token = create_access_token(identity=str(user.id))
    return {"access_token": token, "role": user.role}, 200

