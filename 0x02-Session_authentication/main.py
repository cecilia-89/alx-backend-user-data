#!/usr/bin/env python3
from flask import request
""" Main 4
"""
from api.v1.auth.session_db_auth import SessionDBAuth
s = SessionDBAuth()
s.destroy_session("request")