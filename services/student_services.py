"""
This module defines the `StudentServices` class, which is responsible for handling the logic
related to retrieving and managing student data. It includes methods for fetching student information,
with built-in exception handling to ensure robust error management.

Key Features:
- Retrieves student data based on the enrollment number (MATRICULA).
- Built-in exception handling with the `@exception_handler` decorator.
- Supports caching to improve performance by avoiding repeated database queries for the same student.

Methods:
- `get_student`: Fetches the student data from the database using their enrollment number (MATRICULA).

Exceptions:
- The `@exception_handler` decorator ensures that errors raised during the execution of this method
  are caught, logged, and properly managed.

Usage:
This service is typically used to retrieve student data from the database based on their enrollment number.
The retrieved student object contains the necessary details such as name, enrollment, and other student-related
attributes.
"""

from decorators.handlers import exception_handler
from models.student_model import ALUMNO


class StudentServices:
    """
    StudentServices handles the logic related to retrieving student data.
    This class includes methods for fetching student information, with built-in
    exception handling and caching.
    """

    @exception_handler
    def get_student(self, enrollment: str) -> ALUMNO:
        """
        Fetches a student's data based on their enrollment number (MATRICULA).

        Args:
            enrollment (str): The student's enrollment number (MATRICULA).

        Returns:
            ALUMNO: The student object containing the student's data.

        Decorators:
            @exception_handler: Ensures any errors are properly handled and logged.
            @caching: Caches the result of this method to improve performance by
            avoiding repeated database queries for the same student data.
        """
        return ALUMNO().get(MATRICULA=enrollment)
