from Rock import Rock
import plotly.graph_objects as go
import math
import numpy as np
from StreamDiverter import StreamDiverter
import plotly.io as pio

# needs to install psutil, requests, ipython, nbformat, orca as well, dependency of plotly


def luciaManifold(_k, _phi, queue):
    sample = Rock(_k, _phi)
    lc = Lucia(sample)
    lc.canvas()
    lc.classify()
    plot = lc.retrievePlot()
    queue.put([plot, lc.json, lc.rFNumber()])

class Lucia:
    def __init__(self, _sample):
        self.rock = _sample
        self.rfn = list()
        self.lrgr = np.array([])
        self.plot = go.Figure()
        self.json = ''

    def canvas(self):
        self.rfnData()
        self.luciaRegr()
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.rfn[0], fill=None, name='RFN 0.5'))
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.rfn[1], fill='tonexty', name='RFN 1.5'))
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.rfn[2], fill='tonexty', name='RFN 2.5'))
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.rfn[3], fill='tonexty', name='RFN 4.0'))
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.lrgr[0], name='Regressão Lucia C1'))
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.lrgr[1], name='Regressão Lucia C2'))
        self.plot.add_trace(go.Scatter(x=np.arange(0.01, 0.5, 0.001), y=self.lrgr[2], name='Regressão Lucia C3'))
        self.plot.update_layout(title="Classificação de Lucia", xaxis=dict(title="Porosidade Interpartícula"), yaxis=dict(title="Permeabilidade (mD)"), xaxis_type='log', yaxis_type='log')
        self.plot.update_xaxes(range=[-2, -0.3010])
        self.plot.update_yaxes(range=[-2, 4])

    def classify(self):
        k = self.rock.getK()
        phi = self.rock.getPhi()
        print(k, phi)
        self.plot.add_trace(go.Scatter(x=phi, y=k, name='Series A', mode='markers'))

    def retrievePlot(self):
        self.json = pio.to_json(self.plot)

        diverter = StreamDiverter()
        self.plot.show(renderer='iframe')
        return diverter.srcExtractor()

    def rfnData(self):
        rfn = [0.5, 1.5, 2.5, 4]
        A = 9.7982
        B = 12.0838
        C = 8.6711
        D = 8.2965
        tomiliDarcy = 1000 / (1.01325 * 10 ** 12)

        k = []
        phi = np.arange(0.01, 0.5, 0.001)

        for n in rfn:
            k.clear()
            for p in phi:
                st = (A - (B * math.log10(n)))
                nd = (C - (D * math.log10(n)))
                rslt = 10 ** (st + (nd * math.log10(p)))
                k.append(rslt)
            self.rfn.append(k.copy())

    def luciaRegr(self):
        phi = np.arange(0.01, 0.5, 0.001)
        k = [0, 0, 0]
        k[0] = [(45.35 * 10 ** 8) * p ** 8.537 for p in phi]
        k[1] = [(2.040 * 10 ** 6) * p ** 6.38 for p in phi]
        k[2] = [(2.884 * 10 ** 3) * p ** 4.275 for p in phi]
        self.lrgr = np.array(k)
        
    def rFNumber(self):
        """
        Calcula o número rfn médio
        :return:
        """
        A = 9.7982
        B = 12.0838
        C = 8.6711
        D = 8.2965

        k = np.mean(self.rock.getK())
        phi = np.mean(self.rock.getPhi())

        numerator = pow(10, A+C*math.log10(phi))
        denominator = k
        inverse_power = B+D*math.log10(phi)

        rfn = pow(numerator/denominator, 1/inverse_power)
        return rfn
