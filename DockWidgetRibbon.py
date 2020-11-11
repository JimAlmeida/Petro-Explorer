from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QFont


class DockWidgetRibbon(QLabel):
    def __init__(self, description):
        super().__init__()

        self._font = QFont('Bahnschrift SemiLight Condensed', 13)

        self.setText(description)

        self.setFont(self._font)

        self.setStyleSheet('background-color: #5c686e; color: white;')