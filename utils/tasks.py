from services.history_services import HistoryServices
from models.history_model import HISTORIAL

histories = HistoryServices()


def check_student(student: dict) -> None:
    data = HISTORIAL().get_all(MATRICULA=student["MATRICULA"], GRADO=student["GRADO"])

    if len(data) == 0:
        for item in student["CARGA"]:
            new_history = HISTORIAL()
            new_history.MATRICULA = student["MATRICULA"]
            new_history.GRUPO = student["GRUPO"]
            new_history.GRADO = student["GRADO"]
            new_history.CLAVEMAT = item["CLAVEMAT"]
            new_history.ASIGNATURA = item["DATOS_MATERIA"]["ASIGNATURA"]
            new_history.PARCIAL_1 = item["PARCIAL_1"]
            new_history.PARCIAL_2 = item["PARCIAL_2"]
            new_history.PARCIAL_3 = item["PARCIAL_3"]
            new_history.save()
