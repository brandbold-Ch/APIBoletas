"""
This module defines the `Ratings` class, which is responsible for calculating and managing
the academic ratings of students based on their partial exams and semiannual averages.
It also includes a helper function to validate if all partial exams have been completed.

Key Features:
- Calculates ratings for each student based on their partial exam results and semiannual averages.
- Provides detailed information on student performance, including word equivalents and status
("APROBADO" or "REPROBADO").
- Handles incomplete exams by raising an `InvalidTimePeriod` exception.

Functions:
- `validate_partials`: Validates whether all partial exams are completed.
    - Args: A list of partial exam results where 'None' indicates an incomplete exam.
    - Returns: True if all partials are completed, False otherwise.

Classes:
- `Ratings`: A class for calculating and assigning ratings to student exams.
    - Attributes:
        - `reports`: A list of dictionaries representing the student reports with partial exam results.
        - `partial`: The partial exam number (1, 2, 3, or 6 for semiannual).
        - `ratings`: A dictionary mapping numeric grades to corresponding grade words and status.
    - Methods:
        - `_calculate_semiannual`: Calculates the semiannual average based on the student's partial exam results.
        - `_calculate_partials`: Calculates the average grade for a specific partial exam period.
        - `__add__`: Adds the calculated ratings to the given student object and stores the details in the
        `DETALLES` attribute.

Exceptions:
- `InvalidTimePeriod`: Raised if any required partial exam has not been completed.

Usage:
The `Ratings` class is used to calculate the student's academic performance and ratings based on their exam results.
It adds the calculated ratings to the student object, which includes detailed results for each subject and partial.

Example:
    student = Ratings(student_reports, partial_exam_number)
    student_with_details = student + student_object  # Adds calculated ratings to student object

    On success:
        Returns the student object with the added `DETALLES` attribute containing ratings.

    On failure:
        Raises an `InvalidTimePeriod` exception if exams are incomplete.
"""
from errors.errors import InvalidTimePeriod, ServerError


def validate_partials(partials: list[str]) -> bool:
    """
    Validates if all partial exams are completed.

    Args:
        partials (list[str]): List of partial exam results,
        where 'None' indicates an incomplete exam.

    Returns:
        bool: True if all partials are completed, False otherwise.
    """
    partials = [False if x == 'None' else True for x in partials]
    return all(partials)


class Ratings:
    """
    A class for calculating student ratings based on partial
    exams and semiannual averages.

    Attributes:
        reports (list[dict]): A list of dictionaries representing
        the student reports with partial exam results.
        partial (int): The partial exam number (1, 2, 3, or 6 for semiannual).
        ratings (dict): A dictionary mapping numeric grades to corresponding
        grade words and status (e.g., "REPROBADO" or "APROBADO").
    """

    def __init__(self, reports: list[dict], partial: int) -> None:
        """
        Initializes the Ratings object with the student reports and
        partial exam number.

        Args:
            reports (list[dict]): A list of dictionaries containing
            partial exam results for different subjects.
            partial (int): The partial exam number (1, 2, 3, or 6 for semiannual).
        """
        self.reports = reports
        self.partial = partial
        self.ratings = {
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

    def _calculate_semiannual(self) -> dict:
        """
        Calculates the semiannual average for the student.

        This method calculates the average of the three partial exams for each subject,
        then calculates the overall semiannual average and assigns corresponding grade words.

        Returns:
            dict: A dictionary containing the final average grade ("PROMEDIO_FINAL").

        Raises:
            InvalidTimePeriod: If not all three partial exams are completed.
        """
        try:
            check_partial_one = validate_partials([
                self.reports[0]["PARCIAL_1"],
                self.reports[0]["PARCIAL_2"],
                self.reports[0]["PARCIAL_3"],
            ])

            if check_partial_one:
                rating, average_by_subject = 0.0, 0

                for item in self.reports:
                    average_by_subject += (float(item["PARCIAL_1"]) +
                                           float(item["PARCIAL_2"]) +
                                           float(item["PARCIAL_3"]))
                    item["PROMEDIO"] = round(float(f"{average_by_subject / 3:.2f}"))
                    item["PALABRA"], item["OBSERVA"] = self.ratings[f"{item['PROMEDIO']}.0"]
                    rating += item["PROMEDIO"]
                    average_by_subject = 0

                return {
                    "PROMEDIO_FINAL": float(f"{rating / len(self.reports):.2f}")
                }

            raise InvalidTimePeriod("You have not completed the three partials 🕓️")

        except ZeroDivisionError as e:
            raise ServerError(e) from e

        except IndexError:
            raise InvalidTimePeriod("There is no data on that history. 📋️")

    def _calculate_partials(self) -> dict:
        """
        Calculates the average grade for a specific partial exam period.

        This method calculates the grade for the selected partial
        (e.g., PARCIAL_1, PARCIAL_2, or PARCIAL_3),
        assigns the corresponding grade word and observation,
        and returns the final average and total absences for the partial.

        Returns:
            dict: A dictionary containing the total absences ("TOTAL_FALTAS")
            and the final average grade ("PROMEDIO_FINAL").

        Raises:
            InvalidTimePeriod: If the partial exam is not completed.
        """
        try:
            rating, faults = 0.0, 0
            chunk = f"PARCIAL_{self.partial}"

            if len(self.reports) == 0:
                raise InvalidTimePeriod()

            for item in self.reports:
                if item[chunk] != "None":
                    item["PALABRA"], item["OBSERVA"] = self.ratings[item[chunk]]
                    rating += float(item[chunk])
                    faults += int(item.get(f"FALTAS_{self.partial}", 0))

                else:
                    raise InvalidTimePeriod()

            return {
                "TOTAL_FALTAS": faults,
                "PROMEDIO_FINAL": float(f"{rating / len(self.reports):.2f}")
            }

        except ZeroDivisionError as e:
            raise ServerError(e) from e

    def score(self, student: dict):
        """
        Adds the calculated ratings to the given student object.

        This method allows for the addition of a `Ratings` object to a student object,
        which then contains the calculated ratings in the `DETALLES` attribute.

        Args:
            other: The student object to which the ratings details will be added.

        Returns:
            The student object with the added "DETALLES" attribute.
            :param student:
        """
        details = None

        if 1 <= self.partial <= 3:
            details = self._calculate_partials()

        elif self.partial == 6:
            details = self._calculate_semiannual()

        elif self.partial == 0:
            return student

        student["DETALLES"] = details
        return student
