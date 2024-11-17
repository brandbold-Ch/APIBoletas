from models.history_model import HISTORIAL
from models.student_model import ALUMNO
from decorators.handlers import exception_handler


class HistoryServices:

    @exception_handler
    def get_history(self, enrollment: str, rank: str) -> HISTORIAL:
        return HISTORIAL().get(MATRICULA=enrollment, GRADO=rank)

    def set_history(self, student: ALUMNO):
        histories = HISTORIAL().get_all(MATRICULA=student.MATRICULA)

    def delete_history(self):
        ...

    def update_history(self):
        ...
