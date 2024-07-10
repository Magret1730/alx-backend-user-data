#!/usr/bin/env python3
""" Test file """


from api.v1.auth.session_auth import SessionAuth

def test_inheritance():
    """ Test to validate inheritance from Auth """
    session_auth = SessionAuth()
    assert isinstance(session_auth, SessionAuth)
    assert isinstance(session_auth, Auth)
    print("SessionAuth inherits correctly from Auth.")

if __name__ == "__main__":
    test_inheritance()
