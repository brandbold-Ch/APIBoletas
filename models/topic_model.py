"""
This module defines the `ASIGNATURA` model, representing academic subjects within the system.
It maps to a DBF file containing information about various subjects, including their names,
unique identifiers, and additional keys that may be used for categorization or linking to
other data in the academic system.

Key Features:
- Represents academic subjects in the system, allowing easy mapping to a DBF file.
- Stores essential subject information such as name, unique keys, and identifiers.

Usage:
This model is used for managing and storing academic subject information in the system.
It facilitates integration with other models related to student performance, grades, and curriculum
management, allowing efficient handling of subjects within the academic environment.
"""


from os import path
from dbfmapper.model import Model


class ASIGNATURA(Model):
    """
    Model representing an academic subject (Asignatura) in the system.

    This class maps to a DBF file that contains information about various academic subjects,
    including their names, keys, and related identifiers.

    Attributes:
        ASIGNATURA (str): The name of the academic subject.
        CLAVE (str): A unique key for the subject.
        CLAVE_IN (str): An additional identifier for the subject, possibly
        used for categorization or linking to other data.
    """
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/ASIGNATURAS.DBF"))

    def __init__(self) -> None:
        """
        Initializes the ASIGNATURA model and maps fields to the
        corresponding columns in the DBF file.

        This constructor sets up the subject-related attributes
        that will be mapped to the DBF
        file's columns, which include the subject's name, key,
        and other identifiers.
        """
        super().__init__(self)
        self.ASIGNATURA = None
        self.CLAVE = None
        self.CLAVE_IN = None
