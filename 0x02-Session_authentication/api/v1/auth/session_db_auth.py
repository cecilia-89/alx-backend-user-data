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
            UserSession.save_to_file()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_obj = UserSession.search({'session_id': session_id})
        if user_obj:
            return user_obj[0].user_id

    def destroy_session(self, request=None):
        """destroys a session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_session = UserSession.search({
            'session_id': session_id
        })

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
