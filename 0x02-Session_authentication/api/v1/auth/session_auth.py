#!/usr/bin/env python3
""" Session Authentication Module """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth class that inherits Auth """

    # Class attribute to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Function that creates a Session ID for a user_id

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The Session ID if user_id is valid, else None.
        """
        # Check if user_id is None or not a string
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id
