from decorators.handlers import exception_handler
from errors.errors import PasswordsDoNotMatch
from models.student_model import ALUMNO
from utils.token import create_token


class AuthServices:
    """
    AuthServices handles user authentication logic, including login and token creation.
    """

    @exception_handler
    def login(self, username: str, password: str) -> dict:
        """
        Log in a student using their CURP (username) and password (enrollment number).

        Args:
            username (str): The CURP of the student, used as the login identifier.
            password (str): The password (enrollment number) provided by the user.

        Returns:
            dict: A dictionary containing:
                - 'token': The JWT token to authenticate the user.
                - 'student_data': The student information from the database.

        Raises:
            PasswordsDoNotMatch: If the provided password does not match the student's enrollment number.

        Steps:
            1. Retrieve the student using the CURP (username).
            2. Verify if the provided password matches the student's enrollment number.
            3. If they match, create a JWT token.
            4. Return the token and the student data.
        """
        student = ALUMNO().get(CURP=username)

        if student.MATRICULA != password:
            raise PasswordsDoNotMatch()

        return {
            "token": create_token({
                "enrollment": password
            }),
            "student_data": student.to_repr()
        }
