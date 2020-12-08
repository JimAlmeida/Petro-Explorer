from PySide2.QtWidgets import QWidget, QPushButton, QFormLayout, QLineEdit
from PySide2.QtCore import Signal
from Dropdown import Dropdown
import json as j


class PlotControls(QWidget):
    erasePlot = Signal(bool)

    def __init__(self):
        super().__init__()

        types_of_axes = ['Cartesiano', 'Logarítmico']
        types_of_traces = ['Scatter', "Boxplot"]

        self.modify_title = QLineEdit()
        self.modify_x_axis_type = Dropdown(types_of_axes)
        self.modify_y_axis_type = Dropdown(types_of_axes)
        self.modify_x_axis_label = QLineEdit()
        self.modify_y_axis_label = QLineEdit()
        self.modify_lower_x_range = QLineEdit()
        self.modify_upper_x_range = QLineEdit()
        self.modify_lower_y_range = QLineEdit()
        self.modify_upper_y_range = QLineEdit()
        self.type_of_trace = Dropdown(types_of_traces)
        self.add_x_trace = QLineEdit()
        self.add_y_trace = QLineEdit()
        self.trace_name = QLineEdit()
        self.run_button = QPushButton('Confirmar alterações')
        self.erase_button = QPushButton('Apagar gráfico')

        self.erase_button.clicked.connect(lambda: self.erasePlot.emit(True))
        self.type_of_trace.currentIndexChanged.connect(self.typeChanged)

        self.buildLayout()
        self.setStyleSheet('color:white; font-family: Bahnschrift SemiLight Condensed; font-size: 14px;')

        self.modify_title.setStyleSheet('background-color: white; color: black')
        self.modify_x_axis_type.setStyleSheet('background-color: white; color: black')
        self.modify_y_axis_type.setStyleSheet('background-color: white; color: black')
        self.modify_x_axis_label.setStyleSheet('background-color: white; color: black')
        self.modify_y_axis_label.setStyleSheet('background-color: white; color: black')
        self.modify_lower_x_range.setStyleSheet('background-color: white; color: black')
        self.modify_upper_x_range.setStyleSheet('background-color: white; color: black')
        self.modify_lower_y_range.setStyleSheet('background-color: white; color: black')
        self.modify_upper_y_range.setStyleSheet('background-color: white; color: black')
        self.type_of_trace.setStyleSheet('background-color: white; color: black')
        self.add_x_trace.setStyleSheet('background-color: white; color: black')
        self.add_y_trace.setStyleSheet('background-color: white; color: black')
        self.trace_name.setStyleSheet('background-color: white; color: black')
        self.run_button.setStyleSheet('background-color: white; color: black')
        self.erase_button.setStyleSheet('background-color: white; color: black')

    def buildLayout(self):
        layout = QFormLayout()
        layout.addRow('Título', self.modify_title)
        layout.addRow('Escala do eixo X', self.modify_x_axis_type)
        layout.addRow('Escala do eixo Y', self.modify_y_axis_type)
        layout.addRow('Rótulo do eixo X', self.modify_x_axis_label)
        layout.addRow('Rótulo do eixo Y', self.modify_y_axis_label)
        layout.addRow('Limite inferior do eixo X', self.modify_lower_x_range)
        layout.addRow('Limite superior do eixo X', self.modify_upper_x_range)
        layout.addRow('Limite inferior do eixo Y', self.modify_lower_y_range)
        layout.addRow('Limite superior do eixo Y', self.modify_upper_y_range)
        layout.addRow('Tipo de série', self.type_of_trace)
        layout.addRow('Adicionar série/box no gráfico (eixo x)', self.add_x_trace)
        layout.addRow('Adicionar série/box no gráfico (eixo y)', self.add_y_trace)
        layout.addRow('Nome da série', self.trace_name)
        layout.addWidget(self.run_button)
        layout.addWidget(self.erase_button)
        self.setLayout(layout)

    def fillFromJson(self, _json):
        # json is the standard json export from the plotly library
        assert (isinstance(_json, str))

        j_obj = j.loads(_json)
        
        try:
            if 'title' in list(j_obj['layout'].keys()):
                self.modify_title.setText(str(j_obj['layout']['title']['text']))
    
            if 'type' in list(j_obj['layout']['xaxis'].keys()):
                if j_obj['layout']['xaxis']['type'].lower() == 'log':
                    self.modify_x_axis_type.setCurrentIndex(1)
                else:
                    self.modify_y_axis_type.setCurrentIndex(0)
                    
            if 'type' in list(j_obj['layout']['yaxis'].keys()):
                if j_obj['layout']['yaxis']['type'].lower() == 'log':
                    self.modify_y_axis_type.setCurrentIndex(1)
                else:
                    self.modify_y_axis_type.setCurrentIndex(0)
    
            if 'title' in list(j_obj['layout']['xaxis'].keys()):
                self.modify_x_axis_label.setText(str(j_obj['layout']['xaxis']['title']['text']))
            if 'title' in list(j_obj['layout']['yaxis'].keys()):
                self.modify_y_axis_label.setText(str(j_obj['layout']['yaxis']['title']['text']))
            if 'range' in list(j_obj['layout']['xaxis'].keys()):
                self.modify_lower_x_range.setText(str(j_obj['layout']['xaxis']['range'][0]))
                self.modify_upper_x_range.setText(str(j_obj['layout']['xaxis']['range'][1]))
            if 'range' in list(j_obj['layout']['yaxis'].keys()):
                self.modify_lower_y_range.setText(str(j_obj['layout']['yaxis']['range'][0]))
                self.modify_upper_y_range.setText(str(j_obj['layout']['yaxis']['range'][1]))
        except KeyError:
            if 'title' in list(j_obj['layout']['template']['layout'].keys()):
                self.modify_title.setText(str(j_obj['layout']['template']['layout']['title']['text']))

            if 'type' in list(j_obj['layout']['template']['layout']['xaxis'].keys()):
                if j_obj['layout']['template']['layout']['xaxis']['type'].lower() == 'log':
                    self.modify_x_axis_type.setCurrentIndex(1)
                else:
                    self.modify_y_axis_type.setCurrentIndex(0)

            if 'type' in list(j_obj['layout']['template']['layout']['yaxis'].keys()):
                if j_obj['layout']['template']['layout']['yaxis']['type'].lower() == 'log':
                    self.modify_y_axis_type.setCurrentIndex(1)
                else:
                    self.modify_y_axis_type.setCurrentIndex(0)

            if 'title' in list(j_obj['layout']['template']['layout']['xaxis'].keys()):
                self.modify_x_axis_label.setText(str(j_obj['layout']['template']['layout']['xaxis']['title']['text']))
            if 'title' in list(j_obj['layout']['template']['layout']['yaxis'].keys()):
                self.modify_y_axis_label.setText(str(j_obj['layout']['template']['layout']['yaxis']['title']['text']))
            if 'range' in list(j_obj['layout']['template']['layout']['xaxis'].keys()):
                self.modify_lower_x_range.setText(str(j_obj['layout']['template']['layout']['xaxis']['range'][0]))
                self.modify_upper_x_range.setText(str(j_obj['layout']['template']['layout']['xaxis']['range'][1]))
            if 'range' in list(j_obj['layout']['template']['layout']['yaxis'].keys()):
                self.modify_lower_y_range.setText(str(j_obj['layout']['template']['layout']['yaxis']['range'][0]))
                self.modify_upper_y_range.setText(str(j_obj['layout']['template']['layout']['yaxis']['range'][1]))

        return

    def typeChanged(self, ind):
        currentType = self.type_of_trace.currentText()
        if currentType == "Boxplot":
            self.add_y_trace.setDisabled(True)
            self.add_y_trace.setStyleSheet('background-color: grey; color: black')
        else:
            self.add_y_trace.setEnabled(True)
            self.add_y_trace.setStyleSheet('background-color: white; color: black')

