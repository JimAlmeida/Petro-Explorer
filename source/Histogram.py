import plotly.graph_objects as go
import pandas as pd
import StreamDiverter as sd
import plotly.io as pio
import numpy as np
from Rock import extractor


def histogramManifold(data, _nbins, queue):
    if _nbins == '':
        _nbins=0
    data = np.array([float(y) for y in data if extractor(y)])
    try:
        ndata = pd.DataFrame(data)
        nbins = int(_nbins)
    except ValueError:
        return 'Error'
    hst = Histogram(data, nbins)
    hst.plot()
    queue.put([hst.plot_path, hst.json])


class Histogram:
    def __init__(self, data, bins):
        self.data = data
        self.nbins = bins

        self.fig = go.Figure()
        self.fig.add_trace(go.Histogram(x=self.data, autobinx=True))
        self.fig.update_layout(
            title_text='Histograma',  # title of plot
            xaxis_title_text='X',  # xaxis label
            yaxis_title_text='Número de elementos',  # yaxis label
            bargap=0.1,  # gap between bars of adjacent location coordinates
            bargroupgap=0.0  # gap between bars of the same location coordinates
        )
        self.plot_path = ''
        self.json = ''

    def plot(self):
        self.json = pio.to_json(self.fig)
        diverter = sd.StreamDiverter()
        self.fig.show(renderer='iframe')
        self.plot_path = diverter.srcExtractor()
        return self.plot_path