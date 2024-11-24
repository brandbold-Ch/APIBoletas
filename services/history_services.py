from decorators.handlers import exception_handler
from models.history_model import HISTORIAL
from models.student_model import ALUMNO
from utils.rating_tools import Ratings


class HistoryServices:
    """
    HistoryServices handles the logic related to academic histories of students, such as
    retrieving, updating, and deleting academic records.
    """

    @exception_handler
    def get_histories(self, enrollment: str, rank: str, partial: int) -> ALUMNO:
        """
        Fetches a student's academic history based on their enrollment, grade rank, and partial.

        Args:
            enrollment (str): The enrollment number (MATRICULA) of the student.
            rank (str): The grade rank of the student (e.g., '1' for first grade, '2' for second grade).
            partial (int): The partial number (1, 2, or 3) to calculate the rating for the student.

        Returns:
            ALUMNO: The student object populated with their academic history.

        Steps:
            1. Retrieve the student data using the provided enrollment number.
            2. Fetch the academic history for the student based on the enrollment number and grade.
            3. Apply ratings to the student's history using the `Ratings` utility.
            4. Return the updated student object with the academic history and calculated ratings.
        """
        student = ALUMNO().get(MATRICULA=enrollment)
        student.HISTORIAL = HISTORIAL().get_all(MATRICULA=enrollment, GRADO=rank, easy_view=True)
        Ratings(student.HISTORIAL, partial) + student

        return student

    def set_history(self, student: ALUMNO) -> None:
        histories = HISTORIAL().get_all(MATRICULA=student.MATRICULA)

    def delete_history(self) -> None:
        ...

    def update_history(self) -> None:
        ...
    