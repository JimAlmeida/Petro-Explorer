from PySide2.QtWidgets import QMainWindow, QStackedLayout, QWidget, QDockWidget, QVBoxLayout, QApplication, QSizePolicy, \
    QScrollArea, QFileDialog, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from HomePage import HomePage
from MainWindow import MainWindow
import sys


class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.hm_page = HomePage()
        self.mn_window = MainWindow()
        self.widget_layout = QStackedLayout()

        self.buildLayout()
        self.connections()

        #self.setStyleSheet('background-color: white')
        #self.hm_page.setStyleSheet('background-color: #2e3843')

    def buildLayout(self):
        self.widget_layout = QStackedLayout()
        self.widget_layout.addWidget(self.hm_page)
        self.widget_layout.addWidget(self.mn_window)
        self.setLayout(self.widget_layout)

    def connections(self):
        self.hm_page.changePage.connect(lambda: self.widget_layout.setCurrentIndex(1))
        self.mn_window.changePage.connect(lambda: self.widget_layout.setCurrentIndex(0))


def test():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = ApplicationWindow()
    win.showMaximized()
    sys.exit(app.exec_())

test()