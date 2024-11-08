from dbfmapper.exception.exceptions import NotFoundTable
from errors.errors import NotFoundEntity
from typing import Callable


def exception_handler(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)
        except NotFoundTable as e:
            raise NotFoundEntity() from e
    return wrapper
