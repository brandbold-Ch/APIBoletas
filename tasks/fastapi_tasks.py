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
import asyncio
import itertools
from dbf import Table, READ_ONLY, Record, FieldnameList
from services.history_services import HistoryServices
from services.load_services import LoadServices
from utils.db import Collection, get_collection
from utils.logging_config import app_logger
from decorators.handlers import exception_handler

histories = HistoryServices()
load_services = LoadServices()


def asdict(ctx: Record, fields: FieldnameList) -> dict:
    return {k: str(getattr(ctx, k)).strip() for k in fields}


def create_collections(table: Table) -> list[dict]:
    return [asdict(record, table.field_names) for record in table]


@exception_handler
async def each_topic() -> None:
    collection = get_collection(Collection.TOPICS)
    topics = Table("db/asignaturas.dbf")
    topics.open(mode=READ_ONLY)

    await collection.delete_many({})
    await collection.insert_many(create_collections(topics))


@exception_handler
async def each_student() -> None:
    try:
        collection = get_collection(Collection.STUDENTS)
        students = Table("db/alumnos.dbf")
        students.open(mode=READ_ONLY)

        await collection.delete_many({})
        await collection.insert_many(create_collections(students))

    except Exception as e:
        app_logger.error(f"Error on <each_student>: {str(e)}")


@exception_handler
async def each_load() -> None:
    try:
        collection = get_collection(Collection.LOADS)
        loads = Table("db/cargas.dbf")
        loads.open(mode=READ_ONLY)

        await collection.delete_many({})
        await collection.insert_many(create_collections(loads))

    except Exception as e:
        app_logger.error(f"Error on <each_load>: {str(e)}")


@exception_handler
async def each_history() -> None:
    collection = get_collection(Collection.STUDENTS)
    students = await collection.find().to_list(None)

    @exception_handler
    async def check_period(student) -> None:
        for partial in [1, 2, 3]:
            updated_student = await (load_services
                                     .check_academic_load_for_task(student=student, partial=partial))
            await check_student_history(updated_student)

    await asyncio.gather(*(check_period(student) for student in students))


@exception_handler
async def update_records(records, loads, collection, student) -> None:
    filtered_records = [record for record in records
                        if record["GRADO"] == student["GRADO"]]
    updates = []

    for record, load in itertools.product(filtered_records, loads):
        updates_dict = {}

        for key in ["PARCIAL_1", "PARCIAL_2", "PARCIAL_3"]:
            student_value = load[key]
            record_value = record[key]

            if student_value != "None" and record_value == "None":
                updates_dict[key] = student_value

        if updates_dict:
            updates.append(collection.update_one({"_id": record["_id"]},
                                                 {"$set": updates_dict}))

    if updates:
        await asyncio.gather(*updates)


@exception_handler
async def check_student_history(student: dict) -> None:
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
    collection = get_collection(Collection.RECORDS)
    records = await collection.find({"MATRICULA": student["MATRICULA"],
                                     "GRADO": student["GRADO"]}).to_list(None)
    loads = student["CARGA"]

    if len(records) == 0:
        doc = [
            {
                "MATRICULA": student["MATRICULA"],
                "GRUPO": student["GRUPO"],
                "GRADO": student["GRADO"],
                "CLAVEMAT": load["CLAVEMAT"],
                "ASIGNATURA": load["DATOS_MATERIA"]["ASIGNATURA"],
                "PARCIAL_1": load["PARCIAL_1"],
                "PARCIAL_2": load["PARCIAL_2"],
                "PARCIAL_3": load["PARCIAL_3"]
            } for load in loads
        ]
        await collection.insert_many(doc)
    else:
        await update_records(records, loads, collection, student)


@exception_handler
async def main() -> None:
    task1 = asyncio.create_task(each_topic())
    task2 = asyncio.create_task(each_student())
    task3 = asyncio.create_task(each_load())
    task4 = asyncio.create_task(each_history())

    await task1
    await task2
    await task3
    await task4


async def run_main() -> None:
    lock = asyncio.Lock()

    async with lock:
        await main()
