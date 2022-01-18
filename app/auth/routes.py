from app import jwt
from app.auth import bp
from app.auth.helpers import get_users, get_user, add_user, remove_user, encrypt_pwd, check_pwd
from example_authentication.app.auth.models import Users, InvalidToken
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required


@jwt.token_in_blocklist_loader
def check_if_blacklisted_token(data, decrypted):
    """
    Decorator designed to check for blacklisted tokens
    """
    jti = decrypted['jti']
    return InvalidToken.is_invalid(jti)


@bp.route("/api/login", methods=["POST"])
def login():
    """
    User login end-point accepts email and password.
    returns jwt_token
    """
    try:
        username = request.json["username"]
        pwd = request.json["pwd"]
        if username and pwd:
            user = list(filter(lambda x: x["username"] == username and check_pwd(pwd, x["pwd"]), get_users()))
            if len(user) == 1:
                token = create_access_token(identity=user[0]["id"])
                refresh_token = create_refresh_token(identity=user[0]["id"])
                return jsonify({"token": token, "refreshToken": refresh_token})
            else:
                return jsonify({"error": "Invalid credentials"})
        else:           
            return jsonify({"error":"Invalid Form"})
    except:
        return jsonify({"error": "Invalid Form"})


@bp.route("/api/register", methods=["POST"])
def register():
    """
    End-point to handle user registration, encrypting the password and validating the email
    """
    try:
        pwd = encrypt_pwd(request.json['pwd'])
        username = request.json['username']
        
        users = get_users()
        if len(list(filter(lambda x: x["username"] == username, users))) == 1:         
            return jsonify({"error": "Invalid Form"})
        add_user(username, pwd)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


@bp.route("/api/checkiftokenexpire", methods=["POST"])
@jwt_required()
def check_if_token_expire():
    """
    End-point for frontend to check if the token has expired or not
    """
    return jsonify({"success": True})


@bp.route("/api/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    End-point to refresh the token when required
    
    """
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token})


@bp.route("/api/getcurrentuser")
@jwt_required()
def current_user():
    """
    End-point to handle collecting the current user information
    """
    uid = get_jwt_identity()
    return jsonify(get_user(uid))


@bp.route("/api/logout/access", methods=["POST"])
@jwt_required()
def access_logout():
    """
    End-point to log the user out and Invalidate the token.
    """
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success":True})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)e})


@bp.route("/api/logout/refresh", methods=["POST"])
@jwt_required()
def refresh_logout():
    """
    End-point to invalidate the token.
    Can be used with both log the user out or for the frontend to call after refreshing the token.

    """
    
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


@bp.route("/api/deleteaccount", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    End-point to handle removal of users
    """
    try:
        user = get_user(get_jwt_identity())
        remove_user(user.id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})