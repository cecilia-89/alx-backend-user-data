#!/usr/bin/env python3
"""Module: Session Authentic"""
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from models.user import User
from os import getenv
from flask import request, jsonify
import uuid


class SessionAuth(Auth):
    """Authenticates class using session"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates session_id for a user_id"""
        if user_id is not None and type(user_id) == str:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns User id based on a session_id"""
        if session_id is not None and type(session_id) == str:
            user_id = self.user_id_by_session_id.get(session_id)
            if user_id is not None:
                return user_id
            return None

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """handles session authentication"""
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({ "error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({ "error": "no user found for this email" }), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)

    result = jsonify(user[0].to_json())
    result.set_cookie(getenv('SESSION_NAME'), session_id)
    return result


