#!/usr/bin/env python3
"""Module: authentition"""
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in excluded_p aths"""

        if path is not None and excluded_paths is not None:
            for url in excluded_paths:
                if url[-1] == '*':
                    if path.startswith(url[:-1]):
                        return False
            if path[-1] != "/":
                path = path + "/"
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validates all requests to secure the API"""
        if request is not None:
            dict_key = request.headers.get('Authorization')
            if dict_key is not None:
                return dict_key
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user"""
        return None
