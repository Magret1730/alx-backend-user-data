#!/usr/bin/env python3
""" Session Module """
from flask import abort, jsonify, make_response, request
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """
    POST /auth_session/login

    Method handles all route for session authentication
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not user_email or user_email is None:
        return jsonify({"error": "email missing"}), 400

    if not user_password or user_password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': user_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    print(f"Session_id:  {session_id}")
    if not session_id:
        abort(500)

    response = make_response(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout() -> str:
    """
    DELETE /auth_session/logout

    Handle user logout via session authentication.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
