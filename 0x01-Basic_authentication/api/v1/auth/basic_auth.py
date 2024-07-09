#!/usr/bin/env python3
""" BasicAuth module that inherits from Auth """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ BasicAuth module that inherits from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Method that returns the Base64 part of the Authorization header for
        a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Method that returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Method that returns the user email and password from
        the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        # Split only on the first occurrence of ':'
        parts = decoded_base64_authorization_header.split(':', 1)

        # Check if we have exactly two parts
        if len(parts) != 2:
            return None, None

        email, password = parts
        return email, password
        # email = decoded_base64_authorization_header.rsplit(":")[0]
        # password = decoded_base64_authorization_header.rsplit(":")[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Method that returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method that overloads Auth and retrieves the User
        instance for a request
        """
        auth_header = self.authorization_header(request)
        # print("Auth_header: ", auth_header)
        if auth_header:
            base = self.extract_base64_authorization_header(auth_header)
            # print("extract_base: ", extract_base)
            if base:
                decoded = self.decode_base64_authorization_header(base)
                # print("decoded_value: ", decoded_value)
                if decoded:
                    credentials = self.extract_user_credentials(decoded)
                    # print("User_credentials:", user_credentials)
                    if credentials:
                        email = credentials[0]
                        pwd = credentials[1]
                        user = self.user_object_from_credentials(email, pwd)
                        return user
        return None
