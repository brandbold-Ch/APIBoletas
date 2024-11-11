from dbfmapper.model import Model
from os import path


class ALUMNO(Model):
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/Alumnos.dbf"))

    def __init__(self):
        super().__init__(self)
        self.MATRICULA = None
        self.NOMBRES = None
        self.STATUSA = None
        self.APELLIDOS = None
        self.GRADO = None
        self.GRUPO = None
        self.CURP = None
