from PySide2.QtWidgets import QAction, QTableWidget, QApplication, QAbstractItemView, QTableView, QWidget, QToolButton, QGridLayout
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize, Signal
from PySide2 import QtGui
import numpy as np
import pandas as pd
import string

def num_to_excel_col(n):
    if n < 1:
        raise ValueError("Number must be positive")
    result = ""
    while True:
        if n > 26:
            n, r = divmod(n - 1, 26)
            result = chr(r + ord('A')) + result
        else:
            return chr(n + ord('A') - 1) + result


class CopySelectedCellsAction(QAction):
    def __init__(self, table_widget: QTableWidget):
        super(CopySelectedCellsAction, self).__init__("Copy", table_widget)
        self.setShortcut('Ctrl+C')
        self.triggered.connect(self.copy_cells_to_clipboard)
        self.table_widget = table_widget

    def copy_cells_to_clipboard(self):
        if len(self.table_widget.selectionModel().selectedIndexes()) > 0:
            t = [(index.row(), index.column()) for index in self.table_widget.selectionModel().selectedIndexes()]
            t.sort()

            lastRow = t[0][0]
            lastColumn = t[0][1]

            # add rows and columns to clipboard
            clipboard = ""

            for i in range(len(t)):
                if t[i][0] == lastRow:
                    clipboard += str(self.table_widget.model.input_data[t[i][0]][t[i][1]]).strip('\n\t')
                    clipboard += '\t'
                else:
                    lastRow = t[i][0]
                    clipboard = clipboard.rstrip('\t')

                    clipboard += '\n'
                    clipboard += str(self.table_widget.model.input_data[t[i][0]][t[i][1]])
                    clipboard += '\t'

            # copy to the system clipboard
            clipboard = clipboard.rstrip('\t')
            sys_clip = QApplication.clipboard()
            sys_clip.setText(clipboard)


class PasteFromClipboard(QAction):
    def __init__(self, table_widget: QTableWidget):
        super(PasteFromClipboard, self).__init__("Paste", table_widget)
        self.setShortcut('Ctrl+V')
        self.triggered.connect(self.paste_to_cells)
        self.table_widget = table_widget

    def paste_to_cells(self):
        clipboard = QApplication.clipboard().text()
        row_start = self.table_widget.selectionModel().selectedIndexes()[0].row()
        column_start = self.table_widget.selectionModel().selectedIndexes()[0].column()

        t = ''
        row = row_start
        column = column_start

        for c in clipboard:
            if c == '\t':
                self.table_widget.model.input_data[row][column] = t
                self.table_widget.model.dataChanged.emit(row, column)
                column += 1
                t = ''
            elif c == '\n':
                self.table_widget.model.input_data[row][column] = t
                self.table_widget.model.dataChanged.emit(row, column)
                row += 1
                column -= (column-column_start)
                t = ''
            else:
                t = t + c
        self.table_widget.model.input_data[row][column] = t
        self.table_widget.model.dataChanged.emit(row, column)
        return


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, header=None):
        QAbstractTableModel.__init__(self)
        self.mapping = {}
        self.input_data = np.array(data)
        shape = np.shape(self.input_data)
        if shape == (0,):
            self.row_count = 0
            self.column_count = 0
        else:
            self.row_count, self.column_count = np.shape(self.input_data)
        self.header_info = [num_to_excel_col(i + 1) for i in range(self.column_count)]

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.header_info[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row_column = tuple([index.row(), index.column()])
            return str(self.input_data.item(row_column))
        elif role == Qt.BackgroundRole:
            return QtGui.QBrush(QtGui.Qt.white)
        else:
            return None

    def setData(self, index, value=0, role=Qt.EditRole, flag=False):
        if index.isValid() and role == Qt.EditRole:
            if self.input_data[index.row()][index.column()] != value:
                self.input_data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
            return True
        if index.isValid() and role == Qt.BackgroundRole:
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable


class Spreadsheet(QTableView):
    def __init__(self):
        super().__init__()
        self.setWordWrap(True)
        self.resizeRowsToContents()
        self.copy_action = CopySelectedCellsAction(self)
        self.paste_action = PasteFromClipboard(self)
        self.addAction(self.copy_action)
        self.addAction(self.paste_action)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.model = CustomTableModel([])

    def changeModel(self, data, header):
        self.model = CustomTableModel(data, header)
        self.setModel(self.model)

    def addBlankSheet(self):
        new_model = pd.DataFrame(index=[1,2,3,4,5,6,7,8,9,10], columns=[1,2,3,4,5,6,7,8,9,10]).fillna('')
        self.changeModel(new_model, None)

    def addColumn(self, array=None):
        if array is None:
            array = []
            for i in range(self.model.rowCount()):
                array.append('')
        model = self.retrieveModel()
        print(model.shape)
        column_name = num_to_excel_col(model.shape[1]+1)
        model[column_name] = pd.Series(array)
        self.changeModel(model, list(model.keys()))

    def addRow(self, array=None):
        model = self.retrieveModel()
        columns = list(model.keys())
        if array is None:
            array = []
            c = ''
            for i in range(len(columns)):
                array.append(c)
        new_row = pd.Series(array, index=columns)
        model = model.append(new_row, ignore_index=True)
        self.changeModel(model, columns)

    def deleteColumn(self):
        df = self.retrieveModel()
        df = df.drop(columns=self.model.header_info[self.currentIndex().column()])
        self.changeModel(df, None)

    def deleteRow(self):
        df = self.retrieveModel()
        df = df.drop(index=self.currentIndex().row())
        self.changeModel(df, None)

    def retrieveModel(self):
        if len(self.model.input_data) > 0:
            return pd.DataFrame(self.model.input_data, columns=self.model.header_info)
        else:
            return None


class SpreadsheetControls(QWidget):
    AddRow = Signal(bool)
    AddColumn = Signal(bool)
    DeleteRow = Signal(bool)
    DeleteColumn = Signal(bool)

    def __init__(self):
        super().__init__()

        self.add_row_button = QToolButton()
        self.add_column_button = QToolButton()
        self.delete_row_button = QToolButton()
        self.delete_column_button = QToolButton()

        self.pixmap1 = QtGui.QPixmap('icons/addRow.png')
        self.pixmap2 = QtGui.QPixmap('icons/addColumn.PNG')
        self.pixmap3 = QtGui.QPixmap('icons/deleteRow.PNG')
        self.pixmap4 = QtGui.QPixmap('icons/deleteColumn.PNG')

        self.action1 = QAction(self.pixmap1, 'Adicionar linhas', self, statusTip='Adicionar linhas',
                               triggered=self.addRow)

        self.action2 = QAction(self.pixmap2, 'Adicionar colunas', self, statusTip='Adicionar colunas',
                               triggered=self.addColumn)

        self.action3 = QAction(self.pixmap3, 'Deletar linhas', self, statusTip='Deletar linhas',
                               triggered=self.deleteRow)

        self.action4 = QAction(self.pixmap4, 'Deletar colunas', self, statusTip='Deletar colunas',
                               triggered=self.deleteColumn)

        self.add_row_button.setDefaultAction(self.action1)
        self.add_column_button.setDefaultAction(self.action2)
        self.delete_row_button.setDefaultAction(self.action3)
        self.delete_column_button.setDefaultAction(self.action4)

        w = 75
        h = 84
        self.add_column_button.setIconSize(QSize(w, h))
        self.add_row_button.setIconSize(QSize(w, h))
        self.delete_row_button.setIconSize(QSize(w, h))
        self.delete_column_button.setIconSize(QSize(w, h))

        self.buildLayout()

    def addRow(self):
        self.AddRow.emit(True)

    def addColumn(self):
        self.AddColumn.emit(True)

    def deleteRow(self):
        self.DeleteRow.emit(True)

    def deleteColumn(self):
        self.DeleteColumn.emit(True)

    def buildLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.add_row_button, 0, 0)
        layout.addWidget(self.add_column_button, 0, 1)
        layout.addWidget(self.delete_row_button, 0, 2)
        layout.addWidget(self.delete_column_button, 0, 3)
        self.setLayout(layout)

