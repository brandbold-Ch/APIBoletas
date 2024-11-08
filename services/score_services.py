from wsgiref.simple_server import sys_version

from errors.errors import InvalidTimePeriod
from decorators.handlers import exception_handler
from decorators.cache import caching
from models.score_model import BOLETA
from util.cache import cache, cached
from models.student_model import ALUMNO


class Ratings:

    def __init__(self, reports: list[dict], partial: int) -> None:
        self.reports = reports
        self.partial = partial

    def partials(self) -> dict:
        rating, faults = 0.0, 0
        partial = f"PARCIAL_{self.partial}"

        if self.partial == 0:
            return {}

        for item in self.reports:
            if item[partial] != 'None':
                rating += float(item[partial])
                faults += int(item[f"FALTAS_{self.partial}"])
            else:
                raise InvalidTimePeriod()

        return {
            "TOTAL_FALTAS": faults,
            "PROMEDIO_FINAL": rating / len(self.reports)
        }

    def __add__(self, other):
        details = self.partials()

        if details == {}:
            return None
        setattr(other, "DETALLES", details)
        return other


class ScoreServices:

    def __init__(self) -> None:
        pass

    @exception_handler
    @cached(cache, key=lambda self, enrollment, partial: enrollment)
    def get_score(self, enrollment: str, partial: int) -> ALUMNO:
        score = ALUMNO().get(MATRICULA=enrollment, relates=True)
        score.BOLETA = score.BOLETA[0:-1]
        ratings = Ratings(score.BOLETA, partial)
        union = ratings + score

        if union is None:
            return score
        return union
