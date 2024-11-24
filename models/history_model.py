from os import path
from dbfmapper.model import Model
from models.student_model import ALUMNO
from typing import Annotated


class HISTORIAL(Model):
    """
    Model representing the historical academic records of students.

    This class maps to a DBF file that contains the academic history for students, including
    grades for different subjects and partial exams. It is linked to the `ALUMNO` model through
    the `MATRICULA` foreign key.

    Attributes:
        MATRICULA (str): The student's unique enrollment number. This field is a foreign key
                         referring to the `ALUMNO` model.
        GRADO (str): The grade level of the student (e.g., first year, second year).
        GRUPO (str): The group or class to which the student belongs.
        CLAVEMAT (str): The subject code for the assigned subject.
        ASIGNATURA (str): The name of the subject.
        PARCIAL_1 (str): The grade for the first partial exam.
        PARCIAL_2 (str): The grade for the second partial exam.
        PARCIAL_3 (str): The grade for the third partial exam.
        PROMEDIO (float): The average grade for the student across the partial exams.
        OBSERVA (str): Any additional observations or comments about the student's performance.
    """
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/HISTORIALES.dbf"))

    def __init__(self) -> None:
        """
        Initializes the HISTORIAL model and maps fields to the corresponding columns in the DBF file.

        Sets up the attributes based on the structure of the historical academic records, including
        fields for the student's enrollment number, grades, and subject information.
        """
        super().__init__(self)
        self.MATRICULA = Annotated[str, {"foreign_key": [ALUMNO]}]
        self.GRADO = None
        self.GRUPO = None
        self.CLAVEMAT = None
        self.ASIGNATURA = None
        self.PARCIAL_1 = None
        self.PARCIAL_2 = None
        self.PARCIAL_3 = None
        self.PROMEDIO = None
        self.OBSERVA = None
