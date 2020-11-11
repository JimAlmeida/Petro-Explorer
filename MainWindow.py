from DataVisualization import DataVisualization
from HomePage import HomePage
from Header import Header
from Navigation import Navigation
from PetrophysicsTopBar import PetrophysicsTopBar
from PetrophysicsOptions import PetrophysicsOptions
from PlotViewer import PlotViewer
from Spreadsheet import Spreadsheet, SpreadsheetControls
from StatisticsOptions import StatisticsOptions
from StatisticsTopBar import StatisticsTopBar
from PySide2.QtWidgets import QMainWindow, QStackedLayout, QWidget, QDockWidget, QVBoxLayout, QApplication, QSizePolicy, \
    QScrollArea, QFileDialog, QMessageBox, QLabel, QStatusBar
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QIcon
import Data
import sys
from HandlerThread import HandlerThread
from Regressions import regressionManifold
from Statistics import statisticsManifold
from Boxplot import boxplotManifold
from Histogram import histogramManifold
from DockWidgetRibbon import DockWidgetRibbon
from KozenyCarman import kCarmanManifold
from Lucia import luciaManifold
from FlowZones import fzManifold
from Winland import winlandManifold
from DykstraParsons import dParsonsManifold
from TimurCoates import tCoatesManifold
from PlotControls import PlotControls
from PlotControleEngine import pceManifold


class MainWindow(QMainWindow):
    changePage = Signal(bool)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Petro-Explorer v1.0')
        win_icon = QIcon('icons/Logo.ico')
        self.setWindowIcon(win_icon)
        self.setStyleSheet('background-color: #363f49;')

        self.header = Header()
        self.navigation = Navigation()
        self.p_top_bar = PetrophysicsTopBar()
        self.s_top_bar = StatisticsTopBar()
        self.p_options_1 = PetrophysicsOptions(_mode='KCarman')
        self.p_options_2 = PetrophysicsOptions(_mode='TCoates')
        self.p_options_3 = PetrophysicsOptions(_mode='Winland')
        self.p_options_4 = PetrophysicsOptions(_mode='RQIFZI')
        self.p_options_5 = PetrophysicsOptions(_mode='Lucia')
        self.p_options_6 = PetrophysicsOptions(_mode='DParsons')
        self.s_options_1 = StatisticsOptions(_mode='Regression')
        self.s_options_2 = StatisticsOptions(_mode='Statistics')
        self.s_options_3 = StatisticsOptions(_mode='Histogram')
        self.s_options_4 = StatisticsOptions(_mode='Boxplot')
        self.sp_controls = SpreadsheetControls()
        self.plot_controls = PlotControls()
        self.plot_viewer = PlotViewer()
        self.spreadsheet = Spreadsheet()
        self.status_bar = QStatusBar()

        self.scroll_area_1 = QScrollArea()
        self.scroll_area_1.setWidget(self.spreadsheet)
        self.scroll_area_1.setWidgetResizable(True)

        self.scroll_area_2 = QScrollArea()
        self.scroll_area_2.setWidget(self.plot_viewer)
        self.scroll_area_2.setWidgetResizable(True)

        self.bar_widget = QWidget()
        self.bar_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.central_widget = QWidget()
        self.options_widget = QWidget()

        self.docking_options = QDockWidget()
        self.docking_options.setWidget(self.options_widget)
        self.docking_options.setTitleBarWidget(DockWidgetRibbon(' Opções de cálculo'))

        self.docking_options2 = QDockWidget()
        self.docking_options2.setWidget(self.sp_controls)
        self.docking_options2.setTitleBarWidget(DockWidgetRibbon(' Controles de visualização'))

        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)
        self.addToolBar(self.navigation)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.docking_options)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.docking_options2)
        self.connections()
        self.buildLayout()

        self.centralWidget().setStyleSheet('background-color: #2e3843')
        self.spreadsheet.setStyleSheet('background-color: white')
        self.status_bar.setStyleSheet('color: white')

    def buildLayout(self):
        stacked_layout_1 = QStackedLayout()
        # stacked_layout_1.addWidget(QWidget())
        stacked_layout_1.addWidget(self.p_top_bar)
        stacked_layout_1.addWidget(self.s_top_bar)

        stacked_layout_2 = QStackedLayout()
        # stacked_layout_2.addWidget(QWidget())
        stacked_layout_2.addWidget(self.p_options_1)
        stacked_layout_2.addWidget(self.p_options_2)
        stacked_layout_2.addWidget(self.p_options_3)
        stacked_layout_2.addWidget(self.p_options_4)
        stacked_layout_2.addWidget(self.p_options_5)
        stacked_layout_2.addWidget(self.p_options_6)
        stacked_layout_2.addWidget(self.s_options_1)
        stacked_layout_2.addWidget(self.s_options_2)
        stacked_layout_2.addWidget(self.s_options_3)
        stacked_layout_2.addWidget(self.s_options_4)

        self.stacked_layout_3 = QStackedLayout()
        self.stacked_layout_3.addWidget(self.scroll_area_1)
        self.stacked_layout_3.addWidget(self.scroll_area_2)

        central_widget_layout = QVBoxLayout()
        central_widget_layout.addWidget(self.bar_widget)
        central_widget_layout.addLayout(self.stacked_layout_3)

        self.central_widget.setLayout(central_widget_layout)
        self.bar_widget.setLayout(stacked_layout_1)
        self.options_widget.setLayout(stacked_layout_2)

    def connections(self):
        self.navigation.PetroAnalysis.connect(lambda: self.bar_widget.layout().setCurrentIndex(0))
        self.navigation.StatsAnalysis.connect(lambda: self.bar_widget.layout().setCurrentIndex(1))
        self.navigation.Save.connect(lambda: self.saveDialog())
        self.navigation.Import.connect(lambda: self.importDialog())
        self.navigation.About.connect(lambda: self.aboutDialog())
        self.navigation.Help.connect(lambda: self.helpDialog())
        self.navigation.header.HomePage.connect(lambda: self.changePage.emit(True))
        self.navigation.ViewSheet.connect(lambda: self.displaySheet())
        self.navigation.ViewPlot.connect(lambda: self.displayPltE())
        self.navigation.New.connect(lambda: self.spreadsheet.addBlankSheet())

        self.p_top_bar.KCarman.connect(lambda: self.options_widget.layout().setCurrentIndex(0))
        self.p_top_bar.TCoates.connect(lambda: self.options_widget.layout().setCurrentIndex(1))
        self.p_top_bar.Winland.connect(lambda: self.options_widget.layout().setCurrentIndex(2))
        self.p_top_bar.DParsons.connect(lambda: self.options_widget.layout().setCurrentIndex(5))
        self.p_top_bar.Lucia.connect(lambda: self.options_widget.layout().setCurrentIndex(4))
        self.p_top_bar.RF.connect(lambda: self.options_widget.layout().setCurrentIndex(3))

        self.s_top_bar.Regr.connect(lambda: self.options_widget.layout().setCurrentIndex(6))
        self.s_top_bar.StatDesc.connect(lambda: self.options_widget.layout().setCurrentIndex(7))
        self.s_top_bar.Boxplt.connect(lambda: self.options_widget.layout().setCurrentIndex(9))
        self.s_top_bar.Hist.connect(lambda: self.options_widget.layout().setCurrentIndex(8))

        self.s_options_1.run_button.clicked.connect(self.startRegr)
        self.s_options_2.run_button.clicked.connect(self.startStat)
        self.s_options_3.run_button.clicked.connect(self.startHist)
        self.s_options_4.run_button.clicked.connect(self.startBxpl)

        self.p_options_1.run.clicked.connect(self.startKCoz)
        self.p_options_2.run.clicked.connect(self.startTCoa)
        self.p_options_3.run.clicked.connect(self.startWinl)
        self.p_options_4.run.clicked.connect(self.startFZIR)
        self.p_options_5.run.clicked.connect(self.startLuci)
        self.p_options_6.run.clicked.connect(self.startDyks)

        self.sp_controls.AddColumn.connect(lambda: self.spreadsheet.addColumn())
        self.sp_controls.AddRow.connect(lambda: self.spreadsheet.addRow())
        self.sp_controls.DeleteRow.connect(lambda: self.spreadsheet.deleteRow())
        self.sp_controls.DeleteColumn.connect(lambda: self.spreadsheet.deleteColumn())

        self.plot_controls.run_button.clicked.connect(lambda: self.startPltE())
        self.plot_controls.erasePlot.connect(lambda: self.plot_viewer.erasePlot())

        self.plot_viewer.feedPlotControls.connect(self.plot_controls.fillFromJson)

    def startPltE(self):
        old_json = self.plot_viewer.json_data
        title = self.plot_controls.modify_title.text()
        xtype = self.plot_controls.modify_x_axis_type.currentText()
        ytype = self.plot_controls.modify_y_axis_type.currentText()
        xlabel = self.plot_controls.modify_x_axis_label.text()
        ylabel = self.plot_controls.modify_y_axis_label.text()

        if len(self.plot_controls.modify_lower_x_range.text()) > 0:
            lxrange = float(self.plot_controls.modify_lower_x_range.text())
        else:
            lxrange = None
        if len(self.plot_controls.modify_upper_x_range.text()) > 0:
            uxrange = float(self.plot_controls.modify_upper_x_range.text())
        else:
            uxrange = None
        if len(self.plot_controls.modify_lower_y_range.text()) > 0:
            lyrange = float(self.plot_controls.modify_lower_y_range.text())
        else:
            lyrange = None
        if len(self.plot_controls.modify_upper_y_range.text()) > 0:
            uyrange = float(self.plot_controls.modify_upper_y_range.text())
        else:
            uyrange = None

        if len(self.plot_controls.add_x_trace.text()) > 0 and len(self.plot_controls.add_y_trace.text()):
            trace_type = self.plot_controls.type_of_trace.currentText()
            x_trace = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.plot_controls.add_x_trace.text())]
            y_trace = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.plot_controls.add_y_trace.text())]
            trace_name = self.plot_controls.trace_name.text()
        else:
            trace_type = None
            x_trace = None
            y_trace = None
            trace_name = None
        
        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.loadPltE(io_operations_handler.results))
        io_operations_handler.loadParameters(f=pceManifold, _args=[old_json, title, xtype, ytype, xlabel, ylabel, lxrange, uxrange, lyrange, uyrange, trace_type, x_trace, y_trace, trace_name])
        io_operations_handler.start()

    def loadPltE(self, results, typ='Regressão'):
        self.plot_viewer.loadPlot(results[0], results[1], _type=typ)
        self.displayPltE()

    def displayPltE(self):
        self.stacked_layout_3.setCurrentIndex(1)
        self.docking_options2.setWidget(self.plot_controls)
        #self.removeDockWidget(self.docking_options3)
        #self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.docking_options2)

    def loadSheet(self, df):
        self.spreadsheet.changeModel(data=df, header=list(df.keys()))
        self.displaySheet()

    def displaySheet(self):
        self.stacked_layout_3.setCurrentIndex(0)
        self.docking_options2.setWidget(self.sp_controls)
        self.status_bar.clearMessage()
        #self.removeDockWidget(self.docking_options2)
        #self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.docking_options3)

    def importDialog(self):
        func = None
        file_settings = QFileDialog().getOpenFileName(self, 'Importar Arquivo',
                                                      filter="Todos os arquivos (*);; Arquivo de Texto (*.txt);; Arquivo CSV (*.csv);; "
                                                             "Planilha Excel (*.xlsx)")
        if ".txt" in file_settings[0]:
            func = Data.readTXT
        if ".csv" in file_settings[0]:
            func = Data.readCSV
        if ".xlsx" in file_settings[0]:
            func = Data.readExcel

        self.status_bar.showMessage('Importando arquivo. Aguarde.')
        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.loadSheet(io_operations_handler.results))
        io_operations_handler.loadParameters(f=func, _args=[file_settings[0],])
        io_operations_handler.start()

    def saveDialog(self):
        func = None
        file_settings = QFileDialog().getSaveFileName(self, "Salvar Arquivo",
                                                      filter="Arquivo de Texto (*.txt);; Arquivo CSV (*.csv);; "
                                                             "Planilha Excel (*.xlsx)")
        if ".txt" in file_settings[0]:
            func = Data.toTXT
        if ".csv" in file_settings[0]:
            func = Data.toCSV
        if ".xlsx" in file_settings[0]:
            func = Data.toExcel

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.loadParameters(f=func, _args=[self.spreadsheet.retrieveModel(), file_settings[0]])
        io_operations_handler.start()

    def aboutDialog(self):
        icon = QIcon(r'icons/sobre.png')
        text = "O Petro-Explorer é um software desenvolvido no Laboratório de Exploração e Produção de Petróleo (" \
               "LENEP) da UENF para análises petrofísicas e estatísticas de dados de rocha. "
        msg = QMessageBox()
        msg.setWindowTitle('Sobre Petro-Explorer')
        msg.setWindowIcon(icon)
        msg.setText(text)
        msg.exec_()

    def helpDialog(self):
        icon = QIcon(r'icons/ajuda.png')
        text = r"Para utilizar o Petro-Explorer de maneira correta siga os seguintes passos:" \
               "\n1 - Clique no botão Novo na barra de navegação, isto irá limpar quaisquer dados de antigas análises.\n" \
               "2 - Para começar a sua análise é preciso importar os dados, assim, clique no botão Importar para escolher o seu arquivo. Atente para o fato que somente três tipos de arquivo são suportados (i.e. *.txt, *.csv, *.xlsx). Depois da sua escolha, os dados devem aparecer na planilha do software.\n" \
               "3 - Se você desejar realizar uma análise petrofísica, clique no botão de Análise Petrofísica na barra de navegação. Caso queira realizar uma análise estatística, clique no botão de Análise Estatística na barra de navegação.\n" \
               "4 - Selecione na barra superior à planilha, a análise que desejas realizar sobre seus dados.\n" \
               "5 - No canto direito da janela, selecione os parâmetros de sua análise assim como o destino de seus resultados. Clique no botão 'Começar Análise' para continuar.\n" \
               "6 - Analise seus resultados na planilha, e, quando disponível, no gráfico também.\n" \
               "7 - Quando terminar, clique no botão Salvar para salvar os resultados de suas análises no disco.\n" \
               "8 - Caso queira realizar outra análise, clique no botão \"Novo\" e comece novamente.\n"
        msg = QMessageBox()
        msg.setWindowTitle('Ajuda')
        msg.setWindowIcon(icon)
        msg.setText(text)
        msg.exec_()

    def startRegr(self):
        xdata = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.s_options_1.payload['x_column'])]
        ydata = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.s_options_1.payload['y_column'])]
        _type = self.s_options_1.payload['calculate']
        dgr = self.s_options_1.degree.value()

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayRegr(self.s_options_1.payload['output_column'], io_operations_handler.results))
        io_operations_handler.loadParameters(f=regressionManifold, _args=[xdata, ydata, dgr, _type])
        io_operations_handler.start()

    def startStat(self):
        xdata = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.s_options_2.payload['x_column'])]
        mthd = self.s_options_2.payload['calculate']
        qtl = self.s_options_2.quartile.value()
        pctl = self.s_options_2.percentile.value()

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayStat(self.s_options_2.payload['output_column'], io_operations_handler.results))
        io_operations_handler.loadParameters(f=statisticsManifold, _args=[xdata, mthd, qtl, pctl])
        io_operations_handler.start()

    def startHist(self):
        xdata = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.s_options_3.payload['x_column'])]
        nbins = self.s_options_3.payload['y_column']

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayHist(io_operations_handler.results))
        io_operations_handler.loadParameters(f=histogramManifold, _args=[xdata, nbins])
        io_operations_handler.start()

    def startBxpl(self):
        indexes = []
        columns = self.s_options_4.payload['column_range']
        for col in columns:
            indexes.append(self.spreadsheet.model.header_info.index(col))
        xdata = self.spreadsheet.model.input_data[:, indexes]
        box_orientation = self.s_options_4.payload['y_column']

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayBxpl(io_operations_handler.results))
        io_operations_handler.loadParameters(f=boxplotManifold, _args=[xdata, box_orientation])
        io_operations_handler.start()

    def startKCoz(self):
        #you need to ascertain if x corresponds to Permeability, y to Porosity and z to Swir/Svgr

        k = None
        phi = None
        svgr = None

        prp = self.p_options_1.payload['calculate']

        if prp == 'Permeabilidade (mD)':
            phi = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.p_options_1.payload['x_column'])]
            svgr = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.p_options_1.payload['y_column'])]
        elif prp == 'SVgr (cm-1)':
            k = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.p_options_1.payload['x_column'])]
            phi = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.p_options_1.payload['y_column'])]
        else:
            k = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.p_options_1.payload['x_column'])]
            phi = self.spreadsheet.model.input_data[:, self.spreadsheet.model.header_info.index(self.p_options_1.payload['y_column'])]

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayKCoz(io_operations_handler.results))
        io_operations_handler.loadParameters(f=kCarmanManifold, _args=[k, phi, svgr, prp])
        io_operations_handler.start()

    def startTCoa(self):
        #you need to ascertain if x corresponds to Permeability, y to Porosity and z to Swir/Svgr
        if self.p_options_2.payload['x_column'] != '':
            xdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_2.payload['x_column'])]
        else:
            xdata = []
        if self.p_options_2.payload['y_column'] != '':
            ydata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_2.payload['y_column'])]
        else:
            ydata = []
        if self.p_options_2.payload['z_column'] != '':
            zdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_2.payload['z_column'])]
        else:
            zdata = []
        prp = self.p_options_2.payload['calculate']

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayTCoa(io_operations_handler.results))
        io_operations_handler.loadParameters(f=tCoatesManifold, _args=[xdata, ydata, zdata, prp])
        io_operations_handler.start()

    def startWinl(self):
        #you need to ascertain if x corresponds to Permeability, y to Porosity and z to Swir/Svgr
        if self.p_options_3.payload['x_column'] != '':
            xdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_3.payload['x_column'])]
        else:
            xdata = []
        if self.p_options_3.payload['y_column'] != '':
            ydata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_3.payload['y_column'])]
        else:
            ydata = []

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayWinl(io_operations_handler.results))
        io_operations_handler.loadParameters(f=winlandManifold, _args=[xdata, ydata])
        io_operations_handler.start()

    def startFZIR(self):
        # you need to ascertain if x corresponds to Permeability, y to Porosity and z to Swir/Svgr
        if self.p_options_4.payload['x_column'] != '':
            xdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_4.payload['x_column'])]
        else:
            xdata = None
        if self.p_options_4.payload['y_column'] != '':
            ydata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_4.payload['y_column'])]
        else:
            ydata = None
        if self.p_options_4.payload['z_column'] != '':
            zdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_4.payload['z_column'])]
        else:
            zdata = None

        prp = self.p_options_4.payload['calculate']
        un = self.p_options_4.payload['column_range']

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayFZIR(io_operations_handler.results))
        io_operations_handler.loadParameters(f=fzManifold, _args=[xdata, ydata, zdata, un, prp])
        io_operations_handler.start()

    def startLuci(self):
        #you need to ascertain if x corresponds to Permeability, y to Porosity and z to Swir/Svgr
        if self.p_options_5.payload['x_column'] != '':
            xdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_5.payload['x_column'])]
        else:
            xdata = []
        if self.p_options_5.payload['y_column'] != '':
            ydata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_5.payload['y_column'])]
        else:
            ydata = []

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayLuci(io_operations_handler.results))
        io_operations_handler.loadParameters(f=luciaManifold, _args=[xdata, ydata])
        io_operations_handler.start()

    def startDyks(self):
        #you need to ascertain if x corresponds to Permeability, y to Porosity and z to Swir/Svgr
        if self.p_options_6.payload['x_column'] != '':
            xdata = self.spreadsheet.model.input_data[:,
                    self.spreadsheet.model.header_info.index(self.p_options_6.payload['x_column'])]
        else:
            xdata = []
        prp = self.p_options_6.payload['calculate']

        io_operations_handler = HandlerThread()
        io_operations_handler.messageSent.connect(self.status_bar.showMessage)
        io_operations_handler.daemon = True
        io_operations_handler.hasFinished.connect(lambda: self.displayDyks(io_operations_handler.results))
        io_operations_handler.loadParameters(f=dParsonsManifold, _args=[xdata, prp])
        io_operations_handler.start()

    def displayKCoz(self, content):
        content = list(content)
        content.insert(0, 'Resultados - Kozeny-Carman')
        self.spreadsheet.addColumn(content)

    def displayWinl(self, content):
        self.loadPltE(content[:2])
        content[2].insert(0, 'R35 - Winland')
        content[3].insert(0, 'Ports - Winland')
        self.spreadsheet.addColumn(content[2])
        self.spreadsheet.addColumn(content[3])

    def displayTCoa(self, content):
        content.insert(0, 'Resultados - Timur Coates')
        self.spreadsheet.addColumn(content)

    def displayDyks(self, content):
        content.insert(0, 'Resultados - Dykstra-Parsons')
        self.spreadsheet.addColumn(content)
        self.p_options_6.results.setText('Atenção! Resultado pode ser diferente do coeficiente calculado através do gráfico de probabilidade. \n' + str(content[0]) + ': ' + str(content[1]))

    def displayLuci(self, results):
        self.loadPltE(results[:2])
        self.p_options_5.results.setText('Número médio de fábrica de rocha: ' + str(round(results[2], 4)))

    def displayFZIR(self, results):
        results[0].insert(0, 'Resultados - RQI (μm)')
        self.spreadsheet.addColumn(results[0])
        results[1].insert(0, 'Resultados - PhiZ')
        self.spreadsheet.addColumn(results[1])
        self.loadPltE(results[2:])

    def displayRegr(self, display_name, results):
        results.insert(0, 'Resultados da Regressão')
        self.spreadsheet.addColumn(results[0])
        self.s_options_1.results.setText(str(results[0])+results[1])
        self.loadPltE(results[-2:])

    def displayStat(self, display_name, results):
        results.insert(0, 'Resultados - Estatística')
        self.spreadsheet.addColumn(results)
        self.s_options_2.results.setText(str(results))

    def displayHist(self, results):
        self.loadPltE(results, 'Histograma')

    def displayBxpl(self, results):
        self.loadPltE(results, 'Boxplot')



def test():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/Logo.ico'))
    app.setStyle('Fusion')
    win = MainWindow()
    win.showMaximized()
    win.setWindowIcon(QIcon('icons/Logo.ico'))
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()