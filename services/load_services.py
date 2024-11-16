from models.load_model import CARGA
from models.topic_model import ASIGNATURA
from models.student_model import ALUMNO
from errors.errors import InvalidTimePeriod
from decorators.handlers import exception_handler
from services.history_services import HistoryServices


class Ratings:

    def __init__(self, reports: list[dict], partial: int) -> None:
        self.reports = reports
        self.partial = partial

    def calculate_partials(self) -> dict:
        try:
            rating, faults = 0.0, 0
            partial = f"PARCIAL_{self.partial}"
            score_to_word = {
                '0.0': ("CERO", "REPROBADO"),
                '1.0': ("UNO", "REPROBADO"),
                '2.0': ("DOS", "REPROBADO"),
                '3.0': ("TRES", "REPROBADO"),
                '4.0': ("CUATRO", "REPROBADO"),
                '5.0': ("CINCO", "REPROBADO"),
                '6.0': ("SEIS", "APROBADO"),
                '7.0': ("SIETE", "APROBADO"),
                '8.0': ("OCHO", "APROBADO"),
                '9.0': ("NUEVE", "APROBADO"),
                '10.0': ("DIEZ", "APROBADO"),
            }

            if self.partial == 0:
                return {}

            for item in self.reports:
                if item[partial] != 'None':
                    if item[partial] in score_to_word:
                        item["PALABRA"], item["OBSERVA"] = score_to_word[item[partial]]

                    rating += float(item[partial])
                    faults += int(item[f"FALTAS_{self.partial}"])

                else:
                    raise InvalidTimePeriod()

            return {
                "TOTAL_FALTAS": faults,
                "PROMEDIO_FINAL": float(f"{rating / len(self.reports):.2f}")
            }
        except ZeroDivisionError:
            pass

    def __add__(self, other):
        details = self.calculate_partials()

        if details == {}:
            return None
        setattr(other, "DETALLES", details)
        return other


class LoadServices:

    @exception_handler
    def get_loads(self, enrollment: str, partial: int) -> list[dict]:
        student = ALUMNO().get(MATRICULA=enrollment, relates=True)
        history_services = HistoryServices()
        rating = Ratings(student.CARGA, partial)
        merged_objs = rating + student

        history_services.set_history(student)

        for load in student.CARGA:
            load["DATOS_MATERIA"] = ASIGNATURA().get_all(
                CLAVE_IN=load["CLAVE_IN"], easy_view=True
            )[-1]

        return student if merged_objs is None else merged_objs
