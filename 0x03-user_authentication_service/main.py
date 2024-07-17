#!/usr/bin/env python3
""" Main file to test all url"""


import requests

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(f"{BASE_URL}/users",
                             data={"email": email, "password": password})
    assert response.status_code == 200, f"200, got {response.status_code}"
    # print("User registered successfully.")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with wrong password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401, f"401, got {response.status_code}"
    # print("Login with wrong password correctly failed.")


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200, f"200, got {response.status_code}"
    assert "session_id" in response.cookies, "Session ID not found in cookies"
    # print("Login successful.")
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Access profile without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"403, got {response.status_code}"
    # print("Access to profile without logging in correctly failed.")


def profile_logged(session_id: str) -> None:
    """Access profile with a valid session ID."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"200, got {response.status_code}"
    # print("Access to profile with valid session ID successful.")


def log_out(session_id: str) -> None:
    """Log out with a valid session ID."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"200, got {response.status_code}"
    # print("Logout successful.")


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200, f"200, got {response.status_code}"
    response_json = response.json()
    assert "reset_token" in response_json, "Reset token not found in response"
    # print("Password reset token obtained successfully.")
    return response_json["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using reset token."""
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={"email": email,
                                  "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200, f"200, got {response.status_code}"
    # print("Password updated successfully.")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
