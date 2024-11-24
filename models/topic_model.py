from dbfmapper.model import Model
from os import path


class ASIGNATURA(Model):
    """
    Model representing an academic subject (Asignatura) in the system.

    This class maps to a DBF file that contains information about various academic subjects,
    including their names, keys, and related identifiers.

    Attributes:
        ASIGNATURA (str): The name of the academic subject.
        CLAVE (str): A unique key for the subject.
        CLAVE_IN (str): An additional identifier for the subject, possibly used for categorization or linking to other data.
    """
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/ASIGNATURAS.DBF"))

    def __init__(self) -> None:
        """
        Initializes the ASIGNATURA model and maps fields to the corresponding columns in the DBF file.

        This constructor sets up the subject-related attributes that will be mapped to the DBF
        file's columns, which include the subject's name, key, and other identifiers.
        """
        super().__init__(self)
        self.ASIGNATURA = None
        self.CLAVE = None
        self.CLAVE_IN = None
