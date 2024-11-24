from dbfmapper.exception.exceptions import (
    NotFoundTable, DatabaseNotFound, DBFException
)
from errors.errors import NotFoundEntity, DatabaseError
from typing import Callable


def exception_handler(func: Callable) -> Callable:
    """
    A decorator to handle exceptions from the `dbfmapper` library and map them to application-specific errors.

    This decorator intercepts exceptions that may occur during the execution of the wrapped function
    and raises corresponding custom application-level exceptions.

    Args:
        func (Callable): The function to be wrapped by the decorator.

    Returns:
        Callable: The wrapped function with exception handling logic.

    Raises:
        NotFoundEntity: Raised when a `NotFoundTable` exception occurs.
        DatabaseError: Raised when a `DatabaseNotFound` or `DBFException` occurs.
    """
    def wrapper(*args, **kwargs) -> Callable:
        """
        Inner function to execute the wrapped function and handle specific exceptions.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns:
            Callable: The result of the decorated function if no exceptions occur.

        Raises:
            NotFoundEntity: Mapped from `NotFoundTable`.
            DatabaseError: Mapped from `DatabaseNotFound` or `DBFException`.
        """
        try:
            return func(*args, **kwargs)

        except NotFoundTable as e:
            raise NotFoundEntity(e) from e

        except DatabaseNotFound as e:
            raise DatabaseError(e) from e

        except DBFException as e:
            raise DatabaseError(e) from e
    return wrapper
