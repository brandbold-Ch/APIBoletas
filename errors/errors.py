class ServerBaseException(Exception):
    """
    Base class for server-specific exceptions.

    Attributes:
        original_message (str): The original error message provided during initialization.
        http_argument (str): The HTTP status string associated with the error (e.g., "Not Found").
        error_code (int): Custom error code for the exception.
        status_code (int): HTTP status code (e.g., 404, 500).
    """
    def __init__(self, message) -> None:
        """
        Initialize the base exception with a custom message.

        Args:
            message (str): The error message for this exception.
        """
        super().__init__(message)
        self.original_message = str(message)
        self.http_argument = None
        self.error_code = None
        self.status_code = None

    def to_dict(self) -> dict:
        """
        Convert the exception details into a dictionary format.

        This method is particularly useful for returning structured
        error responses in APIs.

        Returns:
            dict: A dictionary containing exception details including status,
                  original message, additional notes, and error codes.
        """
        return {
            "status": self.http_argument,
            "message": self.original_message,
            "details": self.__dict__["__notes__"][0].strip(),
            "codes": {
                "status_code": self.status_code,
                "error_code": self.error_code
            }
        }


class NotFoundEntity(ServerBaseException):
    """
    Exception raised when an entity is not found.

    Attributes:
        message (str): The error message (default is "Entity not found 🤷").
        error_code (int): Custom error code for entity not found (default is 1201).
        status_code (int): HTTP status code for not found errors (default is 404).
        http_argument (str): HTTP status string ("Not Found 🚫").
    """
    def __init__(self, message="Entity not found 🤷") -> None:
        super().__init__(message)
        self.add_note("La entidad no existe.")

        self.error_code = 1201
        self.status_code = 404
        self.http_argument = "Not Found 🚫"


class InvalidTimePeriod(ServerBaseException):
    """
    Exception raised for invalid time periods.

    Attributes:
        message (str): The error message (default is "Invalid time period 🕓️").
        error_code (int): Custom error code for invalid time periods (default is 1202).
        status_code (int): HTTP status code for bad request (default is 400).
        http_argument (str): HTTP status string ("Bad Request ❓").
    """
    def __init__(self, message="Invalid time period 🕓️") -> None:
        super().__init__(message)
        self.add_note("Periodo académico no completado.")

        self.error_code = 1202
        self.status_code = 400
        self.http_argument = "Bad Request ❓"


class PasswordsDoNotMatch(ServerBaseException):
    """
    Exception raised when passwords do not match.

    Attributes:
        message (str): The error message (default is "Passwords do not match 🔒").
        error_code (int): Custom error code for password mismatch (default is 1203).
        status_code (int): HTTP status code for unauthorized (default is 401).
        http_argument (str): HTTP status string ("Unauthorized 🚫").
    """
    def __init__(self, message="Passwords do not match 🔒") -> None:
        super().__init__(message)
        self.add_note("La contraeña es incorrecta.")

        self.error_code = 1203
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class DatabaseError(ServerBaseException):
    """
    Exception raised for database read/write errors.

    Attributes:
        message (str): The error message (default is "Error reading or writing to database 💿🔄").
        error_code (int): Custom error code for database errors (default is 1204).
        status_code (int): HTTP status code for internal server errors (default is 500).
        http_argument (str): HTTP status string ("Internal Server Error ❌").
    """
    def __init__(self, message="Error reading or writing to database 💿🔄") -> None:
        super().__init__(message)
        self.add_note("Error al leer o escribir en la base de datos.")

        self.error_code = 1204
        self.status_code = 500
        self.http_argument = "Internal Server Error ❌"


class NotFoundTokenError(ServerBaseException):
    """
    Exception raised when a token is not found in the request.

    Attributes:
        message (str): The error message (default is "Token not found 🤷‍♂️").
        error_code (int): Custom error code for missing token (default is 1206).
        status_code (int): HTTP status code for forbidden errors (default is 403).
        http_argument (str): HTTP status string ("Forbidden ⚔️").
    """
    def __init__(self, message="Token not found 🤷‍♂️") -> None:
        super().__init__(message)
        self.add_note("No se encuentra el token en el header.")
        self.error_code = 1206
        self.status_code = 403
        self.http_argument = "Forbidden ⚔️"


class ExpiredTokenError(ServerBaseException):
    """
    Exception raised when a token has expired.

    Attributes:
        message (str): The error message (default is "Token has expired 💨").
        error_code (int): Custom error code for expired token (default is 1207).
        status_code (int): HTTP status code for unauthorized (default is 401).
        http_argument (str): HTTP status string ("Unauthorized 🚫").
    """
    def __init__(self, message="Token has expired 💨") -> None:
        super().__init__(message)
        self.add_note("El token ha expirado.")

        self.error_code = 1207
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class InvalidTokenError(ServerBaseException):
    """
    Exception raised when a token is invalid.

    Attributes:
        message (str): The error message (default is "The token is invalid 🔏").
        error_code (int): Custom error code for invalid token (default is 1208).
        status_code (int): HTTP status code for bad request (default is 400).
        http_argument (str): HTTP status string ("Bad Request ❓").
    """
    def __init__(self, message="The token is invalid 🔏") -> None:
        super().__init__(message)
        self.add_note("El token es inválido.")
        self.error_code = 1208
        self.status_code = 400
        self.http_argument = "Bad Request ❓"


class IncorrectUserError(ServerBaseException):
    """
    Exception raised when the token does not correspond to the user.

    Attributes:
        message (str): The error message (default is "The token does not correspond to the student, you are ridiculous. 🙂‍↕️").
        error_code (int): Custom error code for incorrect user token (default is 1209).
        status_code (int): HTTP status code for unauthorized (default is 401).
        http_argument (str): HTTP status string ("Unauthorized 🚫").
    """
    def __init__(self, message="The token does not correspond to the student, you are ridiculous. 🙂‍↕️") -> None:
        super().__init__(message)
        self.add_note("El token que mandas no corresponde con el alumno.")
        self.error_code = 1209
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class TokenNotAllowed(ServerBaseException):
    """
    Exception raised when an action is not allowed with the provided token.

    Attributes:
        message (str): The error message (default is "Token not allowed 🔑").
        error_code (int): Custom error code for token restrictions (default is 1210).
        status_code (int): HTTP status code for unauthorized (default is 401).
        http_argument (str): HTTP status string ("Unauthorized 🚫").
    """
    def __init__(self, message="Token not allowed 🔑") -> None:
        super().__init__(message)
        self.add_note("No puedes subir bases de datos.")
        self.error_code = 1210
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"
