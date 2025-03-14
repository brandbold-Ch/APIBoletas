"""
This module contains a Celery task that checks the status of students in the 'HISTORIALES.dbf' and
'Alumnos.dbf' tables.
It compares student records in both tables and deletes the histories for students that are no longer
found in the 'Alumnos.dbf' table.
The task ensures that no outdated history records remain in the 'HISTORIALES.dbf' table.

Dependencies:
- utils.celery_config.app: Celery application instance
- dbf.Table, READ_WRITE, READ_ONLY, delete: Functions from the `dbf` library to read and write DBF files
- utils.logging_config.app_logger: Logger for logging task progress and errors
"""

from utils.celery_config import app
from dbf import Table, READ_WRITE, delete, READ_ONLY
from utils.logging_config import app_logger


@app.each_history
def check_student_status() -> None:
    """
    Celery task that checks student status by comparing records in the 'HISTORIALES.dbf' and 'Alumnos.dbf' tables.

    This task performs the following actions:
    - Compares student records from the 'HISTORIALES.dbf' table with those in 'Alumnos.dbf'.
    - Deletes records from the 'HISTORIALES.dbf' table if no matching record is found in the 'Alumnos.dbf' table.
    - Logs the number of deleted history records.

    This is a background task and should be executed periodically to keep student history data up to date.

    Returns:
        None
    """
    histories = Table("db/HISTORIALES.dbf")
    histories.open(mode=READ_WRITE)

    students = Table("db/alumnos.dbf")
    students.open(mode=READ_ONLY)

    counter = 0

    try:
        for history in histories:
            enrollment = history.MATRICULA
            student = students.query(f"SELECT * WHERE matricula=='{enrollment}'")

            if len(student) == 0:
                records = histories.query(f"SELECT * WHERE matricula=='{enrollment}'")

                for record in records:
                    delete(record)
                    counter += 1

                histories.pack()

        app_logger.info(f"Were deleted on <check_student_status>: {counter} histories")

    except Exception as e:
        app_logger.error(f"Error on <check_student_status>: {str(e)}")

    finally:
        histories.close()
        students.close()
