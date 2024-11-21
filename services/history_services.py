from models.history_model import HISTORIAL
from models.student_model import ALUMNO
from decorators.handlers import exception_handler
from utils.tools import Ratings


class HistoryServices:

    @exception_handler
    def get_histories(self, enrollment: str, rank: str, partial: int) -> ALUMNO:
        student = ALUMNO().get(MATRICULA=enrollment)
        student.HISTORIAL = HISTORIAL().get_all(MATRICULA=enrollment, GRADO=rank, easy_view=True)
        Ratings(student.HISTORIAL, partial) + student

        return student

    def set_history(self, student: ALUMNO):
        histories = HISTORIAL().get_all(MATRICULA=student.MATRICULA)

    def delete_history(self):
        ...

    def update_history(self):
        ...
    