from flask import request, jsonify
from . import auth_bp
from app.services.auth_service import register_user, login_user


@auth_bp.post("/register")
def register():
    data = request.get_json()
    result, status = register_user(data)
    return jsonify(result), status


@auth_bp.post("/login")
def login():
    data = request.get_json()
    result, status = login_user(data)
    return jsonify(result), status
