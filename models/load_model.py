from models.student_model import ALUMNO
from dbfmapper.model import Model
from typing import Annotated
from os import path


class CARGA(Model):
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/cargas.dbf"))

    def __init__(self):
        super().__init__(self)

        self.CLAVE_IN = None
        self.CLAVEMAT = None
        self.MATRICULA = Annotated[str, {"foreign_key": [ALUMNO]}]
        self.PARCIAL_1 = None
        self.FALTAS_1 = None
        self.OBSERVA = None
        self.PALABRA = None
        self.STATUS = None
        self.PARCIAL_2 = None
        self.FALTAS_2 = None
        self.PARCIAL_3 = None
        self.FALTAS_3 = None
        self.PARCIAL_4 = None
        self.FALTAS_4 = None
        self.PARCIAL_5 = None
        self.PROMEDIO = None
