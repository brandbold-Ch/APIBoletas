from errors.errors import InvalidTimePeriod


def validate_partials(partials: list[str]) -> bool:
    """
    Validates if all partial exams are completed.

    Args:
        partials (list[str]): List of partial exam results, where 'None' indicates an incomplete exam.

    Returns:
        bool: True if all partials are completed, False otherwise.
    """
    partials = [False if x == 'None' else True for x in partials]

    if all(partials):
        return True

    else:
        return False


class Ratings:
    """
    A class for calculating student ratings based on partial exams and semiannual averages.

    Attributes:
        reports (list[dict]): A list of dictionaries representing the student reports with partial exam results.
        partial (int): The partial exam number (1, 2, 3, or 6 for semiannual).
        ratings (dict): A dictionary mapping numeric grades to corresponding grade words and status (e.g., "REPROBADO" or "APROBADO").
    """

    def __init__(self, reports: list[dict], partial: int) -> None:
        """
        Initializes the Ratings object with the student reports and partial exam number.

        Args:
            reports (list[dict]): A list of dictionaries containing partial exam results for different subjects.
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

            else:
                raise InvalidTimePeriod("You have not completed the three partials 🕓️")

        except ZeroDivisionError:
            pass

    def _calculate_partials(self) -> dict:
        """
        Calculates the average grade for a specific partial exam period.

        This method calculates the grade for the selected partial (e.g., PARCIAL_1, PARCIAL_2, or PARCIAL_3),
        assigns the corresponding grade word and observation, and returns the final average and total absences for the partial.

        Returns:
            dict: A dictionary containing the total absences ("TOTAL_FALTAS") and the final average grade ("PROMEDIO_FINAL").

        Raises:
            InvalidTimePeriod: If the partial exam is not completed.
        """
        try:
            rating, faults = 0.0, 0
            chunk = f"PARCIAL_{self.partial}"

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
        except ZeroDivisionError:
            pass

    def __add__(self, other):
        """
        Adds the calculated ratings to the given student object.

        This method allows for the addition of a `Ratings` object to a student object,
        which then contains the calculated ratings in the `DETALLES` attribute.

        Args:
            other: The student object to which the ratings details will be added.

        Returns:
            The student object with the added "DETALLES" attribute.
        """
        details = None

        if self.partial == 0:
            return None

        elif 1 <= self.partial <= 3:
            details = self._calculate_partials()

        elif self.partial == 6:
            details = self._calculate_semiannual()

        setattr(other, "DETALLES", details)
        return other
