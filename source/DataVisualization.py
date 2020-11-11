from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QApplication, QToolButton
import sys

class DataVisualization(QWidget):
    def __init__(self):
        super().__init__()

        self.show_table = QToolButton()
        self.show_plot = QToolButton()

        self.l1 = QLabel('Ver tabela')
        self.l2 = QLabel('Ver gráfico')

        self.title = QLabel('Modos de visualização')

    def buildLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.title, 0, 0, columnSpan=2)
        layout.addWidget(self.l1, 1, 0)
        layout.addWidget(self.l2, 1, 1)
        layout.addWidget(self.show_table, 2, 0)
        layout.addWidget(self.show_plot, 2, 1)
        self.setLayout(layout)

    def loadTable(self):
        pass

    def loadPlot(self):
        pass
