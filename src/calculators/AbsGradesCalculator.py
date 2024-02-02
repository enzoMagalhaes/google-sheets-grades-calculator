from abc import ABC, abstractmethod
import gspread
import pandas as pd


class AbsGradesCalculator(ABC):

    def __init__(self, service_account: str, sheet_id: str, worksheet: int = 0) -> None:
        # Authorize the client using the service account
        self.client = gspread.service_account(filename=service_account)

        # Open the Google Sheets document by its ID
        sheet = self.client.open_by_key(sheet_id)

        # get the first sheet page of the document
        self.worksheet = sheet.get_worksheet(worksheet)

    @abstractmethod
    def grade_thresholds(self, average: float) -> str:
        pass

    @abstractmethod
    def calculate_naf(self, average: float) -> int:
        pass

    def compute_student_result(
        self,
        row: pd.Series,
        exams_cols: list[str],
        absences_col: str,
        absences_treshold: float,
    ) -> pd.Series:
        if row[absences_col] > self.number_of_classes * absences_treshold:
            row["Situação"] = "Reprovado por Falta"
            row["Nota para Aprovação Final"] = 0
        else:
            average = 0
            for col in exams_cols:
                average += row[col]
            average /= len(exams_cols)

            row["Situação"] = self.grade_thresholds(average)
            if row["Situação"] == "Exame Final":
                row["Nota para Aprovação Final"] = self.calculate_naf(average)
            else:
                row["Nota para Aprovação Final"] = 0

        return row

    def run(
        self,
        head_row: int = 3,
        exams_cols: list[str] = ["P1", "P2", "P3"],
        absences_col: str = "Faltas",
        absences_treshold: float = 0.25,
        update_sheet: bool = False,
    ) -> None | pd.DataFrame:
        # get data as a Dataframe
        df = pd.DataFrame.from_dict(self.worksheet.get_all_records(head=head_row))

        # Get the number of classes lessoned
        number_of_classes_cell = self.worksheet.cell(2, 1).value
        self.number_of_classes = int(
            number_of_classes_cell.replace("Total de aulas no semestre: ", "")
        )

        df = df.apply(
            self.compute_student_result,
            axis=1,
            args=(exams_cols, absences_col, absences_treshold),
        )

        if update_sheet:
            self.worksheet.update(
                df[["Situação", "Nota para Aprovação Final"]].values.tolist(), "G4"
            )
        else:
            return df
