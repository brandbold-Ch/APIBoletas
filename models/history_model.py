from os import path
from dbfmapper.model import Model
from models.student_model import ALUMNO
from typing import Annotated


class HISTORIAL(Model):
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/HISTORIALES.dbf"))

    def __init__(self):
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
