from decorators.handlers import exception_handler
from errors.errors import PasswordsDoNotMatch
from models.student_model import ALUMNO
from util.cache import cache, cached


class AuthServices:

    def __init__(self) -> None:
        pass

    @exception_handler
    @cached(cache, key=lambda self, username, password: username)
    def login(self, username: str, password: str) -> ALUMNO:
        student = ALUMNO().get(MATRICULA=username)

        if student.CURP != password:
            raise PasswordsDoNotMatch()
        return student
