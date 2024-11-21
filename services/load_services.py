from models.load_model import CARGA
from models.topic_model import ASIGNATURA
from models.student_model import ALUMNO
from decorators.handlers import exception_handler
from utils.tools import Ratings


class LoadServices:

    def _merge_topics(self, obj: ALUMNO) -> None:
        for load in obj.CARGA:
            load["DATOS_MATERIA"] = ASIGNATURA().get_all(
                CLAVE_IN=load["CLAVE_IN"], easy_view=True
            )[-1]

    @exception_handler
    def get_academic_loads(self, enrollment: str, partial: int) -> ALUMNO:
        student = ALUMNO().get(MATRICULA=enrollment, relates=True, exclude=["HISTORIAL"])
        Ratings(student.CARGA, partial) + student
        self._merge_topics(student)

        return student
