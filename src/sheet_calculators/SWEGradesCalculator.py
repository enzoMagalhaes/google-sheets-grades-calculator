from .AbsGradesCalculator import AbsGradesCalculator
import math


class SWEGradesCalculator(AbsGradesCalculator):
    """
    Class with custom logic for calculating grades in Software Engineering course.
    Inherits from AbsGradesCalculator.
    """

    def calculate_grade(self, exams: list[int]) -> float:
        # simple mean
        return sum(exams) / len(exams)

    def student_status(self, grade_result: float) -> str:
        if grade_result < 50:
            return "Reprovado por Nota"
        elif grade_result < 70:
            return "Exame Final"
        else:
            return "Aprovado"

    def calculate_naf(self, grade_result: float) -> int:
        # REVIEW THAT LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return math.ceil(100 - grade_result)
