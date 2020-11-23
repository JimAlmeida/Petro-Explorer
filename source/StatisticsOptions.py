from PySide2.QtWidgets import QWidget, QLabel, QRadioButton, QPushButton, QTextEdit, QFormLayout, QApplication, QLineEdit, QSpinBox
from PySide2.QtCore import Signal
from Dropdown import Dropdown
import sys
import string


class StatisticsOptions(QWidget):
    polymorphic_states = {
      'Regression': {'dtext': 'Tipo de Regressão:', 'xtext': 'Selecione a coluna dos valores correspondentes à variável independente:', 'ytext': 'Selecione a coluna dos valores correspondentes à variável dependente:', 'dropdown': ['Linear', 'Exponencial', 'Logarítmica', 'Potencial', 'Polinomial'], 'ctext':''},
      'Statistics': {'dtext': 'Tipo de análise estatística:', 'xtext': 'Selecione a coluna dos valores para realizar a análise:', 'ytext': '', 'dropdown': ['Média aritmética', 'Mediana', 'Moda', 'Variância Pop.', 'Variância Am.', 'Desvio Padrão Pop.', 'Desvio Padrão Am.', 'Máximo', 'Mínimo', 'Amplitude', 'Quartil', 'Percentil'], 'ctext':''},
      'Histogram':  {'dtext': '', 'xtext': 'Selecione a coluna com os valores:', 'ytext': '', 'dropdown': [], 'ctext':''},
      'Boxplot':    {'dtext': 'Orientação do gráfico:', 'ctext': 'Selecione as colunas onde se encontram as séries para o Boxplot (i.e. B, B:C, A:C:F:G):', 'ytext': '', 'dropdown': ['Vertical', 'Horizontal'], 'xtext':''},
    }
    ready2calculate = Signal(bool)

    def __init__(self, _mode='Regression'):
        super().__init__()

        self.mode = _mode

        self.subtitle = QLabel(str(_mode))

        self.dropdown_text = QLabel(self.polymorphic_states[self.mode]['dtext'])
        self.dropdown_text.setWordWrap(True)
        self.dropdown = Dropdown(self.polymorphic_states[self.mode]['dropdown'])

        self.x_column_text = QLabel(self.polymorphic_states[self.mode]['xtext'])
        self.x_column_text.setWordWrap(True)
        self.x_column = QLineEdit()

        self.y_column_text = QLabel(self.polymorphic_states[self.mode]['ytext'])
        self.y_column_text.setWordWrap(True)
        self.y_column = QLineEdit()

        self.column_range_text = QLabel(self.polymorphic_states[self.mode]['ctext'])
        self.column_range_text.setWordWrap(True)
        self.column_range = QLineEdit()

        self.output_text = QLabel('Select Output:')
        self.output_text.setWordWrap(True)
        self.table_button = QRadioButton('Tabela (Planilha)')
        self.plot_button = QRadioButton('Gráfico (Plot)')
        self.output_destination_text = QLabel('Selecione a coluna onde deve-se armazenar os resultados:')
        self.output_destination_text.setWordWrap(True)
        self.output_destination = QLineEdit()
        self.run_button = QPushButton('Começar Análise')
        self.selected_output = ''

        self.degree_l = QLabel('Ordem:')
        self.degree = QSpinBox()
        self.degree.setRange(1, 6)

        self.quartile_l = QLabel('Quartil:')
        self.quartile = QSpinBox()
        self.quartile.setRange(1, 4)

        self.percentile_l = QLabel('Percentil:')
        self.percentile = QSpinBox()
        self.percentile.setRange(1, 100)

        self.default_degree_stylesheet = self.degree.styleSheet()
        self.default_quartile_stylesheet = self.quartile.styleSheet()
        self.default_percentile_stylesheet = self.percentile.styleSheet()

        self.degree.setDisabled(True)

        self.results_l = QLabel('Resultados da análise: ')
        self.results = QTextEdit()

        self.payload = []

        self.buildLayout()
        self.connections()
        self.initialState()
        self.setStyleSheet('color:white; font-family: Bahnschrift SemiLight Condensed; font-size: 14px;')

        self.x_column.setStyleSheet('background-color: white; color: black')
        self.y_column.setStyleSheet('background-color: white; color: black')
        self.column_range.setStyleSheet('background-color: white; color: black')
        self.results.setStyleSheet('background-color: white; color: black')


    def buildLayout(self):
        layout = QFormLayout()
        if len(self.dropdown_text.text()) > 0:
            layout.addWidget(self.dropdown_text)
            layout.addWidget(self.dropdown)
        if len(self.x_column_text.text()) > 0:
            layout.addWidget(self.x_column_text)
            layout.addWidget(self.x_column)
        if len(self.y_column_text.text()) > 0:
            layout.addWidget(self.y_column_text)
            layout.addWidget(self.y_column)
        if len(self.column_range_text.text()) > 0:
            layout.addWidget(self.column_range_text)
            layout.addWidget(self.column_range)
        if self.mode == 'Statistics':
            layout.addWidget(self.quartile_l)
            layout.addWidget(self.quartile)
            layout.addWidget(self.percentile_l)
            layout.addWidget(self.percentile)
        if self.mode == 'Regression':
            layout.addWidget(self.degree_l)
            layout.addWidget(self.degree)
        layout.addWidget(self.run_button)
        if self.mode != 'Boxplot' and self.mode != "Histogram":
            layout.addWidget(self.results_l)
            layout.addWidget(self.results)

        self.setLayout(layout)

    def initialState(self):
        self.output_destination.setDisabled(True)

    def connections(self):
        self.plot_button.clicked.connect(self.plotSelected)
        self.table_button.clicked.connect(self.tableSelected)
        self.run_button.clicked.connect(self.collectPayload)
        self.dropdown.currentTextChanged.connect(self.enableDegreeBox)

    def columnRangeDecomposition(self, text):
        try:
            return text.split(sep=':')
        except Exception:
            print('A problem happened in decomposing the column ranges. Probable bad user input.')

    def plotSelected(self):
        self.output_destination.setDisabled(True)
        self.selected_output = 'Plot'

    def enableDegreeBox(self, text):
        if text == 'Polinomial':
            self.degree.setStyleSheet('background-color: white; color: black')
            self.degree.setEnabled(True)
        else:
            self.degree.setStyleSheet(self.default_degree_stylesheet)
            self.degree.setDisabled(True)

        if text == 'Quartil':
            self.quartile.setStyleSheet('background-color: white; color: black')
            self.quartile.setEnabled(True)
        else:
            self.quartile.setStyleSheet(self.default_degree_stylesheet)
            self.quartile.setDisabled(True)

        if text == 'Percentil':
            self.percentile.setStyleSheet('background-color: white; color: black')
            self.percentile.setEnabled(True)
        else:
            self.percentile.setStyleSheet(self.default_degree_stylesheet)
            self.percentile.setDisabled(True)


    def tableSelected(self):
        self.output_destination.setDisabled(False)
        self.selected_output = 'Table'

    def collectPayload(self):
        if len(self.column_range_text.text()) > 0:
            a = self.columnRangeDecomposition(self.column_range.text())
            b = 'V'
        else:
            a = None
            b = self.y_column.text()
        payload = {
            'calculate': self.dropdown.currentText(),
            'x_column': self.x_column.text(),
            'y_column': b,
            'z_column': None,
            'column_range': a,
            'output_selection': self.selected_output,
            'output_column': self.output_destination.text()
        }
        self.payload = payload
        self.ready2calculate.emit(True)

def test():
    app = QApplication(sys.argv)
    win = StatisticsOptions(_mode='Statistics')
    win.show()
    sys.exit(app.exec_())
