#!/usr/bin/env python3
""" Authentication module """
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
    Method takes in a password string and returns bytes

    Args:
        password(str): Password to hash

    Returns:
        bytes, a salted hash of the input password
    """
    # Convert passowrd to array of bytes
    pwd_bytes = password.encode('utf-8')

    # Generate salt
    salt = bcrypt.gensalt()

    # Hash password
    pwd = bcrypt.hashpw(pwd_bytes, salt)

    return pwd


def _generate_uuid() -> str:
    """
    This method returns a string representation of a new UUID created
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialization
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        This method registers a user in the database

        Args:
            email(str): Email of the user
            password(str): Password of the user

        Returns:
            User object

        Raises:
            ValueError: If a user already exist with the passed email
        """
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f'User {email} already exists')

        # Hash new user password
        hashed_pwd = _hash_password(password)

        # Create a new user instance
        new_user = User(email=email, hashed_password=hashed_pwd)

        # Add and commit the new user to the database
        self._db.add_user(email, hashed_pwd)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login

        Args:
            email(str): Email of user
            Password(str): User's password

        Return:
            bool: True if password matches, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                # encoding user password
                passwrd = password.encode('utf-8')

                # Get the user password from db
                pwd = user.hashed_password

                if bcrypt.checkpw(passwrd, pwd):
                    return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        This method creates session based on email

        Arg:
            email(str): User's email

        Return:
            str: the session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user_id = _generate_uuid()
                self._db.update_user(user.id, session_id=user_id)
                return user_id
        except NoResultFound:
            return None

    def get_user_from_session_id(session_id: str) -> User:
        """
        Method that finds user by session ID

        Args:
            session_id(str): Session ID of the user

        Returns:
            User or None if no session ID is found
        """
        if session_id is None:
            return None
        try:
            user = DB.find_user_by(session_id)
        except NoResultFound:
            return None:

        return user

