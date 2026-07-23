from flask import request, jsonify
from flask_jwt_extended import set_access_cookies, jwt_required, get_jwt

from . import auth_bp
from app.services.auth_service import register_user, login_user
from app.services.token_blacklist import revoke_token


@auth_bp.post("/register")
def register():
    data = request.get_json()
    result, status = register_user(data)
    return jsonify(result), status


@auth_bp.post("/login")
def login():
    data = request.get_json()
    result, status = login_user(data)

    response = jsonify(result)
    if status == 200 and "access_token" in result:
        set_access_cookies(response, result["access_token"])

    return response, status


@auth_bp.post("/logout")
@jwt_required()
def logout():
    jwt_payload = get_jwt()
    revoke_token(jwt_payload)
    return jsonify({"msg": "Successfully logged out"}), 200
