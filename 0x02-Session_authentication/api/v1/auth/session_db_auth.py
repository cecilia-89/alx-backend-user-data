#!/usr/bin/env python3
"""Module: Session database Expiration"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """database expiration class"""

    def create_session(self, user_id=None):
        """creates a user session"""
        session_id = super().create_session(user_id)
        if session_id:
            u = UserSession(**{'user_id': user_id, 'session_id': session_id})
            u.save()
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID"""
        user_id = self.user_id_for_session_id.get(session_id)
        return user_id

    def destroy_session(self, request=None):
        """destroys the UserSession"""
        return super().destroy_session(request)
