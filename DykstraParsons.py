from Statistics import Statistics
from Rock import Rock
import math

def dParsonsManifold(_k, calculation, queue):
    sample = Rock(_k)
    dp_calculation = DysktraParsons(sample)
    results = []
    dp_calculation.calcCoef()

    if calculation == "Grau de heterogenêidade":
        results.append(dp_calculation.heterogeneityLevel())
    elif calculation == "Coeficiente de Dykstra-Parsons":
        results.append(dp_calculation.getCoef())
    else:
        results.append(dp_calculation.getCoef())

    queue.put(results)

class DysktraParsons:
    def __init__(self, _rock):
        assert isinstance(_rock, Rock)
        self.coef_dykstra = None
        self.logK = [math.log(k) for k in _rock.k]
        self.statistics_handler = Statistics(self.logK)

    def calcCoef(self):
        #self.coef_dykstra = self.statistics_handler.stdevS()/self.statistics_handler.average() -> Tiab
        self.coef_dykstra = 1 - math.exp(self.statistics_handler.stdevS()*-1)

    def heterogeneityLevel(self):
        if self.coef_dykstra == 0.0:
            return "Perfeitamente Homogêneo"
        elif 0.0 < self.coef_dykstra < 0.25:
            return "Leve heterogêneidade"
        elif 0.25 < self.coef_dykstra < 0.5:
            return "Heterogêneo"
        elif 0.5 < self.coef_dykstra < 0.75:
            return "Muito Heterogêneo"
        elif 0.75 < self.coef_dykstra < 1:
            return "Extremamente Heterogêneo"
        elif self.coef_dykstra == 1:
            return "Perfeitamente Heterogêneo"

    def getCoef(self):
        return self.coef_dykstra
