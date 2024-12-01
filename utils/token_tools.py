"""
This module provides utility functions and a custom HTTPBearer class to handle
Bearer token authentication in FastAPI.

The module includes the following functionalities:

1. **CustomHTTPBearer**:
   - A subclass of `HTTPBearer` that overrides the `__call__` method to extract the
     authorization token from incoming requests.
   - If the token is missing from the request, it raises a `NotFoundTokenError`.
   - If the token is found, it stores the token in the request's state.

2. **create_token**:
   - This function generates a JSON Web Token (JWT) using the provided payload.
   - The generated token has an expiration time set to 7 days from the current time.
   - The token is encoded using the HS256 algorithm and a predefined secret key.

3. **verify_token**:
   - This function verifies the validity of a JWT by decoding it.
   - If the token is expired, it raises an `ExpiredTokenError`.
   - If the token is invalid or the signature doesn't match, it raises an `InvalidTokenError`.
   - If valid, it returns the decoded payload of the token.

Dependencies:
- `fastapi.requests.Request`: For extracting and handling HTTP request objects.
- `jose.jwt`: To encode and decode JWT tokens.
- `fastapi.security.HTTPBearer` and `HTTPAuthorizationCredentials`: For handling Bearer token security in FastAPI.
- Custom error classes (`NotFoundTokenError`, `ExpiredTokenError`, `InvalidTokenError`) to handle specific token errors.

The utility functions and custom bearer class allow FastAPI to securely handle and authenticate requests using Bearer
tokens.
"""

from datetime import datetime, timedelta
from fastapi.requests import Request
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from errors.errors import NotFoundTokenError, ExpiredTokenError, InvalidTokenError
from utils.config import Config


class CustomHTTPBearer(HTTPBearer):
    """
    A custom HTTPBearer class to handle bearer token authorization in FastAPI.

    This class overrides the `__call__` method to extract the authorization token
    from incoming requests. It handles cases where the token is missing or invalid
    by raising appropriate errors.

    Methods:
        __call__(self, request: Request) -> HTTPAuthorizationCredentials:
            Extracts and validates the token from the incoming request.
            If the token is missing, raises a `NotFoundTokenError`.
    """

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """
        Extracts the Bearer token from the request headers and assigns it to the request's state.

        Args:
            request (Request): The incoming HTTP request object.

        Raises:
            NotFoundTokenError: If the authorization token is missing from the request.

        Returns:
            HTTPAuthorizationCredentials: The credentials object containing the token.
        """
        self.auto_error = False
        credentials = await super().__call__(request)

        if credentials is None:
            raise NotFoundTokenError()

        request.state.token = credentials.credentials
        return credentials


def create_token(payload: dict) -> str:
    """
    Creates a JWT token with the provided payload and an expiration date.

    This function generates a token that includes the provided payload and an
    expiration date set to 7 days from the current time. The token is encoded using
    the HS512 algorithm and a predefined secret key.

    Args:
        payload (dict): The payload data to be encoded in the JWT token.

    Returns:
        str: The encoded JWT token as a string.
    """
    expire = datetime.utcnow() + timedelta(days=Config.TOKEN_EXPIRE_DAYS)
    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=Config.ALGORITHM
    )


def verify_token(token: str) -> dict:
    """
    Verifies the authenticity of the provided JWT token and decodes it.

    This function attempts to decode the provided JWT token using the HS256 algorithm.
    If the token is expired or invalid, it raises the corresponding error
    (`ExpiredTokenError` or `InvalidTokenError`).

    Args:
        token (str): The JWT token to be verified and decoded.

    Raises:
        ExpiredTokenError: If the token has expired.
        InvalidTokenError: If the token is invalid or the signature doesn't match.

    Returns:
        dict: The decoded payload of the JWT token if valid.
    """
    try:
        return jwt.decode(
            token, Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )

    except JWTError as e:
        if str(e) == "Signature has expired.":
            raise ExpiredTokenError() from e
        raise InvalidTokenError() from e
