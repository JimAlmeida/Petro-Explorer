import numpy as np
from scipy import stats
from Rock import extractor

# typedef
numpyarray = np.ndarray


def statisticsManifold(_xdata: list, method: str, quartile, percentile, queue):
    xdata = np.array([float(x) for x in _xdata if extractor(x)])

    st = Statistics(xdata)
    methods = ['Média aritmética', 'Média Ponderada', 'Mediana', 'Moda', 'Variância Pop.', 'Variância Am.', 'Desvio Padrão Pop.', 'Desvio Padrão Am.', 'Máximo', 'Mínimo', 'Amplitude', 'Quartil', 'Percentil']
    container = []

    if method == methods[0]:
        container.append(st.average())
    if method == methods[1]:
        container.append(st.average())
    if method == methods[2]:
        container.append(st.median())
    if method == methods[3]:
        container.append(st.mode())
    if method == methods[4]:
        container.append(st.varP())
    if method == methods[5]:
        container.append(st.varS())
    if method == methods[6]:
        container.append(st.stdevP())
    if method == methods[7]:
        container.append(st.stdevS())
    if method == methods[8]:
        container.append(st.max())
    if method == methods[9]:
        container.append(st.min())
    if method == methods[10]:
        container.append(st.range())
    if method == methods[11]:
        container.append(st.quartile(quartile))
    if method == methods[12]:
        container.append(st.percentile(percentile))

    queue.put(container)


class Statistics:
    def __init__(self, xarray):
        self.x = np.array(xarray)

    def median(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.median(self.x)
        except Exception as e:
            print(e)

    def mode(self):
        assert isinstance(self.x, numpyarray)
        try:
            return stats.mode(self.x)[0][0]
        except Exception as e:
            print(e)

    def average(self):
        print(isinstance(self.x, numpyarray), type(self.x))
        assert isinstance(self.x, numpyarray)
        try:
            return np.mean(self.x)
        except Exception as e:
            print(e)

    def wAverage(self, pesos):
        assert isinstance(self.x, numpyarray)
        try:
            return np.average(self.x, weights=pesos)
        except Exception as e:
            print(e)

    def varP(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.var(self.x)
        except Exception as e:
            print(e)

    def varS(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.var(self.x, ddof=1)
        except Exception as e:
            print(e)

    def stdevP(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.sqrt(np.var(self.x))
        except Exception as e:
            print(e)

    def stdevS(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.sqrt(np.var(self.x, ddof=1))
        except Exception as e:
            print(e)

    def max(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.amax(self.x)
        except Exception as e:
            print(e)

    def min(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.amin(self.x)
        except Exception as e:
            print(e)

    def range(self):
        assert isinstance(self.x, numpyarray)
        try:
            return np.ptp(self.x)
        except Exception as e:
            print(e)

    def quartile(self, quart: float = 0.5):
        assert isinstance(self.x, numpyarray)
        try:
            return np.quantile(self.x, quart/4)
        except Exception as e:
            print(e)

    def percentile(self, perc: int = 50):
        assert isinstance(self.x, numpyarray)
        try:
            return np.percentile(self.x, perc)
        except Exception as e:
            print(e)

    @staticmethod
    def pearson(xarray, yarray):
        assert isinstance(xarray, numpyarray)
        assert isinstance(yarray, numpyarray)
        assert xarray.shape == yarray.shape
        try:
            return pow(stats.pearsonr(xarray, yarray)[0], 2)
        except Exception as e:
            print(e)


#boxplot
#trace0 = go.Box( y=[2.37, 2.16, 4.82, 1.73, 1.04, 0.23, 1.32, 2.91, 0.11, 4.51, 0.51, 3.75, 1.35, 2.98, 4.50, 0.18, 4.66, 1.30, 2.06, 1.19], name='Only Mean',
#   marker=dict(color='rgb(8, 81, 156)',),boxmean=True)