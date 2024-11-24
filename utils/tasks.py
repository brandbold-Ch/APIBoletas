from services.history_services import HistoryServices
from models.history_model import HISTORIAL

histories = HistoryServices()


def check_student(student: dict) -> None:
    """
    Checks if the student's historical data exists and updates or creates new history records accordingly.

    This function verifies if the student already has a history record in the system based on their matriculation number and grade.
    If no history is found, it creates new records for each subject the student is enrolled in.
    If history already exists, it updates the records where necessary, particularly for missing partial exam scores.

    Args:
        student (dict): A dictionary containing student information, including matriculation number, grade, group,
                        and their subject load with corresponding partial exam grades.

    Returns:
        None: This function does not return any value. It modifies the history records in the database directly.
    """
    data = HISTORIAL().get_all(MATRICULA=student["MATRICULA"], GRADO=student["GRADO"])
    student_loads = student["CARGA"]

    if len(data) == 0:
        for item in student_loads:
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

    else:
        for index, history in enumerate(data):
            student_partial_1 = student_loads[index]["PARCIAL_1"]
            student_partial_2 = student_loads[index]["PARCIAL_2"]
            student_partial_3 = student_loads[index]["PARCIAL_3"]

            history_partial_1 = history.PARCIAL_1
            history_partial_2 = history.PARCIAL_2
            history_partial_3 = history.PARCIAL_3

            if student_partial_1 != "None" and history_partial_1 == "None":
                history.PARTIAL_1 = student_partial_1
                print(student_partial_1 != "None" and history_partial_1 == "None")

            if student_partial_2 != "None" and history_partial_2 == "None":
                history.PARTIAL_2 = student_partial_2
                print(student_partial_2 != "None" and history_partial_2 == "None")

            if student_partial_3 != "None" and history_partial_3 == "None":
                history.PARTIAL_3 = student_partial_3
                print(student_partial_3 != "None" and history_partial_3 == "None")

            history.save()
