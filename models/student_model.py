"""
This module defines the `ALUMNO` model, representing student information within the academic
system. It maps to a DBF file containing detailed student records, such as personal and academic
information, including names, CURP, grade, group, and enrollment status.

Key Features:
- Links student records with personal details, academic grade, group, and enrollment status.
- Maps student attributes to columns in the corresponding DBF file, facilitating easy data access.

Usage:
This model is used for managing and storing student data, mapped to a DBF file. It allows
easy integration into the academic system for tracking students' personal and academic information,
and can be linked to other models for more complex student-related processes,
such as tracking grades or academic performance.
"""

from os import path
from dbfmapper.model import Model


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
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/alumnos.dbf"))

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
