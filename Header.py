from PySide2.QtWidgets import QWidget, QToolButton, QAction, QHBoxLayout, QApplication, QToolBar, QLabel, QGridLayout
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Signal, QSize, Qt


class Header(QWidget):
    HomePage = Signal(bool)
    def __init__(self):
        super().__init__()

        self.pixmap1 = QPixmap('images/LogoHorizontal.PNG')

        self.action1 = QAction(self.pixmap1, 'Home', self,
                               statusTip="Home",
                               triggered=self.loadHomePage)

        self.tbutton1 = QToolButton()
        self.tbutton1.setDefaultAction(self.action1)
        self.tbutton1.setIconSize(QSize(193, 52))
        self.tbutton1.setStyleSheet('border:none')

        self.label2 = QLabel('LENEP-UENF')
        self.label2.setFont('Bahnschrift Condensed')
        self.label2.setStyleSheet('color: white; font-size: 24px;')

        layout = QGridLayout()
        layout.addWidget(self.tbutton1, 0, 0, alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.setStyleSheet('background-color: #2e3843')

    def loadHomePage(self):
        print('HEADER ACTIVATED')
        self.HomePage.emit(True)