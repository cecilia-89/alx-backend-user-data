#!/usr/bin/env python3
""" Main 100
"""
from api.v1.auth.auth import Auth

a = Auth()
print(a.require_auth("/api/v1/users", ["/api/v1/stat*"]))