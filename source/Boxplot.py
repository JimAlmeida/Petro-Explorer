import plotly.graph_objects as go
import numpy as np
import pandas as pd
import StreamDiverter as sd
import plotly.io as pio
from Rock import extractor

def boxplotDataCleaner(_data):
    #flatten, remove strs and then convert to df

    ndata = pd.DataFrame(_data).transpose()
    rows = ndata.shape[1]
    columns = ndata.shape[0]

    auxdata = []

    for c in range(columns):
        d = [float(x) for x in list(ndata.iloc[c]) if extractor(x)]
        auxdata.append(d)

    return pd.DataFrame(auxdata).transpose()

def boxplotManifold(data, box_orientation, queue):
    try:
        ndata = boxplotDataCleaner(data)
    except ValueError:
        print('Error')
    boxes = Boxplot(ndata, box_orientation)
    boxes.plot()
    queue.put([boxes.plot_path, boxes.json])


class Boxplot:
    def __init__(self, data, _orientation='H'):
        self.fig = go.Figure()
        self.orientation = _orientation

        for s in list(data.keys()):
            if self.orientation == 'V':
                self.fig.add_trace(go.Box(y=data[s]))
            elif self.orientation == 'H':
                self.fig.add_trace(go.Box(x=data[s]))
            else:
                self.fig.add_trace(go.Box(y=data[s]))

        self.fig.update_layout(title="Boxplot", xaxis=dict(title="X"), yaxis=dict(title="Y"), xaxis_type='linear', yaxis_type='linear')

        self.plot_path = ''
        self.json = ''

    def plot(self):
        self.json = pio.to_json(self.fig)
        diverter = sd.StreamDiverter()
        self.fig.show(renderer='iframe')
        self.plot_path = diverter.srcExtractor()
        return self.plot_path

    def addBox(self, column):
        if self.orientation == 'V':
            self.fig.add_trace(go.Box(y=column))
        elif self.orientation == 'H':
            self.fig.add_trace(go.Box(x=column))
        else:
            self.fig.add_trace(go.Box(y=column))

