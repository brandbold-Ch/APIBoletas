"""
This file contains the logic for managing and updating student historical records.

The file implements the `check_student` function, which is responsible for checking
if a student has existing historical records in the system.
If no records are found, the function creates new records for each subject the student is enrolled in.
If historical records already exist, the function updates the records with missing partial exam grades.

The workflow is as follows:
1. The `check_student` function queries whether hidata exists for a student based on their matriculation number and grade.
2. If no historical records are found, the function creates new records for each enrolled subject.
3. If historical records already exist, the function updates the fields for any partial exams that are missing grades.

Dependencies:
- `HistoryServices`: Service handling logic related to student historical records.
- `HISTORIAL`: Data model representing the historical records of students.

This file ensures that student historical records are complete and up-to-date for further processing or academic evaluation.
"""

from dbf import Table, READ_ONLY
from errors.errors import InvalidTimePeriod
from models.load_model import CARGA
from services.history_services import HistoryServices
from models.history_model import HISTORIAL
from services.load_services import LoadServices

histories = HistoryServices()
load_services = LoadServices()


def each_student():
    students_loads = Table("db/Alumnos.dbf")
    students_loads.open(mode=READ_ONLY)

    for student in students_loads:
        for item in [1, 2, 3]:
            try:
                user = load_services.get_academic_load(student.MATRICULA, item)
                check_student_history(user.to_repr())
            except InvalidTimePeriod:
                ...


def check_student_history(student: dict) -> None:
    """
    Checks if the student's historical data exists and updates or creates
    new history records accordingly.

    This function verifies if the student already has a history record in the
    system based on their matriculation number and grade.
    If no history is found, it creates new records for
    each subject the student is enrolled in.
    If history already exists, it updates the records where necessary,
    particularly for missing partial exam scores.

    Args:
        student (dict): A dictionary containing student information,
                        including matriculation number, grade, group,
                        and their subject load with corresponding
                        partial exam grades.

    Returns:
        None: This function does not return any value. It modifies the history
        records in the database directly.
    """
    data = HISTORIAL().get_all(MATRICULA=student["MATRICULA"], GRADO=student["GRADO"])
    loads = student["CARGA"]
    print(data)

    if len(data) == 0:
        for load in loads:
            new_history = HISTORIAL()
            new_history.MATRICULA = student["MATRICULA"]
            new_history.GRUPO = student["GRUPO"]
            new_history.GRADO = student["GRADO"]
            new_history.CLAVEMAT = load["CLAVEMAT"]
            new_history.ASIGNATURA = load["DATOS_MATERIA"]["ASIGNATURA"]
            new_history.PARCIAL_1 = load["PARCIAL_1"]
            new_history.PARCIAL_2 = load["PARCIAL_2"]
            new_history.PARCIAL_3 = load["PARCIAL_3"]
            new_history.save()

    else:
        for index, history in enumerate(data):
            student_partial_1 = loads[index]["PARCIAL_1"]
            student_partial_2 = loads[index]["PARCIAL_2"]
            student_partial_3 = loads[index]["PARCIAL_3"]

            history_partial_1 = history.PARCIAL_1
            history_partial_2 = history.PARCIAL_2
            history_partial_3 = history.PARCIAL_3

            if student_partial_1 != "None" and history_partial_1 == "None":
                history.PARTIAL_1 = student_partial_1

            if student_partial_2 != "None" and history_partial_2 == "None":
                history.PARTIAL_2 = student_partial_2

            if student_partial_3 != "None" and history_partial_3 == "None":
                history.PARTIAL_3 = student_partial_3

            history.save()
