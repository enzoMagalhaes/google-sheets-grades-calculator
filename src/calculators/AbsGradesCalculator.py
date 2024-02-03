from abc import ABC, abstractmethod
import gspread


class AbsGradesCalculator(ABC):

    def __init__(self, service_account: str, sheet_id: str, worksheet: int = 0) -> None:
        # Authorize the client using the service account
        self.client = gspread.service_account(filename=service_account)

        # Open the Google Sheets document by its ID
        sheet = self.client.open_by_key(sheet_id)

        # get the sheet page of the document
        self.worksheet = sheet.get_worksheet(worksheet)

    @abstractmethod
    def grade_thresholds(self, average: float) -> str:
        pass

    @abstractmethod
    def calculate_naf(self, average: float) -> int:
        pass

    def student_result(
        self,
        row: dict,
        exams_cols: list[str],
        absences_col: str,
        number_of_classes: int,
        absences_treshold: float,
    ) -> list[str, int]:

        result = ["Reprovado por Falta", 0]
        if row[absences_col] <= number_of_classes * absences_treshold:
            average = 0
            for col in exams_cols:
                average += row[col]
            average /= len(exams_cols)

            result[0] = self.grade_thresholds(average)
            if result[0] == "Exame Final":
                result[1] = self.calculate_naf(average)

        return result

    def run(
        self,
        head_row: int = 3,
        exams_cols: list[str] = ["P1", "P2", "P3"],
        num_classes_cell: str = "A2",
        absences_col: str = "Faltas",
        absences_treshold: float = 0.25,
        output_col: str = "G",
        update_sheet: bool = False,
    ) -> None | list[str, int]:
        # get data as a Dataframe
        students = self.worksheet.get_all_records(head=head_row)

        # Get the number of classes lessoned
        number_of_classes = self.worksheet.acell(num_classes_cell).value
        number_of_classes = int(
            number_of_classes.replace("Total de aulas no semestre: ", "")
        )

        results = []
        for student in students:
            results.append(
                self.student_result(
                    student,
                    exams_cols,
                    absences_col,
                    number_of_classes,
                    absences_treshold,
                )
            )

        if update_sheet:
            self.worksheet.update(results, f"{output_col}{head_row+1}")
        else:
            return results
