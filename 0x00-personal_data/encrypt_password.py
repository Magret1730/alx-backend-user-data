#!/usr/bin/env python3
""" Password hash """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Function to hash password

    Arg:
    Password: password to hash
    """

    # converting password to array of bytes
    passwrd_bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    passwrd = bcrypt.hashpw(passwrd_bytes, salt)

    return passwrd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Function to check if password is correct
    """

    # encoding user password
    userBytes = password.encode('utf-8')

    # checking password
    result = bcrypt.checkpw(userBytes, hashed_password)

    return result
