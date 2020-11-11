from PySide2.QtWidgets import QComboBox

class Dropdown(QComboBox):
    def __init__(self, content):
        super().__init__()
        for c in content:
            self.addItem(str(c))