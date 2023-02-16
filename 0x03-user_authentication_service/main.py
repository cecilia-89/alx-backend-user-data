#!/usr/bin/env python3
"""main.py module
"""
import requests
from flask import jsonify

url = 'http://127.0.0.1:5000/'


def register_user(email: str, password: str) -> None:
    """registers a user"""
    data = {'email': email, 'password': password}
    response = requests.post(url + 'users', data=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    data = {'email': email, 'password': password}
    response = requests.post(url + 'sessions', data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """returns an unlogged user"""
    response = requests.get(url + 'profile')
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """logs in a user"""
    data = {'email': email, 'password': password}
    response = requests.post(url + 'sessions', data=data)
    assert response.json() == {'email': email, 'message': 'logged in'}
    return response.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """returns a logged user"""
    data = {'session_id': session_id}
    response = requests.get(url + 'profile', cookies=data)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """logs out a user"""
    data = {'session_id': session_id}
    response = requests.delete(url + 'sessions', cookies=data)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """resets a users password"""
    response = requests.post(url + 'reset_password', data={'email': email})
    assert response.status_code == 200
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """updates a user's password"""
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url + 'reset_password', data=data)
    assert response.status_code == 200


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
