"""
This module provides an authentication decorator for FastAPI to validate requests.

The primary functionality of this module is:
- Validating JWT tokens from the 'Authorization' header in incoming requests.
- Ensuring that the user enrollment in the token matches the expected enrollment.

Components:
- The `authenticate` decorator: Wraps a function to add authentication logic.
- Custom error handling: Raises `IncorrectUserError` if validation fails.
"""

from functools import wraps
from typing import Callable
from fastapi.requests import Request
from errors.errors import IncorrectUserError
from utils.token import verify_token


def authenticate(func: Callable) -> Callable:
    """
    A decorator to authenticate requests based on a token and user
    enrollment information.

    This decorator validates the JWT token provided in the 'Authorization' header of the request
    and checks whether the user enrollment matches the enrollment specified in the request.

    Args:
        func (Callable): The function to be wrapped by the decorator.

    Returns:
        Callable: The wrapped function with authentication logic.

    Raises:
        IncorrectUserError: If the user's enrollment does not match the expected enrollment.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Callable:
        """
        Inner function that handles authentication before executing the decorated function.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.
                      It must include the 'request'
                      object from FastAPI and the 'enrollment' key for comparison.

        Returns:
            The result of the decorated function if authentication is successful.

        Raises:
            IncorrectUserError: If the user's enrollment does not match the expected enrollment.
        """
        request: Request = kwargs.get("request")
        user_req: dict = verify_token(request.headers.get("authorization")[7:])

        if user_req["enrollment"] == kwargs.get("enrollment"):
            return await func(*args, **kwargs)
        raise IncorrectUserError()

    return wrapper
