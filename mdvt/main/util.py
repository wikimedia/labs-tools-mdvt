from flask import session


def is_logged_in():
    return all(key in session for key in ['user_id', 'username'])
