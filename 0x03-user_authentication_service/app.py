#!/usr/bin/env python3
""" Flask app module """
from auth import Auth
from db import DB
from flask import abort, Flask, jsonify, request

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    A simple route that
    returns a JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    End point to register a user

    Args:
        email(str): User's email
        password(str): User's password
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": new_user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login session

    Args:
        email(str): User's email
        password(str): User's password
    """
    email = request.form.get('email')
    # print(f'Email is {email}')
    password = request.form.get('password')
    # print(f'Email is {email} and Passowrd is {password}')

    if not AUTH.valid_login(email, password):
        # print(f'Aborting.....')
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Route to logout the user by deleting the session ID.

    If the user is found with the session ID, destroy the session
    and redirect to the home page.
    If the user is not found, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    except NoResultFound:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    The method request is expected to contain a session_id cookie
    """
    try:
        session_id = request.cookies.get('session_id')
        # print(f'Session ID: {session_id}')
        if not session_id:
            abort(403)

        user = AUTH.get_user_from_session_id(session_id)
        # print(f'User: {user}')
        if user:
            return jsonify({"email": user.email}), 200
        else:
            # print(f'Aborting...')
            abort(403)
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """
    Endpoint to handle password reset requests
    """
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """
    Endpoint to handle password update requests
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
