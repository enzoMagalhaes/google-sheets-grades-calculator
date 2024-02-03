from .AbsGradesCalculator import AbsGradesCalculator
import math


class SWEGradesCalculator(AbsGradesCalculator):
    """
    Class with custom logic for calculating grades in Software Engineering course.
    Inherits from AbsGradesCalculator.
    """

    def student_status(self, average: float) -> str:
        if average < 50:
            return "Reprovado por Nota"
        elif average < 70:
            return "Exame Final"
        else:
            return "Aprovado"

    def calculate_naf(self, average: float) -> int:
        # REVIEW THAT LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return math.ceil(100 - average)
