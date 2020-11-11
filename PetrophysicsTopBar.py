from PySide2.QtWidgets import QWidget, QToolButton, QAction, QHBoxLayout, QApplication, QToolBar
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Signal, QSize, Qt
import sys


class PetrophysicsTopBar(QToolBar):
    KCarman = Signal(bool)
    TCoates = Signal(bool)
    Winland = Signal(bool)
    RF = Signal(bool)
    Lucia = Signal(bool)
    DParsons = Signal(bool)

    def __init__(self):
        super().__init__()

        self.pixmap1 = QPixmap('images/KozenyCarmanButton.PNG')
        self.pixmap2 = QPixmap('images/TimurCoatesButton.PNG')
        self.pixmap3 = QPixmap('images/WinlandButton.PNG')
        self.pixmap4 = QPixmap('images/RQIFZIButton.PNG')
        self.pixmap5 = QPixmap('images/LuciaButton.PNG')
        self.pixmap6 = QPixmap('images/DykstraParsonsButton.PNG')

        self.action1 = QAction(self.pixmap1, 'Selecionar o método de Kozeny-Carman', self, statusTip="Método de Kozeny-Carman",
                               triggered=self.activateKC)
        self.action2 = QAction(self.pixmap2, 'Selecionar o método de Timur-Coates', self, statusTip="Método de Timur-Coates",
                               triggered=self.activateTC)
        self.action3 = QAction(self.pixmap3, 'Selecionar o método de Winland', self, statusTip="Regressões de Winland",
                               triggered=self.activateW)
        self.action4 = QAction(self.pixmap4, 'Selecionar a análise RQI-FZI', self, statusTip="Análise RQI-FZI",
                               triggered=self.activateRF)
        self.action5 = QAction(self.pixmap5, 'Selecionar a classificação de Lucia', self, statusTip="Classificação de Lucia",
                               triggered=self.activateL)
        self.action6 = QAction(self.pixmap6, 'Selecionar o método de Dykstra-Parsons', self, statusTip="Coeficiente de Dykstra-Parsons",
                               triggered=self.activateDP)

        self.addAction(self.action1)
        self.addAction(self.action2)
        self.addAction(self.action3)
        self.addAction(self.action4)
        self.addAction(self.action5)
        self.addAction(self.action6)
        self.setIconSize(QSize(150, 58))
        self.setStyleSheet('background-color: #2e3843')

    def activateKC(self):
        self.KCarman.emit(True)

    def activateTC(self):
        self.TCoates.emit(True)

    def activateW(self):
        self.Winland.emit(True)

    def activateRF(self):
        self.RF.emit(True)

    def activateL(self):
        self.Lucia.emit(True)

    def activateDP(self):
        self.DParsons.emit(True)

def test():
    app = QApplication(sys.argv)
    win = PetrophysicsTopBar()
    win.show()
    sys.exit(app.exec_())
