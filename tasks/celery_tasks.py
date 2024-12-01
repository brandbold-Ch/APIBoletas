from utils.celery_config import app
from dbf import Table, READ_WRITE, delete, READ_ONLY
from utils.logging_config import celery_logger
from subprocess import run

@app.task
def check_student_status() -> None:
    histories = Table("../db/HISTORIALES.dbf")
    histories.open(mode=READ_WRITE)

    student = Table("../db/Alumnos.dbf")
    student.open(mode=READ_ONLY)

    counter = 0

    run("code .", shell=True)

    try:
        for item_1 in histories:
            enrollment = item_1.MATRICULA
            student_found = student.query(f"SELECT * WHERE matricula=='{enrollment}'")
            print(enrollment)

            if len(student_found) == 0:
                histories_found = histories.query(f"SELECT * WHERE matricula=='{enrollment}'")

                for item_2 in histories_found:
                    delete(item_2)
                    counter += 1
                histories.pack()

        celery_logger.info(f"Were deleted on <check_student_status>: {counter} histories")

    except Exception as e:
        celery_logger.error(f"Error on <check_student_status>: {str(e)}")

    finally:
        histories.close()
        student.close()
