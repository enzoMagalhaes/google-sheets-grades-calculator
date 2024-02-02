from calculators.SWEGradesCalculator import SWEGradesCalculator

swe_grades_calculator = SWEGradesCalculator(
    service_account="./service_account.json",
    sheet_id="1u5BN-kS30TozbcqTxAeEChoPZY-esVaK7S9XkirF0CQ",
)

swe_grades_calculator.run(
    head_row=3,
    exams_cols=["P1", "P2", "P3"],
    absences_col="Faltas",
    absences_treshold=0.25,
    update_sheet=True,
)
