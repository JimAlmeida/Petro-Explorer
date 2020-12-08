from PySide2.QtWidgets import QWidget, QLabel, QTextEdit, QRadioButton, QPushButton, QFormLayout, QApplication, QLineEdit
from PySide2.QtCore import Signal
import sys
import Dropdown

#add mechanism for redefining a,b,c constants in TCoates and Winland calculations
#maybe change the destination columns for when there's a graph involved?


class PetrophysicsOptions(QWidget):
    polymorphic_states = {
        'DParsons': {'param1': 'Coeficiente de Dykstra-Parsons', 'param2': 'Grau de heterogenêidade', 'param3': '', 'param4': '', 'prop1': ['Permeabilidade (mD)'], 'prop2': ['Permeabilidade (mD)'], 'prop3': '', 'prop4': ''},
        'Winland': {'param1': 'Garganta de Poro (Winland R35)', 'param2': '', 'param3': '', 'param4': '', 'prop1': ['Permeabilidade (mD)', 'Porosidade (%)'], 'prop2': 'Porosidade (%)', 'prop3': '', 'prop4': ''},
        'Lucia': {'param1': 'Classificação de Lucia (Gráfico de classes carbonáticas)', 'param2': '', 'param3': '', 'param4': '', 'prop1': ['Permeabilidade (mD)', 'Porosidade Interpartícula (%)'], 'prop2': '', 'prop3': '', 'prop4': ''},
        'RQIFZI':  {'param1': 'RQI (μm)', 'param2': 'FZI (gráfico)', 'param3': '', 'param4': '', 'prop1': ['Permeabilidade', 'Porosidade (%)'], 'prop2': ['Permeabilidade', 'Porosidade (%)'], 'prop3': [], 'prop4': []},
        'TCoates':  {'param1': 'FFI', 'param2': 'BVI', 'param3': 'Permeabilidade (mD)', 'param4': 'Swir (%)', 'prop1': ['Swir (%)', 'Porosidade (%)'], 'prop2': ['Swir (%)', 'Porosidade (%)'], 'prop3': ['Swir (%)', 'Porosidade (%)'], 'prop4': ['Permeabilidade (mD)', 'Porosidade (%)']},
        'KCarman': {'param1': 'Permeabilidade (mD)', 'param2': 'SVgr (cm-1)', 'param3': '', 'param4': '', 'prop1': ['Porosidade (%)', 'SVgr (cm-1)'], 'prop2': ['Permeabilidade (mD)', 'Porosidade (%)'], 'prop3': ['Permeabilidade (cm²)', 'Porosidade (decimal)'], 'prop4': []}
    }
    ready2calculate = Signal(bool)

    def __init__(self, _mode='KCarman'):
        super().__init__()

        self.mode = _mode

        self.subtitle = QLabel('Calcular:')

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()

        self.labels = [self.label1, self.label2, self.label3, self.label4]

        for l in self.labels:
            l.setWordWrap(True)

        self.param1 = QRadioButton()
        self.param2 = QRadioButton()
        self.param3 = QRadioButton()
        self.param4 = QRadioButton()

        self.x_column = QLineEdit()
        self.y_column = QLineEdit()
        self.z_column = QLineEdit()
        self.destination_column = QLineEdit()

        self.results_l = QLabel('Resultados da análise: ')
        self.results = QTextEdit()

        self.unit_selector = Dropdown.Dropdown(['Darcy', 'SI'])

        self.run = QPushButton('Começar Análise')

        self.connections()
        self.changeMode(_mode)
        self.buildLayout()

        self.property_to_calculate = self.property_to_calculate = self.polymorphic_states[self.mode]['param1']
        self.payload = {}

        stly_sheet = "QRadioButton::indicator {width: 13px; height: 13px;} QRadioButton::indicator::unchecked {image: url(:/images/radiobutton_unchecked.png)} QRadioButton::indicator:unchecked:hover {image: url(:/images/radiobutton_unchecked_hover.png);}"

        self.subtitle.setStyleSheet('color: white')
        self.label1.setStyleSheet('color: white')
        self.label2.setStyleSheet('color: white')
        self.label3.setStyleSheet('color: white')
        self.label4.setStyleSheet('color: white')
        self.param1.setStyleSheet('color: white')
        self.param2.setStyleSheet('color: white')
        self.param3.setStyleSheet('color: white')
        self.param4.setStyleSheet('color: white')
        self.x_column.setStyleSheet('background-color: white; color: black')
        self.y_column.setStyleSheet('background-color: white; color: black')
        self.z_column.setStyleSheet('background-color: white; color: black')
        self.results.setStyleSheet('background-color: white; color: black')
        self.setStyleSheet('color:white; font-family: Bahnschrift SemiLight Condensed; font-size: 14px;')


    def buildLayout(self):
        layout = QFormLayout()

        a = self.polymorphic_states[self.mode]['prop1']
        b = self.polymorphic_states[self.mode]['prop2']
        c = self.polymorphic_states[self.mode]['prop3']
        d = self.polymorphic_states[self.mode]['prop4']

        layout.addWidget(self.subtitle)

        if len(self.param1.text()) != 0:
            layout.addWidget(self.param1)
        if len(self.param2.text()) != 0:
            layout.addWidget(self.param2)
        if len(self.param3.text()) != 0:
            layout.addWidget(self.param3)
        if len(self.param4.text()) != 0:
            layout.addWidget(self.param4)

        if len(self.label1.text()) != 0:
            layout.addWidget(self.label1)
            layout.addWidget(self.x_column)
        if len(self.label2.text()) != 0:
            layout.addWidget(self.label2)
            layout.addWidget(self.y_column)
        if len(self.label3.text()) != 0:
            layout.addWidget(self.label3)
            layout.addWidget(self.z_column)
        #if len(self.label4.text()) != 0:
            #layout.addWidget(self.label4)
            #layout.addWidget(self.destination_column)

        if self.mode == 'RQIFZI':
            layout.addWidget(QLabel('Sistema de Unidades: '))
            layout.addWidget(self.unit_selector)

        layout.addWidget(self.run)

        if self.mode == 'DParsons':
            layout.addWidget(self.results_l)
            layout.addWidget(self.results)
        if self.mode == 'Lucia':
            layout.addWidget(self.results_l)
            layout.addWidget(self.results)

        self.setLayout(layout)

    def connections(self):
        self.param1.clicked.connect(self.param1Active)
        self.param2.clicked.connect(self.param2Active)
        self.param3.clicked.connect(self.param3Active)
        self.param4.clicked.connect(self.param4Active)
        self.run.clicked.connect(self.collectPayload)

    def changeMode(self, _mode):
        self.mode = _mode
        self.param1.setText(self.polymorphic_states[self.mode]['param1'])
        self.param1.click()
        self.param2.setText(self.polymorphic_states[self.mode]['param2'])
        self.param3.setText(self.polymorphic_states[self.mode]['param3'])
        self.param4.setText(self.polymorphic_states[self.mode]['param4'])

    def param1Active(self):
        self.label1.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop1'][0])
        try:
            self.label2.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop1'][1])
        except IndexError:
            self.label2.setText('')
        try:
            self.label3.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop1'][2])
        except IndexError:
            self.label3.setText('')
        self.label4.setText('Selecione a coluna para os valores de ' + self.polymorphic_states[self.mode]['param1'])
        self.property_to_calculate = self.polymorphic_states[self.mode]['param1']

    def param2Active(self):
        self.label1.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop2'][0])
        try:
            self.label2.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop2'][1])
        except IndexError:
            self.label2.setText('')
        try:
            self.label3.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop2'][2])
        except IndexError:
            self.label3.setText('')
        self.label4.setText('Selecione a coluna para os valores de ' + self.polymorphic_states[self.mode]['param2'])
        self.property_to_calculate = self.polymorphic_states[self.mode]['param2']

    def param3Active(self):
        self.label1.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop3'][0])
        try:
            self.label2.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop3'][1])
        except IndexError:
            self.label2.setText('')
        try:
            self.label3.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop3'][2])
        except IndexError:
            self.label3.setText('')
        self.label4.setText('Selecione a coluna para os valores de ' + self.polymorphic_states[self.mode]['param3'])
        self.property_to_calculate = self.polymorphic_states[self.mode]['param3']

    def param4Active(self):
        self.label1.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop4'][0])
        try:
            self.label2.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop4'][1])
        except IndexError:
            self.label2.setText('')
        try:
            self.label3.setText('Selecione a coluna com os valores de ' + self.polymorphic_states[self.mode]['prop4'][2])
        except IndexError:
            self.label3.setText('')
        self.label4.setText('Selecione a coluna para os valores de ' + self.polymorphic_states[self.mode]['param4'])
        self.property_to_calculate = self.polymorphic_states[self.mode]['param4']

    def collectPayload(self):
        payload = {
            'calculate': self.property_to_calculate,
            'x_column': self.x_column.text(),
            'y_column': self.y_column.text(),
            'z_column': self.z_column.text(),
            'column_range': self.unit_selector.currentText(),
            'output_selection': None,
            'output_column': self.destination_column.text()
        }
        self.payload = payload
        print(payload)
        self.ready2calculate.emit(True)

def test():
    app = QApplication(sys.argv)
    win = PetrophysicsOptions(_mode='TCoates')
    win.show()
    sys.exit(app.exec_())
