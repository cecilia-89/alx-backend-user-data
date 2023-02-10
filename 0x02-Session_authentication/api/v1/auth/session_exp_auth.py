#!/usr/bin/env python3
"""Module: Session Expiration"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta

class SessionExpAuth(SessionAuth):
    """adds expiration date to a session"""

    def __init__(self):
        """constructor class"""
        try:
            duration = int(getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """creates a session id"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = "session dictionary"
            self.user_id_by_session_id["user_id"] = user_id
            self.user_id_by_session_id["created_at"] = datetime.now()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns user id for session"""
        session_value = self.user_id_by_session_id.get(session_id)
        if session_value is None:
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id['user_id']

        created_at = self.user_id_by_session_id.get('created_at')
        if created_at:
            created_at += timedelta(seconds=self.session_duration)
            if created_at <= datetime.now():
                return self.user_id_by_session_id['user_id']
        return None
