import math
from Rock import Rock
import numpy as np

import plotly.graph_objects as go
import plotly.io as pio
from StreamDiverter import StreamDiverter

def winlandManifold(k, phi, queue):
    sample = Rock(k, phi)
    w = Winland(sample)
    w.canvas()
    w.classify()
    plot = w.retrievePlot()
    r35 = w.poreThroat()
    ports = w.port_classifications
    queue.put([plot, w.json, r35, ports])


class Winland:
    pittman = {
               'r10': (0.459, .500, -0.385),
               'r15': (0.333, .509, -0.344),
               'r20': (0.218, .519, -0.303),
               'r25': (0.204, .531, -0.350),
               'r30': (0.215, .547, -0.420),
               'r35': (0.255, .565, -0.523),
               'r40': (0.360, .582, -0.680),
               'r45': (0.609, .608, -0.974),
               'r50': (0.778, .626, -1.205),
               'r55': (0.948, .632, -1.426),
               'r60': (1.096, .648, -1.666),
               'r65': (1.372, .643, -1.979),
               'r70': (1.664, .627, -2.314),
               'r75': (1.880, .609, -2.626),
               }

    def __init__(self, rock):
        #standard parameters are Winland's R35 method
        assert isinstance(rock, Rock)
        self.k = rock.getK()
        self.phi = rock.getPhi()
        self.plot = go.Figure()
        self.port_classifications = []

    def poreThroat(self, a=0.732, b=0.588, c=-0.8641):
        results = []
        for i in range(len(self.k)):
            try:
                logR35 = a+(b*math.log10(self.k[i]))+(c*math.log10(self.phi[i]))
                results.append(10**logR35)
            except IndexError:
                break
        return results

    def canvas(self, coefficients: tuple = (0.732, 0.588, -0.8641)):
        r35_values = (0.5, 1, 2, 5, 10)
        n_phi = np.arange(5, 40.1, 0.1)
        k_values = []
        for r in r35_values:
            k = []
            for p in n_phi:
                a = 10**((math.log10(r)-coefficients[0]-coefficients[2]*math.log10(p))/coefficients[1])
                k.append(a)
            k_values.append(k)

        self.plot.add_trace(go.Scatter(x=n_phi, y=k_values[0],  fillcolor='rgba(245, 125, 78, 0.25)', name='R35 - 0.5μm'))
        self.plot.add_trace(go.Scatter(x=n_phi, y=k_values[1],  fillcolor='rgba(78, 144, 245, 0.25)', name='R35 - 1μm'))
        self.plot.add_trace(go.Scatter(x=n_phi, y=k_values[2],  fillcolor='rgba(78, 144, 245, 0.25)', name='R35 - 2μm'))
        self.plot.add_trace(go.Scatter(x=n_phi, y=k_values[3],  fillcolor='rgba(111, 255, 0, 0.25)', name='R35 - 5μm'))
        self.plot.add_trace(go.Scatter(x=n_phi, y=k_values[4],  fillcolor='rgba(111, 255, 0, 0.25)', name='R35 - 10μm'))

        cat = [dict(xref='paper', yref='paper', x=0, y=1.1, showarrow=False, xanchor='left',
                    text='Categorização das unidades de fluxo: Megaport (r35 > 10μm) - Macroport (2μm < r35 ≤ 10μm) - Mesoport (0.5μm < r35 ≤ 2μm) - Microport (r35μm < 0.5μm)')]

        self.plot.update_layout(title="Classificação de Winland", xaxis=dict(title="Porosidade (%)"),
                                yaxis=dict(title="Permeabilidade (mD)"), yaxis_type='log', annotations=cat)

        if len(self.k) > 0:
            log_max_k = math.log10(max(self.k))
            if log_max_k <= 4:
                self.plot.update_yaxes(range=[-1, 4])
            else:
                self.plot.update_yaxes(range=[-1, log_max_k])

            self.plot.update_xaxes(range=[0, 40])

    def classify(self):
        r35 = self.poreThroat()

        for r in r35:
            if r > 10:
                self.port_classifications.append('Megaport')
            elif 2 < r <= 10:
                self.port_classifications.append('Macroport')
            elif 0.5 < r <= 2:
                self.port_classifications.append('Mesoport')
            else:
                self.port_classifications.append('Microport')

        self.plot.add_trace(go.Scatter(x=self.phi, y=self.k, mode='markers', hovertext=self.port_classifications, hoverinfo='all'))

    def retrievePlot(self):
        self.json = pio.to_json(self.plot)
        diverter = StreamDiverter()
        self.plot.show(renderer='iframe')
        return diverter.srcExtractor()
