from numpy import array

def extractor(v):
    if type(v) is str:
        if v.replace('.', '').replace('-', '').isnumeric():
            return True
        else:
            return False
    else:
        return True


class Rock:
    def __init__(self, _k=None, _phi=None, _swir=None):
        if _k is None:
            _k = []
        if _phi is None:
            _phi = []
        if _swir is None:
            _swir = []

        self.k = array([float(y) for y in _k if extractor(y)])
        self.phi = array([float(x) for x in _phi if extractor(x)])
        self.swir = array([float(z) for z in _swir if extractor(z)])

        self.regressions = []  # armazena os coeficientes de regressão no formato [(a,b), (a,b,c), ...]

    def setK(self, _k):
        self.k = array(_k)

    def setPhi(self, _phi):
        self.phi = array(_phi)

    def setSwir(self, _swir):
        self.swir = array(_swir)

    def getK(self):
        return self.k

    def getPhi(self):
        return self.phi

    def getSwir(self):
        return self.swir

    def addRegr(self, regression_coefficients: tuple):
        self.regressions.append(regression_coefficients)

    def input(self):
        # does it connect to the Data class to obtain k and phi data from disk?
        pass
