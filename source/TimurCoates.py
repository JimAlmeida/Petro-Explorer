import numpy as np
from Rock import Rock


def tCoatesManifold(k, phi, swir, calculation, queue):
    sample = Rock(k, phi, swir)
    tc_calculation = TimurCoates(sample)
    results = []

    if calculation == "Permeabilidade":
        tc_calculation.calcK()
        results = sample.getK()
    if calculation == "Swir (%)":
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
    def __init__(self, _rock):
        assert isinstance(_rock, Rock)
        self.a = 0.136
        self.b = 4.4
        self.c = 2
        self.rock = _rock
        self.swir = _rock.getSwir()
        self.bvi = np.array([])
        self.ffi = np.array([])

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

    def calcBVI(self):
        x = self.rock.getPhi()
        for i in range(len(x)):
            v = x[i] * self.swir[i]/100
            self.bvi = np.append(self.bvi, v)

    def calcFFI(self):
        x = self.rock.getPhi()
        for i in range(len(x)):
            f = x[i] * (1 - self.swir[i]/100)
            self.ffi = np.append(self.ffi, f)

    def getSwir(self):
        return self.swir

    def getBVI(self):
        return self.bvi

    def getFFI(self):
        return self.ffi