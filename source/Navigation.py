from PySide2.QtWidgets import QWidget, QToolButton, QAction, QHBoxLayout, QApplication, QToolBar, QLabel, QSizePolicy
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Signal, QSize, Qt
from Header import Header
import sys


class Navigation(QToolBar):
    New = Signal(bool)
    Import = Signal(bool)
    Save = Signal(bool)
    PetroAnalysis = Signal(bool)
    StatsAnalysis = Signal(bool)
    About = Signal(bool)
    Help = Signal(bool)
    ViewPlot = Signal(bool)
    ViewSheet = Signal(bool)

    def __init__(self):
        super().__init__()

        self.header = Header()
        self.spacer = QWidget()
        self.lenep_label = QLabel()
        self.uenf_label = QLabel()

        self.pixmap1 = QPixmap('icons/novo.png')
        self.pixmap2 = QPixmap('icons/importar.png')
        self.pixmap3 = QPixmap('icons/salvar.png')
        self.pixmap4 = QPixmap('icons/analisepetro.png')
        self.pixmap5 = QPixmap('icons/analiseest.png')
        self.pixmap6 = QPixmap('icons/sobre.png')
        self.pixmap7 = QPixmap('icons/ajuda.png')
        self.pixmap8 = QPixmap('icons/plot.png')
        self.pixmap9 = QPixmap('icons/spreadsheet.png')
        self.pixmap10 = QPixmap('images/LENEPLogo.png')
        self.pixmap11 = QPixmap('images/UENFLogo3.png')

        a = "Novo"
        b = "Importar"
        c = "Salvar"
        d = "Análise Petrofísica"
        e = "Análise Estatística"
        f = "Sobre"
        g = "Ajuda"
        h = "Mostrar Gráfico"
        i = "Mostrar tabela"

        self.action1 = QAction(self.pixmap1, a, self, statusTip=a,
                               triggered=self.activateN)
        self.action2 = QAction(self.pixmap2, b, self, statusTip=b,
                               triggered=self.activateI)
        self.action3 = QAction(self.pixmap3, c, self, statusTip=c,
                               triggered=self.activateS)
        self.action4 = QAction(self.pixmap4, d, self, statusTip=d,
                               triggered=self.activateAP)
        self.action5 = QAction(self.pixmap5, e, self, statusTip=e,
                               triggered=self.activateAE)
        self.action6 = QAction(self.pixmap6, f, self, statusTip=f,
                               triggered=self.activateSb)
        self.action7 = QAction(self.pixmap7, g, self, statusTip=g,
                               triggered=self.activateA)
        self.action8 = QAction(self.pixmap8, h, self, statusTip=h,
                               triggered=self.activatePlot)
        self.action9 = QAction(self.pixmap9, i, self, statusTip=i,
                               triggered=self.activateSheet)

        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lenep_label.setPixmap(self.pixmap10)
        self.uenf_label.setPixmap(self.pixmap11)

        self.addWidget(self.header)
        self.addAction(self.action1)
        self.addAction(self.action2)
        self.addAction(self.action3)
        self.addAction(self.action4)
        self.addAction(self.action5)
        self.addAction(self.action6)
        self.addAction(self.action7)
        self.addAction(self.action8)
        self.addAction(self.action9)
        self.addWidget(self.spacer)
        self.setIconSize(QSize(70, 35))
        self.setStyleSheet("background-color: #2e3843")
        self.addWidget(self.uenf_label)
        #self.addWidget(self.lenep_label)

        self.w = self.widgetForAction(self.action1)
        self.default_state = self.w.styleSheet()

    def activateN(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action1)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.New.emit(True)

    def activateI(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action2)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.Import.emit(True)

    def activateS(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action3)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.Save.emit(True)

    def activateAP(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action4)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.PetroAnalysis.emit(True)

    def activateAE(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action5)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.StatsAnalysis.emit(True)

    def activateSb(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action6)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.About.emit(True)

    def activateA(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action7)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.Help.emit(True)

    def activatePlot(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action8)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.ViewPlot.emit(True)

    def activateSheet(self):
        self.w.setStyleSheet(self.default_state)
        self.w = self.widgetForAction(self.action9)
        self.default_state = self.w.styleSheet()
        self.w.setStyleSheet('background-color:green')
        self.ViewSheet.emit(True)

def test():
    app = QApplication(sys.argv)
    win = Navigation()
    win.show()
    sys.exit(app.exec_())