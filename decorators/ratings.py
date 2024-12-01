"""
This module provides functionality to handle student data and apply academic ratings.

It includes:
- A decorator (`get_ratings`) that processes student objects to apply ratings to their academic load.

Key Features:
- Validates the presence of essential attributes ('CARGA' or 'HISTORIAL') in student objects.
- Applies ratings based on the provided partial.
- Custom error handling to manage unexpected issues during processing.

Dependencies:
- ALUMNO model for student data management.
- Ratings utility for academic load evaluation.
"""

from typing import Callable
from utils.rating_tools import Ratings
from models.student_model import ALUMNO


def get_ratings(func: Callable) -> Callable:
    """
    Decorator that applies ratings to a student object returned by the decorated function.

    The decorator validates the presence of either the 'CARGA' or 'HISTORIAL' attribute in
    the returned student object and applies the corresponding ratings using the `Ratings` class.

    Args:
        func (Callable): A function that returns an ALUMNO object.

    Returns:
        Callable: The decorated function, which returns an updated ALUMNO object with ratings applied.
    """
    def wrapper(self, enrollment: str, partial: int, *args, **kwargs) -> ALUMNO:
        """
        Wrapper function that intercepts the call to the decorated function and
        applies ratings to the returned ALUMNO object.

        Args:
            self: Reference to the class instance calling the function.
            enrollment (str): The student's enrollment number.
            partial (int): The partial number to calculate ratings for.
            *args: Additional positional arguments passed to the original function.
            **kwargs: Additional keyword arguments passed to the original function.

        Returns:
            ALUMNO: The updated ALUMNO object with ratings applied.

        """
        student: ALUMNO = func(self, enrollment, partial, *args, **kwargs)
        attr: list[dict] = (getattr(student, "CARGA", None) or
                            getattr(student, "HISTORIAL", None))

        return Ratings(attr, partial) + student
    return wrapper
