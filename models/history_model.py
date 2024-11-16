from os import path
from dbfmapper.model import Model


class HISTORIAL(Model):
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/HISTORIALES.dbf"))

    def __init__(self):
        super().__init__(self)
        self.MATRICULA = None
        self.GRADO = None
        self.GRUPO = None
        self.ASIGNATURA = None
        self.PARCIAL_1 = None
        self.PARCIAL_2 = None
        self.PARCIAL_3 = None
        self.PROMF = None
