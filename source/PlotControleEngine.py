import plotly.io as pio
import plotly.graph_objects as go
from StreamDiverter import StreamDiverter
from numpy import array
from Rock import extractor


def pceManifold(json, title, xtype, ytype, xlabel, ylabel, lxrange, uxrange, lyrange, uyrange, trace_type, x_trace, y_trace, trace_name, queue):
    engine = PlotControlEngine(json)

    xtrace = []
    ytrace = []

    if x_trace is not None and y_trace is not None and trace_type is not None:
        try:
            xtrace = array([float(y) for y in x_trace if extractor(y)])
            ytrace = array([float(x) for x in y_trace if extractor(x)])
        except ValueError:
            print('Exception raised in pceManifold() when attempting to cast types')
        engine.addTrace(xtrace, ytrace, trace_name, trace_type)
    if lxrange is not None and uxrange is not None:
        engine.changeXRange(lxrange, uxrange)
    if lyrange is not None and uyrange is not None:
        engine.changeYRange(lyrange, uyrange)
    if xtype is not None:
        engine.changeXType(xtype)
    if ytype is not None:
        engine.changeYType(ytype)
    if xlabel is not None:
        engine.changeXLabel(xlabel)
    if ylabel is not None:
        engine.changeYLabel(ylabel)
    if title is not None:
        engine.changeTitle(title)

    queue.put(engine.render())


class PlotControlEngine:
    def __init__(self, json_data):
        self.json = json_data
        if len(self.json) != 0:
            self.figure = pio.from_json(self.json)
        else:
            self.figure = go.Figure()

    def changeTitle(self, new_title):
        self.figure.update_layout(title=new_title)

    def changeXType(self, new_type):
        if new_type == 'Cartesiano':
            self.figure.update_layout(xaxis_type='linear')
        elif new_type == "Logarítmico":
            self.figure.update_layout(xaxis_type='log')

    def changeYType(self, new_type):
        if new_type == 'Cartesiano':
            self.figure.update_layout(yaxis_type='linear')
        elif new_type == "Logarítmico":
            self.figure.update_layout(yaxis_type='log')

    def changeXLabel(self, new_label):
        self.figure.update_layout(xaxis=dict(title=new_label))

    def changeYLabel(self, new_label):
        self.figure.update_layout(yaxis=dict(title=new_label))

    def changeXRange(self, lwr_range, upr_range):
        self.figure.update_xaxes(range=[lwr_range, upr_range])

    def changeYRange(self, lwr_range, upr_range):
        self.figure.update_yaxes(range=[lwr_range, upr_range])

    def addTrace(self, xdata, ydata, t_name, trace_type="Scatter"):
        if trace_type == "Scatter":
            self.figure.add_trace(go.Scatter(x=xdata, y=ydata, name=t_name))
        elif trace_type == "Boxplot":
            self.figure.add_trace(go.Box(x=xdata, name=t_name))
        else:
            print('Wrong Trace Type', trace_type)

    def render(self):
        self.json = pio.to_json(self.figure)
        diverter = StreamDiverter()
        self.figure.show(renderer='iframe')
        s = diverter.srcExtractor()
        return [s, self.json]
