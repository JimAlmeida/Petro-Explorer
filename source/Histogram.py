import plotly.graph_objects as go
import pandas as pd
import StreamDiverter as sd
import plotly.io as pio
import numpy as np


def histogramManifold(data, _nbins, queue):
    data = np.array([float(y) for y in data if y.strip('-').isnumeric()])
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
        self.fig.add_trace(go.Histogram(x=self.data, nbinsx=self.nbins))
        self.plot_path = ''
        self.json = ''

    def plot(self):
        self.json = pio.to_json(self.fig)
        diverter = sd.StreamDiverter()
        self.fig.show(renderer='iframe')
        self.plot_path = diverter.srcExtractor()
        return self.plot_path