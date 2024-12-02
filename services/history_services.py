"""
This module defines the `HistoryServices` class, responsible for handling the logic related to
academic histories of students. It allows retrieving, updating, and deleting academic records,
and calculating ratings based on the student's academic history.

Key Features:
- Retrieves a student's academic history based on enrollment, grade rank, and partial exam number.
- Uses the `Ratings` utility to calculate academic ratings for students.
- Returns the student object populated with academic history and calculated ratings.

Exceptions:
- The `exception_handler` decorator handles any exceptions raised during the execution of methods.

Usage:
This service is typically used to fetch and calculate ratings for a student's academic history,
which can then be used for analysis or reporting purposes.
"""

from decorators.handlers import exception_handler
from models.history_model import HISTORIAL
from models.student_model import ALUMNO
from decorators.ratings import get_ratings


class HistoryServices:
    """
    HistoryServices handles the logic related to academic histories of students, such as
    retrieving, updating, and deleting academic records.
    """

    @exception_handler
    @get_ratings
    def get_histories(self, enrollment: str, partial: int, rank: str) -> ALUMNO:
        """
        Fetches a student's academic history based on their enrollment, grade rank, and partial.

        Args:
            enrollment (str): The enrollment number (MATRICULA) of the student.
            rank (str): The grade rank of the student (e.g., '1' for first grade,
            '2' for second grade).
            partial (int): The partial number (1, 2, or 3) to calculate the rating
            for the student.

        Returns:
            ALUMNO: The student object populated with their academic history.

        Steps:
            1. Retrieve the student data using the provided enrollment number.
            2. Fetch the academic history for the student based on the enrollment number and grade.
            3. Apply ratings to the student's history using the `Ratings` utility.
            4. Return the updated student object with the academic history and calculated ratings.
        """
        student = ALUMNO().get(MATRICULA=enrollment)
        setattr(
            student, "HISTORIAL",
            HISTORIAL().get_all(MATRICULA=enrollment, GRADO=rank, easy_view=True)
        )

        return student
    