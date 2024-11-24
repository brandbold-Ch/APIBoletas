from errors.errors import IncorrectUserError
from fastapi.requests import Request
from utils.token import verify_token
from functools import wraps
from typing import Callable


def authenticate(func: Callable) -> Callable:
    """
    A decorator to authenticate requests based on a token and user enrollment information.

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
            **kwargs: Keyword arguments passed to the decorated function. It must include the 'request'
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
        else:
            raise IncorrectUserError()
    return wrapper
