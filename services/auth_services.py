"""
This module defines the `AuthServices` class, responsible for handling user authentication
logic, including logging in a student and generating JWT tokens.

Key Features:
- Logs in a student using their CURP (username) and enrollment number (password).
- Verifies the password against the student's enrollment number.
- Generates a JWT token for authenticated users.
- Returns the student data along with the token upon successful login.

Exceptions:
- Raises `PasswordsDoNotMatch` if the provided password does not match the student's
  enrollment number.

Usage:
This service is typically used to authenticate students by verifying their CURP and password
and returning a JWT token that can be used for further API requests.
"""
from utils.db import Collection, get_collection
from decorators.handlers import exception_handler
from errors.errors import PasswordsDoNotMatch, NotFoundStudent
from utils.token_tools import create_token


class AuthServices:
    """
    AuthServices handles user authentication logic, including login and token creation.
    """

    def __init__(self) -> None:
        self.student = get_collection(Collection.STUDENTS)

    @exception_handler
    async def login(self, username: str, password: str) -> dict:
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
            PasswordsDoNotMatch: If the provided password does not match the
            student's enrollment number.

        Steps:
            1. Retrieve the student using the CURP (username).
            2. Verify if the provided password matches the student's enrollment number.
            3. If they match, create a JWT token.
            4. Return the token and the student data.
        """
        student = await self.student.find_one({"CURP": username},
                                              {"_id": 0})

        if student is None:
            raise NotFoundStudent()

        if student["MATRICULA"] != password:
            raise PasswordsDoNotMatch()

        return {
            "token": create_token({
                "enrollment": password
            }),
            "student_data": student
        }
