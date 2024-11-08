from decorators.handlers import exception_handler
from decorators.cache import caching
from models.student_model import ALUMNO


class StudentServices:

    def __init__(self) -> None:
        pass

    @exception_handler
    @caching
    def get_student(self, enrollment: str, **kwargs) -> ALUMNO:
        return kwargs.get("data", ALUMNO().get(MATRICULA=enrollment))
