from sheet_calculators import SWEGradesCalculator

swe_grades_calculator = SWEGradesCalculator(
    service_account="./service_account.json",
    sheet_id="1u5BN-kS30TozbcqTxAeEChoPZY-esVaK7S9XkirF0CQ",  # example public sheet (in a real scenario, use an environment variable instead)
)

swe_grades_calculator.run(
    head_row=3,
    exams_cols=["P1", "P2", "P3"],
    num_classes_cell="A2",
    absences_col="Faltas",
    output_col="G",
    update_sheet=True,
)
