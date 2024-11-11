from errors.errors import IncorrectUserError
from fastapi.requests import Request
from utils.token import verify_token
from functools import wraps
from typing import Callable


def authenticate(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        user_req: dict = verify_token(request.headers.get("authorization")[7:])

        if user_req["enrollment"] == kwargs.get("enrollment"):
            return await func(*args, **kwargs)
        else:
            raise IncorrectUserError()
    return wrapper
