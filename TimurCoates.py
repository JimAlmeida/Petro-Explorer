import numpy as np
from Rock import Rock


def tCoatesManifold(k, phi, swir, calculation, queue):
    sample = Rock(k, phi)
    tc_calculation = TimurCoates(sample, swir)
    results = []

    if calculation == "Permeabilidade":
        tc_calculation.calcK()
        results = sample.getK()
    if calculation == "Swir":
        tc_calculation.calcSwir()
        results = tc_calculation.getSwir()
    if calculation == "BVI":
        tc_calculation.calcBVI()
        results = tc_calculation.getBVI()
    if calculation == "FFI":
        tc_calculation.calcFFI()
        results = tc_calculation.getFFI()

    queue.put(list(results))

class TimurCoates:
    def __init__(self, _rock, _swir=[]):
        assert isinstance(_rock, Rock)
        self.a = 0.136
        self.b = 4.4
        self.c = 2
        self.rock = _rock
        self.swir = np.array(_swir)

    def calcSwir(self):
        x = [p for p in self.rock.getPhi()]
        y = [k for k in self.rock.getK()]

        for i in range(len(x)):
            v = (self.a*(x[i]**self.b)/y[i])**(1/self.c)
            self.swir = np.append(self.swir, v)

    def calcK(self):
        k = []
        phi = self.rock.getPhi()
        for i in range(len(phi)):
            k.append(self.a * pow(phi[i], self.b) * pow((1-self.swir[i])/self.swir[i], self.c))
        k = np.array(k)
        self.rock.setK(k)
        return k

    def calcPhi(self):
        phi = []
        k = self.rock.getK()
        for i in range(len(k)):
            phi.append(pow(k[i]/(self.a * pow((1 - self.swir[i]) / self.swir[i], self.c)), 1/self.b))
        phi = np.array(phi)
        self.rock.setPhi(phi)
        return phi

    def getSwir(self):
        return self.swir
