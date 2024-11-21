from errors.errors import InvalidTimePeriod


class Ratings:

    def __init__(self, reports: list[dict], partial: int) -> None:
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

    def _validate_partials(self, partials: list[str]) -> bool:
        partials = [False if x == 'None' else True for x in partials]

        if all(partials):
            return True

        else:
            return False

    def _calculate_semiannual(self) -> dict:
        try:
            rating, average_by_subject = 0.0, 0

            for item in self.reports:
                check = self._validate_partials(
                    [
                        item["PARCIAL_1"],
                        item["PARCIAL_2"],
                        item["PARCIAL_3"]
                    ]
                )

                if check:
                    average_by_subject += (float(item["PARCIAL_1"]) +
                                           float(item["PARCIAL_2"]) +
                                           float(item["PARCIAL_3"]))
                    item["PROMEDIO"] = round(float(f"{average_by_subject / 3:.2f}"))
                    item["PALABRA"], item["OBSERVA"] = self.ratings[f"{item['PROMEDIO']}.0"]
                    rating += item["PROMEDIO"]
                    average_by_subject = 0

                else:
                    raise InvalidTimePeriod("You have not completed the three partials 🕓️")

            return {
                "PROMEDIO_FINAL": float(f"{rating / len(self.reports):.2f}")
            }
        except ZeroDivisionError:
            pass

    def _calculate_partials(self) -> dict:
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
        details = None

        if self.partial == 0:
            return None

        elif 1 <= self.partial <= 3:
            details = self._calculate_partials()

        elif self.partial == 6:
            details = self._calculate_semiannual()

        setattr(other, "DETALLES", details)
        return other
