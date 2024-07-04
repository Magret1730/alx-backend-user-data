#!/usr/bin/env python3
""" Password hash """
import bcrypt


def hash_password(password):
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
