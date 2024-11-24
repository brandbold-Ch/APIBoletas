
from dbfmapper.model import Model
from os import path


class ALUMNO(Model):
    """
    Model representing student information in the academic system.

    This class maps to a DBF file that contains student records, including personal details
    such as names, CURP, academic grade, group, and enrollment status.

    Attributes:
        MATRICULA (str): The student's unique enrollment number.
        NOMBRES (str): The student's first names.
        APELLIDOS (str): The student's last names.
        CURP (str): The student's unique CURP (a Mexican personal identification number).
        GRADO (str): The student's current academic grade or year.
        GRUPO (str): The student's academic group.
        STATUSA (str): The student's status in the system (e.g., active, graduated, suspended).
    """
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/Alumnos.dbf"))

    def __init__(self) -> None:
        """
        Initializes the ALUMNO model and maps fields to the corresponding columns in the DBF file.

        This constructor sets up the student-related attributes that will be mapped to the DBF
        file's columns, which include personal and academic information.
        """
        super().__init__(self)
        self.MATRICULA = None
        self.NOMBRES = None
        self.APELLIDOS = None
        self.CURP = None
        self.GRADO = None
        self.GRUPO = None
        self.STATUSA = None
