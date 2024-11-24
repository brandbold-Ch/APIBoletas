from models.load_model import CARGA
from models.topic_model import ASIGNATURA
from models.student_model import ALUMNO
from decorators.handlers import exception_handler
from utils.rating_tools import Ratings


class LoadServices:
    """
    LoadServices handles the logic related to a student's academic load, such as retrieving their
    courses (subjects) and assigning ratings to those subjects.
    """

    def _merge_topics(self, obj: ALUMNO) -> None:
        """
        Merges the course (subject) data into the student's academic load.

        Args:
            obj (ALUMNO): The student object whose courses (CARGA) will be enriched with subject details.

        Returns:
            None: This method modifies the student's CARGA attribute in place by merging subject data.

        Steps:
            1. Iterates over each course in the student's CARGA (academic load).
            2. For each course, it fetches additional data about the subject (ASIGNATURA) using the
               course's CLAVE_IN and adds this information to the respective course in CARGA.
        """
        for load in obj.CARGA:
            load["DATOS_MATERIA"] = ASIGNATURA().get_all(
                CLAVE_IN=load["CLAVE_IN"], easy_view=True
            )[-1]

    @exception_handler
    def get_academic_loads(self, enrollment: str, partial: int) -> ALUMNO:
        """
        Retrieves the academic load for a given student, applies ratings to their courses,
        and enriches the courses with subject information.

        Args:
            enrollment (str): The student's enrollment number (MATRICULA).
            partial (int): The partial number (1, 2, or 3) to calculate ratings for.

        Returns:
            ALUMNO: The student object enriched with academic load (CARGA) and ratings.

        Steps:
            1. Retrieves the student data based on their enrollment number.
            2. Fetches the student's academic load (CARGA) and applies ratings to each course.
            3. Merges the subject data (ASIGNATURA) into the student's academic load.
            4. Returns the student object with the updated academic load.
        """
        student = ALUMNO().get(MATRICULA=enrollment, relates=True, exclude=["HISTORIAL"])
        Ratings(student.CARGA, partial) + student
        self._merge_topics(student)

        return student
