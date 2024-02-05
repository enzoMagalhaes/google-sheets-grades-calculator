from .AbsGradesCalculator import AbsGradesCalculator
import math


class ExampleGradesCalculator(AbsGradesCalculator):
    """
    Example class with custom logic for calculating grades in a course.
    Inherits from AbsGradesCalculator.
    """

    absences_treshold = 0.10

    def calculate_grade(self, exams: list[int]) -> float:
        # geometric mean
        mean = 1
        for num in exams:
            mean *= num

        geometric_mean = mean ** (1 / len(exams))
        return geometric_mean

    def student_status(self, grade_result: float) -> str:
        if grade_result < 60:
            return "Reprovado por Nota"
        elif grade_result < 80:
            return "Exame Final"
        else:
            return "Aprovado"

    def calculate_naf(self, grade_result: float) -> int:
        return math.floor(100 - grade_result * 0.8)
