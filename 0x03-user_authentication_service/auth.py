#!/usr/bin/env python3
""" Authentication module """
import bcrypt


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
