from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QApplication
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal

class HomePage(QWidget):
    changePage = Signal(bool)
    def __init__(self):
        super().__init__()

        self.logo = QPixmap(r'images/Graphic Design.png')
        self.start = QPushButton('Começar!')
        self.banner = QLabel()
        self.banner.setPixmap(self.logo)
        self.setStyleSheet('background-color: white')
        self.start.setStyleSheet('background-color: #5b7e65; color: white; font: bold 18px')
        self.buildlayout()
        self.connections()
        w = QApplication.desktop().width()
        h = QApplication.desktop().height()
        self.setMinimumSize(int(0.8*w), int(0.8*h))
        print(self.size())

    def buildlayout(self):
        layout = QGridLayout()
        layout.addWidget(self.banner, 0, 0, alignment=Qt.AlignHCenter)
        layout.addWidget(self.start, 1, 0)
        self.setLayout(layout)

    def connections(self):
        self.start.clicked.connect(lambda: self.changePage.emit(True))