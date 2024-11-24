from decorators.handlers import exception_handler
from models.student_model import ALUMNO


class StudentServices:
    """
    StudentServices handles the logic related to retrieving student data.
    This class includes methods for fetching student information, with built-in exception handling and caching.
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
            @caching: Caches the result of this method to improve performance by avoiding repeated database queries for the same student data.
        """
        return ALUMNO().get(MATRICULA=enrollment)
