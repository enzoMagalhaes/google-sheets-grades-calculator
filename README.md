## Calculadora de Notas

Este projeto consiste em uma calculadora de notas desenvolvida para auxiliar no cálculo e gerenciamento de notas de alunos em diferentes cursos utilizando o Google Sheets. Ele permite calcular e gerenciar notas com base em resultados de exames e registros de frequência.

### Funcionalidades

- Calcula as notas finais dos alunos com base nas notas dos exames.
- Determina o status da nota (Aprovado, Exame Final, Reprovado) com base na nota calculada.
- Calcula a nota necessária para um exame final, se aplicável.
- Suporta personalização para diferentes critérios de avaliação.

### Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/enzoMagalhaes/google-sheets-grades-calculator
2. Instale as dependências necessárias:
   ```bash
    pip install -r requirements.txt

3. Certifique-se de ter um arquivo service account JSON da Google Cloud com permissões adequadas. Mais informações para a criação de uma service account [aqui](https://docs.gspread.org/en/latest/oauth2.html) e [aqui](https://owaisqureshi.medium.com/access-google-sheets-api-in-python-using-service-account-3a0c6d89d5fc).

4. Atualize a configuração no arquivo `calculate_swe_grades.py`:
    * `service_account`: Caminho para o seu arquivo service account JSON da Google Cloud.
    * `sheet_id`: ID do documento Google Sheets contendo os dados dos alunos.

### Como Rodar

1. Instancie a classe SWEGradesCalculator com os parâmetros necessários:
   ```python
    from sheet_calculators import SWEGradesCalculator

    swe_grades_calculator = SWEGradesCalculator(
        service_account="./service_account.json",
        sheet_id="SEU_ID_DE_PLANILHA",
    )

2. Execute o programa para calcular as notas:
   ```python
    swe_grades_calculator.run(
        head_row=3,
        exams_cols=["P1", "P2", "P3"],
        num_classes_cell="A2",
        absences_col="Faltas",
        output_col="G",
        update_sheet=True,
    )

#### Configuração

* `head_row`: Número da linha do cabeçalho da tabela.
* `exams_cols`: Lista de colunas contendo as notas dos exames.
* `num_classes_cell`: Célula contendo o número total de aulas.
* `absences_col`: Coluna contendo o número de faltas.
* `absences_treshold`: Limiar para considerar um aluno ausente.
* `output_col`: Coluna onde os resultados serão escritos.
* `update_sheet`: Booleano indicando se a planilha deve ser atualizada com os resultados.

# Como criar a calculadora para o seu próprio curso
Para personalizar a lógica de cálculo de notas para seu curso específico, você pode estender a classe AbsGradesCalculator e implementar os métodos necessários (calculate_grade, student_status, calculate_naf) de acordo com seus critérios de avaliação (veja `ExampleGradesCalculator.py`).