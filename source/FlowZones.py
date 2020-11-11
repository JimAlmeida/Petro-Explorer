from Rock import Rock
from math import sqrt
import plotly.io as pio
import plotly.graph_objects as go
from StreamDiverter import StreamDiverter


def fzManifold(_k, _phi, swir, _un, _prp, queue):
    sample = Rock(_k, _phi)
    f = FlowZones(sample, _un, swir)
    f.calcPhiZ()
    f.calcRQI()
    f.plot()
    queue.put([f.rqi, f.phi_z, f.plot_path, f.json])


class FlowZones:
    def __init__(self, _sample, unit, swir=None):
        self.rqi = list()
        self.phi_z = list()
        self.fzi = list()
        self.swir = swir
        self.unit = unit
        self.rock = _sample
        self.plot_path = ''
        self.json = ''
        self.fig = go.Figure()

    def calcPhiZ(self):
        self.phi_z = [f/(1-f) for f in self.rock.getPhi()]

    def calcRQI(self):
        k = self.rock.getK()
        p = self.rock.getPhi()
        if self.swir is None:
            if self.unit == 'SI':
                self.rqi = [sqrt(k[i]/p[i]) for i in range(len(k))]
            if self.unit == 'Darcy':
                self.rqi = [0.0314*sqrt(k[i] / p[i]) for i in range(len(k))]
        else:
            if self.unit == 'SI':
                self.rqi = [sqrt(p[i]**3)*(p[i](1-self.swir[i])/p[i]-p[i](1-self.swir[i])) for i in range(len(k))]
            if self.unit == 'Darcy':
                self.rqi = [3.14*sqrt(p[i]**3)*(p[i](1-self.swir[i])/p[i]-p[i](1-self.swir[i])) for i in range(len(k))]

    def calcFZI(self):
        self.fzi = []

    def plot(self):

        self.fig.update_layout(title="Estudo de Zonas de Fluxo", xaxis=dict(title="Phi-Z"),
                               yaxis=dict(title="RQI"), xaxis_type='log', yaxis_type='log')

        self.fig.add_trace(go.Scatter(x=self.phi_z, y=self.rqi, fill=None, name='Dados', mode='markers'))

        self.json = pio.to_json(self.fig)
        diverter = StreamDiverter()
        self.fig.show(renderer='iframe')
        self.plot_path = diverter.srcExtractor()
