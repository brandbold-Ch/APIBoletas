from dbfmapper.exception.exceptions import (
    NotFoundTable, DatabaseNotFound, DBFException
)
from errors.errors import NotFoundEntity, DatabaseError
from typing import Callable


def exception_handler(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)

        except NotFoundTable as e:
            raise NotFoundEntity(e) from e

        except DatabaseNotFound as e:
            raise DatabaseError(e) from e

        except DBFException as e:
            raise DatabaseError(e) from e
    return wrapper
