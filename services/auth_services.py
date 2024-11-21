from decorators.handlers import exception_handler
from errors.errors import PasswordsDoNotMatch
from models.student_model import ALUMNO
from utils.token import create_token


class AuthServices:

    @exception_handler
    #@cached(cache, key=lambda self, username, password: username)
    def login(self, username: str, password: str) -> dict:
        student = ALUMNO().get(CURP=username)

        if student.MATRICULA != password:
            raise PasswordsDoNotMatch()

        return {
            "token": create_token({
                "enrollment": password
            }),
            "student_data": student.to_repr()
        }
