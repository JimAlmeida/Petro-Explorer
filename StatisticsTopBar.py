from PySide2.QtWidgets import QWidget, QToolButton, QAction, QHBoxLayout, QApplication, QToolBar
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Signal, QSize, Qt
import sys


class StatisticsTopBar(QToolBar):
    Regr = Signal(bool)
    StatDesc = Signal(bool)
    Hist = Signal(bool)
    Boxplt = Signal(bool)

    def __init__(self):
        super().__init__()

        self.pixmap1 = QPixmap('images/RegressoesButton.PNG')
        self.pixmap2 = QPixmap('images/EstatisticaButton.PNG')
        self.pixmap3 = QPixmap('images/HistogramaButton.PNG')
        self.pixmap4 = QPixmap('images/BoxplotButton.PNG')

        self.action1 = QAction(self.pixmap1, 'Selecionar o módulo de Regressões', self, statusTip="Módulo de Regressões",
                               triggered=self.activateRG)
        self.action2 = QAction(self.pixmap2, 'Selecionar o módulo de Estatística Descritiva', self, statusTip="Módulo de Estatística Descritiva",
                               triggered=self.activateED)
        self.action3 = QAction(self.pixmap3, 'Selecionar o módulo para criação de Histogramas', self, statusTip="Módulo para criação de Histogramas",
                               triggered=self.activateHG)
        self.action4 = QAction(self.pixmap4, 'Selecionar o módulo para criação de Boxplots', self, statusTip="Módulo para criação de Boxplots",
                               triggered=self.activateBP)

        self.addAction(self.action1)
        self.addAction(self.action2)
        self.addAction(self.action3)
        self.addAction(self.action4)
        self.setIconSize(QSize(150, 58))

    def activateRG(self):
        self.Regr.emit(True)

    def activateED(self):
        self.StatDesc.emit(True)

    def activateHG(self):
        self.Hist.emit(True)

    def activateBP(self):
        self.Boxplt.emit(True)


def test():
    app = QApplication(sys.argv)
    win = StatisticsTopBar()
    win.show()
    sys.exit(app.exec_())
