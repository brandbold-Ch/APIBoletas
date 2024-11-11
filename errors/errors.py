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
    def __init__(self, message="Invalid time period ⚠️"):
        super().__init__(message)
        self.add_note("Periodo académico no completado. 🕓")

        self.error_code = 1202
        self.status_code = 400
        self.http_argument = "Bad Request 🚫"


class PasswordsDoNotMatch(ServerBaseException):
    def __init__(self, message="Passwords do not match 🔒"):
        super().__init__(message)
        self.add_note("La contraeña es incorrecta. ⛔")

        self.error_code = 1203
        self.status_code = 401
        self.http_argument = "Unauthorized 🚫"


class DatabaseError(ServerBaseException):
    def __init__(self, message="Error reading or writing to database 💿"):
        super().__init__(message)
        self.add_note("Error al leer o escribir en la base de datos")

        self.error_code = 1204
        self.status_code = 500
        self.http_argument = "Internal Server Error ❌"


class InvalidParam(ServerBaseException):
    def __init__(self, message="The parameter type must be student or score ⚠️"):
        super().__init__(message)
        self.add_note("El tipo de parametro debe ser 'student' o 'score'")

        self.error_code = 1205
        self.status_code = 400
        self.http_argument = "Bad Request 🚫"
