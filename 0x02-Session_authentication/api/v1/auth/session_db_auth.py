#!/usr/bin/env python3
"""Module: Session database Expiration"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """database expiration class"""

    def create_session(self, user_id=None):
        """creates a user user session"""
        u = UserSession()

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID"""
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return user_id

    def destroy_session(self, request=None):
        """destroys the UserSession"""
        super().destroy_session(request)