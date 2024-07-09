#!/usr/bin/env python3
""" BasicAuth module that inherits from Auth """
from api.v1.auth.auth import Auth
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
        email = decoded_base64_authorization_header.rsplit(":")[0]
        password = decoded_base64_authorization_header.rsplit(":")[1]
        return email, password
