"""
This module provides an exception-handling decorator for mapping database-related exceptions
from the `dbfmapper` library to custom application-level exceptions.

Purpose:
- Intercept and handle exceptions raised by functions interacting with `dbfmapper`.
- Map these exceptions to more meaningful application-specific errors for consistent error handling.

Components:
- The `exception_handler` decorator: Wraps a function to add exception-handling logic.
- Exception mapping:
    - `NotFoundTable` is mapped to `NotFoundEntity`.
    - `DatabaseNotFound` and `DBFException` are mapped to `DatabaseError`.

Usage:
Apply the `exception_handler` decorator to any function that interacts with the `dbfmapper` library
to ensure exceptions are translated to custom application-specific exceptions.
"""
from typing import Callable
from dbfmapper.exception.exceptions import (
    NotFoundTable, DatabaseNotFound, DBFException
)
from errors.errors import NotFoundStudent, ServerError
from utils.logging_config import app_logger


def exception_handler(func: Callable) -> Callable:
    """
    A decorator to handle exceptions from the `dbfmapper`
    library and map them to application-specific errors.

    This decorator intercepts exceptions that may occur
    during the execution of the wrapped function
    and raises corresponding custom application-level exceptions.

    Args:
        func (Callable): The function to be wrapped by the decorator.

    Returns:
        Callable: The wrapped function with exception handling logic.

    Raises:
        NotFoundEntity: Raised when a `NotFoundTable` exception occurs.
        DatabaseError: Raised when a `DatabaseNotFound` or `DBFException` occurs.
    """
    async def wrapper(*args, **kwargs) -> Callable:
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
            return await func(*args, **kwargs)

        except NotFoundTable as e:
            app_logger.error(f"Error on <exception_handler, NotFoundTable>: {str(e)}")
            raise NotFoundStudent() from e

        except DatabaseNotFound as e:
            app_logger.critical(f"Error on <exception_handler, DatabaseNotFound>: {str(e)}")
            raise ServerError(e) from e

        except DBFException as e:
            app_logger.critical(f"Error on <exception_handler, DatabaseNotFound>: {str(e)}")
            raise ServerError(e) from e

    return wrapper
