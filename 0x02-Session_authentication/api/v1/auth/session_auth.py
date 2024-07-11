#!/usr/bin/env python3
""" Session Authentication Module """
from api.v1.auth.auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Function that returns a User ID based on a Session ID

        Args:
            session_id (str): The session ID used to return user_id

        Returns:
            str: User ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        # Returns user_id based on provided session_id
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """
        Method that returns a User instance based on cookie value

        Args:
            request (Request): The Flask request object.

        Returns:
            User: The user instance if the session ID is valid, else None.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        print(f"Session_id:   {session_id}")
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id is None:
            return None
        print(f"User_id:   {user_id}")
        user = User.get(user_id)
        print(f"User:  {user}")
        return user
