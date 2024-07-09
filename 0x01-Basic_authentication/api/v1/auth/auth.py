#!/usr/bin/env python3
""" Authentication class module """
from flask import request
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
        return request
