from Statistics import Statistics
import math
import numpy as np
import plotly.graph_objects as go
from StreamDiverter import StreamDiverter
import plotly.io as pio


def advancedExtractor(data):
    try:
        r = float(data)
        return True
    except ValueError:
        return False


def regressionManifold(_xdata: list, _ydata: list, dgr: int, regr: str, queue):

    ydata = np.array([float(y) for y in _ydata if advancedExtractor(y)])
    xdata = np.array([float(x) for x in _xdata if advancedExtractor(x)])

    print('XData Length - Regressions', len(xdata))
    print('YData Length - Regressions', len(ydata))
    if regr == 'Linear':
        regr_obj = LinearRegr(xdata, ydata)
    elif regr == 'Exponencial':
        regr_obj = ExpRegr(xdata, ydata)
    elif regr == 'Potencial':
        regr_obj = PotRegr(xdata, ydata)
    elif regr == 'Logarítmica':
        regr_obj = LogRegr(xdata, ydata)
    elif regr == 'Polinomial':
        regr_obj = RegrPol(xdata, ydata, dgr)
    else:
        regr_obj = LinearRegr(xdata, ydata)

    coefficients = regr_obj.calcRegr()
    assert(isinstance(coefficients, tuple))
    regr_obj.plot()
    equation = prettyText(coefficients, regr, regr_obj.r2)
    print('OYE', equation)
    container = [equation, regr_obj.plot_address, regr_obj.json_data]
    queue.put(container)


def prettyNumber(n):
    r = round(n, 4)
    if r > 0:
        x = '+ ' + str(r)
    else:
        x = str(r)
    return x


def prettyText(coef, typ, r2):
    ax = ''
    if typ =='Polinomial':
        ax = str(coef[0])
        dgr = 1
        for c in coef[1:]:
            ax += prettyNumber(c) + 'x^' + str(dgr) + ' '
            dgr += 1
    if typ == 'Linear':
        ax = str(coef[0]) + ' ' + prettyNumber(coef[1]) + 'x'
    if typ == 'Potencial':
        ax = str(coef[0]) + 'x^' + str(coef[1])
    if typ == 'Exponencial':
        ax = str(coef[0]) + 'e^' + str(coef[1]) + 'x'
    if typ == 'Logarítmica':
        ax = str(coef[1]) + 'ln(x)' + prettyNumber(coef[0])

    s = 'Resultados da regressão'
    t = 'Tipo da regressão: ' + typ
    e = 'Equação de ajuste: ' + ax
    p = 'Coefficiente de Pearson: ' + str(round(r2, 4))

    return '\n' + t + '\n' + e + '\n' + p


class LinearRegr:
    def __init__(self, _x, _y):
        self.xdata = _x
        self.ydata = _y
        self.original_xdata = _x
        self.original_ydata = _y
        self.b1 = 0.0
        self.b0 = 0.0
        self.plot_address = ''
        self.json_data = ''
        self.r2 = 0.0

    def calcRegr(self):
        x_avg = Statistics(self.xdata).average()
        y_avg = Statistics(self.ydata).average()

        z = 0.0
        w = 0.0
        for i in range(len(self.xdata)):
            z += pow(self.xdata[i] - x_avg, 2)
            w += (self.xdata[i] - x_avg) * (self.ydata[i] - y_avg)

        self.b1 = w / z
        self.b0 = (sum(self.ydata) - self.b1 * sum(self.xdata)) / len(self.ydata)

        y_reg = [self.b1 * x + self.b0 for x in self.xdata]
        self.r2 = Statistics.pearson(self.ydata, np.array(y_reg))

        r = (self.b0, self.b1)
        return r

    def plot(self):
        x_reg = np.arange(min(self.original_xdata), max(self.original_xdata), (max(self.original_xdata)-min(self.original_xdata))/1000)
        y_reg = [self.b1 * x + self.b0 for x in x_reg]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.original_xdata, y=self.original_ydata, fill=None, name='Dados originais', mode='markers'))
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, fill=None, name='Dados da regressão'))
        fig.update_layout(title="Regressão Linear", xaxis=dict(title="X"), yaxis=dict(title="Y"))

        self.json_data = pio.to_json(fig)

        diverter = StreamDiverter()
        fig.show(renderer='iframe')
        self.plot_address = diverter.srcExtractor()


class PotRegr(LinearRegr):
    def __init__(self, _x, _y):
        super().__init__(_x, _y)

        self.original_xdata = _x
        self.original_ydata = _y

        self.xdata = np.array([math.log(x, 10) for x in self.xdata])
        self.ydata = np.array([math.log(y, 10) for y in self.ydata])

    def calcRegr(self):
        x_avg = Statistics(self.xdata).average()
        y_avg = Statistics(self.ydata).average()

        z = 0.0
        w = 0.0
        for i in range(len(self.xdata)):
            z += pow(self.xdata[i] - x_avg, 2)
            w += (self.xdata[i] - x_avg) * (self.ydata[i] - y_avg)

        b1 = w / z
        b0 = (sum(self.ydata) - b1 * sum(self.xdata)) / len(self.ydata)

        y_reg = [b1 * x + math.pow(10, b0) for x in self.xdata]
        self.r2 = Statistics.pearson(self.ydata, np.array(y_reg))

        self.b0 = math.pow(10, b0)
        self.b1 = b1

        r = (math.pow(10, b0), b1)
        return r

    def plot(self):
        x_reg = np.arange(min(self.original_xdata), max(self.original_xdata), (max(self.original_xdata)-min(self.original_xdata))/1000)
        y_reg = [self.b0 * pow(x, self.b1) for x in x_reg]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.original_xdata, y=self.original_ydata, fill=None, name='Dados originais', mode='markers'))
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, fill=None, name='Dados da regressão'))
        fig.update_layout(title="Regressão Potencial", xaxis=dict(title="X"), yaxis=dict(title="Y"))

        self.json_data = pio.to_json(fig)

        diverter = StreamDiverter()
        fig.show(renderer='iframe')
        self.plot_address = diverter.srcExtractor()


class ExpRegr(LinearRegr):
    def __init__(self, _x, _y):
        super().__init__(_x, _y)

        self.original_xdata = _x
        self.original_ydata = _y

        self.ydata = np.array([math.log(y) for y in self.ydata])

    def calcRegr(self):
        x_avg = Statistics(self.xdata).average()
        y_avg = Statistics(self.ydata).average()

        z = 0.0
        w = 0.0
        for i in range(len(self.xdata)):
            z += pow(self.xdata[i] - x_avg, 2)
            w += (self.xdata[i] - x_avg) * (self.ydata[i] - y_avg)

        b1 = w / z
        b0 = (sum(self.ydata) - b1 * sum(self.xdata)) / len(self.ydata)

        y_reg = [b1 * x + math.exp(b0) for x in self.xdata]
        self.r2 = Statistics.pearson(self.ydata, np.array(y_reg))

        self.b1 = b1
        self.b0 = math.exp(b0)

        r = (math.exp(b0), b1)
        return r

    def plot(self):
        x_reg = np.arange(min(self.original_xdata), max(self.original_xdata), (max(self.original_xdata)-min(self.original_xdata))/1000)
        y_reg = [self.b0 * math.exp(self.b1*x) for x in x_reg]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.original_xdata, y=self.original_ydata, fill=None, name='Dados originais', mode='markers'))
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, fill=None, name='Dados da regressão'))
        fig.update_layout(title="Regressão Exponencial", xaxis=dict(title="X"), yaxis=dict(title="Y"))

        self.json_data = pio.to_json(fig)

        diverter = StreamDiverter()
        fig.show(renderer='iframe')
        self.plot_address = diverter.srcExtractor()


class LogRegr(LinearRegr):
    def __init__(self, _x, _y):
        super().__init__(_x, _y)

        self.original_xdata = _x
        self.original_ydata = _y

        self.xdata = np.array([math.log(x) for x in self.xdata])

    def calcRegr(self):
        x_avg = Statistics(self.xdata).average()
        y_avg = Statistics(self.ydata).average()

        z = 0.0
        w = 0.0
        for i in range(len(self.xdata)):
            z += pow(self.xdata[i] - x_avg, 2)
            w += (self.xdata[i] - x_avg) * (self.ydata[i] - y_avg)

        b1 = w / z
        b0 = (sum(self.ydata) - b1 * sum(self.xdata)) / len(self.ydata)

        y_reg = [b1 * x + b0 for x in self.xdata]
        self.r2 = Statistics.pearson(self.ydata, np.array(y_reg))

        self.b0 = b0
        self.b1 = b1

        r = (b0, b1)
        return r

    def plot(self):
        x_reg = np.arange(min(self.original_xdata), max(self.original_xdata), (max(self.original_xdata)-min(self.original_xdata))/1000)
        y_reg = [self.b0 + self.b1*math.log(x) for x in x_reg]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.original_xdata, y=self.original_ydata, fill=None, name='Dados originais', mode='markers'))
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, fill=None, name='Dados da regressão'))
        fig.update_layout(title="Regressão Logarítmica", xaxis=dict(title="X"), yaxis=dict(title="Y"))

        self.json_data = pio.to_json(fig)

        diverter = StreamDiverter()
        fig.show(renderer='iframe')
        self.plot_address = diverter.srcExtractor()


class RegrPol:
    def __init__(self, _xdata, _ydata, degree=2):
        self.xdata = _xdata
        self.ydata = _ydata
        self.dgr = degree
        self.r2 = 0
        self.coefficients = []

    def linSystemSolver(self, matrix, column):
        return tuple(np.linalg.solve(matrix, column))

    def calcRegr(self):
        m = []
        b = [0 for i in range(self.dgr + 1)]
        for i in range(self.dgr + 1):
            m.append([0 for i in range(self.dgr + 1)])

        for r in range(self.dgr + 1):
            k = r
            b[r] = np.sum((self.xdata ** r) * self.ydata)
            for c in range(self.dgr + 1):
                m[r][c] = np.sum(self.xdata ** k)
                k += 1

        matrix = np.array(m)
        column = np.array(b)

        self.coefficients = self.linSystemSolver(matrix, column)
        y_reg = []
        aux = 0.0
        dgr = 0
        for x in self.xdata:
            for c in self.coefficients:
                aux += c*pow(x, dgr)
                print()
                dgr += 1
            y_reg.append(aux)
            aux = 0.0
            dgr = 0
        y_reg = np.array(y_reg)
        self.r2 = Statistics.pearson(self.ydata, y_reg)

        return self.coefficients

    def plot(self):
        x_reg = np.arange(min(self.xdata), max(self.xdata),
                          (max(self.xdata) - min(self.xdata)) / 1000)
        y_reg = []
        aux = 0.0
        dgr = 0
        for x in x_reg:
            for c in self.coefficients:
                aux += c*pow(x, dgr)
                dgr += 1
            y_reg.append(aux)
            aux = 0.0
            dgr = 0
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.xdata, y=self.ydata, fill=None, name='Dados originais', mode='markers'))
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, fill=None, name='Dados da regressão'))
        fig.update_layout(title="Regressão Polinomial", xaxis=dict(title="X"), yaxis=dict(title="Y"))

        self.json_data = pio.to_json(fig)

        diverter = StreamDiverter()
        fig.show(renderer='iframe')
        self.plot_address = diverter.srcExtractor()


#Arrays for testing purposes
#x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
#y = np.array([1,8,27,64,125,231,541,652,915])
