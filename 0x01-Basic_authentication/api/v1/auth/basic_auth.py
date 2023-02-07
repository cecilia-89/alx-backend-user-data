#!/usr/bin/env python3
"""Module: Basic Auth"""
import uuid
import hashlib
from api.v1.auth.auth import Auth
from typing import TypeVar, Tuple
from models.user import User
import re
import base64


class BasicAuth(Auth):
    """class for basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extracts basic auth password from header"""
        auth_header = authorization_header
        if auth_header is not None and type(auth_header) == str:
            if auth_header.startswith("Basic "):
                return auth_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a Base64 string"""
        base64_header = base64_authorization_header
        if base64_header is not None and type(base64_header) == str:
            try:
                base64_bytes = base64_header.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                return message_bytes.decode('ascii')
            except Exception:
                pass
        return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """extracts and returns user credentials"""
        decoded_base = decoded_base64_authorization_header
        if decoded_base is not None and type(decoded_base) == str:
            if ':' in decoded_base:
                email = re.match('(.+):', decoded_base)[1]
                password = re.match('.+:(.+)', decoded_base)[1]
                return (email, password)

        return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns user with the currect credentials"""
        for param in [user_pwd, user_email]:
            if param is None or type(param) != str:
                return None
        for user in User.search():
            user_pwd = hashlib.sha256(user_pwd.encode()).hexdigest().lower()
            if user.email == user_email and user.password == user_pwd:
                return user
        return None
