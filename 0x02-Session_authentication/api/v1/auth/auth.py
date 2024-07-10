#!/usr/bin/env python3
""" Authentication class module """
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """
    Authentication class module
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Requires authentication
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path by removing trailing slash
        if path[-1] == '/':
            path = path[:-1]

        # Check if the path is in the excluded_paths list
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '/':
                excluded_path = excluded_path[:-1]
            # Handle wildcard matching
            if excluded_path.endswith('*'):
                # Remove the '*' and compare prefix
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Authorization for current user
        """
        return None

    def session_cookie(self, request=None):
        """
        Method that returns a cookie value from a request
        """
        if request is None:
            return None
        # Get the cookie name from the environment variable
        cookie_name = getenv('SESSION_NAME', '_my_session_id')
        # Return the value of the cookie named cookie_name from request
        return request.cookies.get(cookie_name)
