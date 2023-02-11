#!/usr/bin/env python3
""" Main 4
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
s = SessionExpAuth()
print(s.user_id_for_session_id('kkkk'))