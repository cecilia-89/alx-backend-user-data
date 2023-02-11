#!/usr/bin/env python3
""" Main 4
"""
from api.v1.auth.session_db_auth import SessionDBAuth
s = SessionDBAuth()
s.user_id_for_session_id('39381576-ccdf-4fca-9e55-af8791261a9c')