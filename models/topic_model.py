from dbfmapper.model import Model
from os import path


class ASIGNATURA(Model):
    __ctx__ = path.abspath(path.join(path.dirname(__file__), "../db/ASIGNATURAS.DBF"))

    def __init__(self):
        super().__init__(self)
        self.ASIGNATURA = None
        self.CLAVE = None
        self.CLAVE_IN = None
