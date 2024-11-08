from models.student_model import ALUMNO
from dbfmapper.model import Model
from typing import Annotated
from os import path


class BOLETA(Model):
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/boletas.dbf"))

    def __init__(self):
        super().__init__(self)

        self.CLAVEMAT = None
        self.MATRICULA = Annotated[str, {"foreign_key": [ALUMNO]}]
        self.MATERIA = None
        self.PARCIAL_1 = None
        self.FALTAS_1 = None
        self.PARCIAL_2 = None
        self.FALTAS_2 = None
        self.PARCIAL_3 = None
        self.FALTAS_3 = None
        self.PARCIAL_4 = None
        self.FALTAS_4 = None
        self.PARCIAL_5 = None
        self.PROMEDIO = None
        self.STATUS = None
        self.OBSERVA = None
        self.PALABRA = None