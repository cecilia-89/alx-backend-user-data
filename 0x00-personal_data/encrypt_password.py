"""Module: encrypt password"""
import bcrypt

def hash_password(password):
    """returns a hashed password"""
    encoded = password.encode()
    return bcrypt.hashpw(encoded, bcrypt.gensalt)


def is_valid(hashed_password, password):
    """determines if a password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)