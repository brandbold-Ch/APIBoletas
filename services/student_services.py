from decorators.handlers import exception_handler
from decorators.cache import caching
from models.student_model import ALUMNO


class StudentServices:

    @exception_handler
    @caching
    def get_student(self, enrollment: str) -> ALUMNO:
        return ALUMNO().get(MATRICULA=enrollment)
