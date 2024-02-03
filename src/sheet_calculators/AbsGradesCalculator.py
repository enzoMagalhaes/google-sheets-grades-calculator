from abc import ABC, abstractmethod
import gspread
import logging


class AbsGradesCalculator(ABC):
    """
    Abstract base class for Google Sheets grades calculation.
    """

    DEFAULT_NUMBER_OF_CLASSES = 60

    def __init__(self, service_account: str, sheet_id: str, worksheet: int = 0) -> None:
        """
        Initialize the grades calculator.

        Arguments:
        - service_account: Google service account JSON file path.
        - sheet_id: Google Sheets document ID.
        - worksheet: Index of the worksheet to use (default is 0).
        """
        # Configure logging
        logging.basicConfig(
            filename="grades_calculator.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d %m %Y %H:%M:%S",
        )

        logging.info("Initializing client and opening worksheet...")

        # Authorize the client using the service account
        try:
            self.client = gspread.service_account(filename=service_account)
            logging.info("Google Sheets client authorized successfully.")
        except Exception as e:
            logging.error(f"Error authorizing Google Sheets client: {e}")
            raise e

        # Open the Google Sheets document by its ID
        try:
            sheet = self.client.open_by_key(sheet_id)
            self.worksheet = sheet.get_worksheet(worksheet)
            logging.info(f"Sheet {sheet_id} opened successfully.")
        except Exception as e:
            logging.error(f"Error opening worksheet: {e}")
            raise e

    @abstractmethod
    def student_status(self, average: float) -> str:
        """
        Abstract method to determine the grade status based on the average score.

        Arguments:
        - average: The average score of a student.

        Returns:
        - A string indicating the grade status.
        """
        pass

    @abstractmethod
    def calculate_naf(self, average: float) -> int:
        """
        Abstract method to calculate the score needed for a final exam.

        Arguments:
        - average: The average score of a student.

        Returns:
        - An integer indicating the score needed for a final exam.
        """
        pass

    def student_result(
        self,
        row: dict,
        exams_cols: list[str],
        absences_col: str,
        number_of_classes: int,
        absences_treshold: float,
    ) -> list[str, int]:
        """
        Calculate the result of a student.

        Arguments:
        - row: Dictionary containing student data.
        - exams_cols: List of columns containing exam scores.
        - absences_col: Column containing the number of absences.
        - number_of_classes: Total number of classes in the semester.
        - absences_treshold: Threshold for considering a student absent.

        Returns:
        - A list containing the student's grade status and the score needed for a final exam.
        """
        try:
            result = ["Reprovado por Falta", 0]
            if row[absences_col] <= number_of_classes * absences_treshold:
                average = 0
                for col in exams_cols:
                    average += row[col]
                average /= len(exams_cols)

                result[0] = self.student_status(average)
                if result[0] == "Exame Final":
                    result[1] = self.calculate_naf(average)

            logging.info(
                f"Student result calculated successfully. data: {row}, result: {result}"
            )
            return result
        except Exception as e:
            logging.error(f"Error processing student info: {e}. Row values: {row}")
            raise e

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
        """
        Run the grades calculation process.

        Arguments:
        - head_row: Row number where the data starts in the worksheet (default is 3).
        - exams_cols: List of columns containing exam scores.
        - num_classes_cell: Cell containing the total number of classes.
        - absences_col: Column containing the number of absences.
        - absences_treshold: Threshold for considering a student absent.
        - output_col: Column where the results will be written (default is "G").
        - update_sheet: Boolean indicating whether to update the worksheet with results.

        Returns:
        - If update_sheet is False, returns a list of student results.
        - If update_sheet is True, updates the worksheet and returns None.
        """
        # get data as a Dataframe
        students = self.worksheet.get_all_records(head=head_row)

        # Get the number of classes lessoned
        try:
            number_of_classes = self.worksheet.acell(num_classes_cell).value
            number_of_classes = int(
                number_of_classes.replace("Total de aulas no semestre: ", "")
            )
            logging.info(
                f"Number of classes retrieved. Number of classes: {number_of_classes}"
            )
        except Exception as e:
            logging.error(
                f"Error getting number of classes: {e}. Using default number of classes ({self.DEFAULT_NUMBER_OF_CLASSES})."
            )
            number_of_classes = self.DEFAULT_NUMBER_OF_CLASSES

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
            try:
                self.worksheet.update(results, f"{output_col}{head_row+1}")
                logging.info("Results updated in the worksheet.")
            except Exception as e:
                logging.error(f"Error updating worksheet: {e}")
                raise e
        else:
            return results
