from models.student_model import ALUMNO
from dbfmapper.model import Model
from typing import Annotated
from os import path


class CARGA(Model):
    """
    Model representing the academic load (grades and absences) of students.

    This class maps to a DBF file that contains the academic load information for students,
    including grades for partial exams, absences, and other relevant data. It is linked to the
    `ALUMNO` model through the `MATRICULA` foreign key.

    Attributes:
        MATRICULA (str): The student's unique enrollment number. This field is a foreign key
                         referring to the `ALUMNO` model.
        CLAVE_IN (str): The unique identifier for the student's academic load (possibly for
                        a specific academic program or course).
        CLAVEMAT (str): The subject code for the assigned subject.
        PARCIAL_1 (str): The grade for the first partial exam.
        FALTAS_1 (int): The number of absences during the first partial exam.
        PARCIAL_2 (str): The grade for the second partial exam.
        FALTAS_2 (int): The number of absences during the second partial exam.
        PARCIAL_3 (str): The grade for the third partial exam.
        FALTAS_3 (int): The number of absences during the third partial exam.
        PROMEDIO (float): The average grade across all partial exams.
        OBSERVA (str): Any additional observations or comments about the student's academic performance.
        PALABRA (str): Possibly a keyword or code related to the student's academic or disciplinary record.
    """
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/cargas.dbf"))

    def __init__(self) -> None:
        """
        Initializes the CARGA model and maps fields to the corresponding columns in the DBF file.

        Sets up the attributes based on the structure of the academic load records, including
        fields for grades, absences, and other student-related information.
        """
        super().__init__(self)
        self.MATRICULA = Annotated[str, {"foreign_key": [ALUMNO]}]
        self.CLAVE_IN = None
        self.CLAVEMAT = None
        self.PARCIAL_1 = None
        self.FALTAS_1 = None
        self.PARCIAL_2 = None
        self.FALTAS_2 = None
        self.PARCIAL_3 = None
        self.FALTAS_3 = None
        self.PROMEDIO = None
        self.OBSERVA = None
        self.PALABRA = None
