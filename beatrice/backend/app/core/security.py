"""Security utils.

This module contains utility functions related to password and
authentication tokens management.
"""

import datetime

from passlib import context
import jose

from app.core import config

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the match between the given plain and hashed passwords.

    Args:
        plain_password: The password in plain text.
        hashed_password: The hashed password.

    Returns:
        True if the passwords match.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Returns the hash for the given password.

    Args:
        password: The password in plain text.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict,
                        expires_delta: datetime.timedelta | None = None):
    """Returns an encoded JWT token.

    Args:
        data: The data to encode.
        expires_delta: The token's lifetime expressed in minutes.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jose.jwt.encode(to_encode,
                                  config.settings.SECRET_KEY,
                                  algorithm=ALGORITHM)

    return encoded_jwt
