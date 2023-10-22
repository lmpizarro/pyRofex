from rava import cash_flow_bono
import matplotlib.pyplot as plt
from flujos import flujo_ba37d


def plot_cash_flow(cf):
    plt.grid()
    plt.scatter(cf.index,  cf.acumulado, c=cf.acumulado, cmap='plasma')
    plt.axhline(y=0, color = 'r')
    plt.title(cf.iloc[-1].ticker)
    plt.show()


def plot_cash_flow_all(flujos):
    for b in flujos:
        cf = flujos[b]
        plt.grid()
        plt.plot(cf.index,  cf.acumulado, label=b)
        plt.scatter(cf.index,  cf.acumulado)
        plt.legend()
    plt.title('all bonds')
    plt.axhline(y=0, color = 'r')
    plt.show()


if __name__ == '__main__':

    flujos = {}

    for b in ['al29', 'al30', 'al35', 'ae38', 'al41', 'gd46']:
        flujo = cash_flow_bono(b)
        flujos[b] = flujo[:14]

    flujos['ba37d'] = flujo_ba37d()[:14]
    flujos['ba37d'].set_index('FECHA', inplace=True)

    plot_cash_flow_all(flujos=flujos)

