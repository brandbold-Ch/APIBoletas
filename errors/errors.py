class ServerBaseException(Exception):

    def __init__(self, message) -> None:
        super().__init__(message)
        self.original_message = str(message)
        self.http_argument = None
        self.error_code = None
        self.status_code = None

    def to_dict(self) -> dict:
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
    def __init__(self, message="Entity not found 🤷") -> None:
        super().__init__(message)
        self.add_note("La entidad no existe. 🧑‍🎓")

        self.error_code = 1201
        self.status_code = 404
        self.http_argument = "Not Found 🚫"


class InvalidTimePeriod(ServerBaseException):
    def __init__(self, message="Invalid time period ⚠️") -> None:
        super().__init__(message)
        self.add_note("Periodo académico no completado. 🕓")

        self.error_code = 1202
        self.status_code = 400
        self.http_argument = "Bad Request ❓"


class PasswordsDoNotMatch(ServerBaseException):
    def __init__(self, message="Passwords do not match 🔒") -> None:
        super().__init__(message)
        self.add_note("La contraeña es incorrecta. ⛔")

        self.error_code = 1203
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class DatabaseError(ServerBaseException):
    def __init__(self, message="Error reading or writing to database 💿") -> None:
        super().__init__(message)
        self.add_note("Error al leer o escribir en la base de datos")

        self.error_code = 1204
        self.status_code = 500
        self.http_argument = "Internal Server Error ❌"


class InvalidParam(ServerBaseException):
    def __init__(self, message="The parameter type must be student or score ⚠️") -> None:
        super().__init__(message)
        self.add_note("El tipo de parametro debe ser 'student' o 'score'")

        self.error_code = 1205
        self.status_code = 400
        self.http_argument = "Bad Request ❓"


class NotFoundTokenError(ServerBaseException):
    def __init__(self, message="Token not found 🤷‍♂️") -> None:
        super().__init__(message)
        self.add_note("No se encuentra el token en el header.")
        self.error_code = 1206
        self.status_code = 403
        self.http_argument = "Forbidden ⚔️"


class ExpiredTokenError(ServerBaseException):
    def __init__(self, message="Token has expired 💨") -> None:
        super().__init__(message)
        self.add_note("El token ha expirado.")
        self.error_code = 1207
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class InvalidTokenError(ServerBaseException):
    def __init__(self, message="The token is invalid 🔏") -> None:
        super().__init__(message)
        self.add_note("El token es inválido.")
        self.error_code = 1208
        self.status_code = 400
        self.http_argument = "Bad Request ❓"


class IncorrectUserError(ServerBaseException):
    def __init__(self, message="The token does not correspond to the student 🤡") -> None:
        super().__init__(message)
        self.add_note("El token que mandas no corresponde con el alumno.")
        self.error_code = 1209
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class TokenNotAllowed(ServerBaseException):
    def __init__(self, message="Token not allowed 🔑") -> None:
        super().__init__(message)
        self.add_note("No puedes subir bases de datos.")
        self.error_code = 1210
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"