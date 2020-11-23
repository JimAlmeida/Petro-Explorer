from Rock import Rock
from Rock import extractor
from numpy import array, roots
import math as m


def kCarmanManifold(_k, _phi, svgr, calculation, queue):
    sample = Rock(_k, _phi)
    kc_calculation = KozenyCarman(sample, _svgr=svgr)
    results = []
    if calculation == "Permeabilidade (mD)":
        kc_calculation.calcK()
        results = sample.getK()
    elif calculation == "Porosidade (%)":
        kc_calculation.calcPhi()
        results = sample.getPhi()
    elif calculation == "SVgr (cm-1)":
        kc_calculation.calcSVGR()
        results = kc_calculation.getSVGR()
    elif calculation == "Tortuosidade":
        kc_calculation.calcTort()
        results = kc_calculation.getTort()
    else:
        kc_calculation.calcSVGR()
        results = kc_calculation.getSVGR()
    queue.put(results)


class KozenyCarman:
    def __init__(self, _sample, _svgr=None):
        self.rock = _sample
        self.tortuosidade = []
        self.svgr = None
        self.rock.setPhi([p / 100 for p in _sample.getPhi()])  # convert porosity from % to decimal

        if _svgr is None:
            _svgr = []
        else:
            self.svgr = [float(y) for y in _svgr if extractor(y)]

    def calcSVGR(self):
        phi = self.rock.getPhi().copy()
        k = [_k * ((10**-11)/0.9869) for _k in self.rock.getK()] #convert mD to cm2
        self.svgr = [m.sqrt(1 / (5 * k[i]) * (phi[i] ** 3 / (1 - phi[i]) ** 2)) for i in range(len(phi))]

    def calcK(self):
        phi = self.rock.getPhi().copy()
        k = [(1/(5*(self.svgr[i]**2))*(phi[i]**3/(1-phi[i])**2))*(0.9869*(10**11)) for i in range(len(phi))]
        self.rock.setK(array(k))

    def calcTort(self):
        pass

    def getSVGR(self):
       return self.svgr

    def getTort(self):
        return None