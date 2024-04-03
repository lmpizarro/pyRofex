import yfinance as yf
from datetime import datetime
import pickle
import numpy as np

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

symbol = 'spy'

def download(symbol):
    ticker = yf.Ticker(symbol)
    today = datetime.now().strftime('%Y-%m-%d')
    filenameCall = f'call-{today}.pckl'
    maturities = ticker.options
    close = ticker.history().iloc[-1].Close

    print(filenameCall)

    callChain = {'date': today, 'lastPrice': close, 'chain': {}}
    for maturity in maturities:
        calls = ticker.option_chain(maturity).calls
        callChain['chain'][maturity] = calls

    print(callChain)
    # open a file, where you ant to store the data
    file = open(filenameCall, 'wb')

    # dump information to that file
    pickle.dump(callChain, file)

    # close the file
    file.close()



# download(symbol=symbol)

def load(filename):
    # open a file, where you stored the pickled data
    file = open(filename, 'rb')

    # dump information to that file
    data = pickle.load(file)

    # close the file
    file.close()

    return data

def objective3(x, a, b, c, d):
 return a * x*x*x + b *x*x + c*x +d
def objective2(x, a, b, c):
 return a * x*x + b *x + c



# S K T sigma r d
yieldR = [0, 5.33, 5.52, 5.47, 5.48, 5.41, 5.37, 5.01, 4.61, 4.37, 4.19, 4.20, 4.19, 4.45, 4.35]
terms = [0, 1/360, 1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30 ]
myTerms = 2*np.asarray(terms)

chain = load('call-2024-03-14.pckl')
cols = ['strike', 'impliedVolatility', 'lastPrice', 'T', 'r', 'S/K']
minKs = []
maxKs = []
for mat, calls in chain['chain'].items():
    print(mat)
    T = (datetime.fromisoformat(mat)- datetime.now()).days/360
    calls['T'] = T
    if T > .1:
        continue

    calls['r'] = np.interp(T, terms, yieldR) / 100
    calls['S/K'] = chain['lastPrice'] / calls['strike']
    calls = calls[cols]
    calls = calls.rename(columns={'lastPrice': 'C', 'impliedVolatility': 'sigma0', 'strike': 'K'})

    calls = calls[calls['S/K'].between(.90, 1.05)]
    calls = calls[calls['sigma0'].between(.3*calls['sigma0'].mean(), 1.7*calls['sigma0'].mean())]
    calls['sigma0'].replace(0, np.nan, inplace=True)
    calls['sigma0'].interpolate(method='spline', order=3, inplace=True, limit=20)
    calls['sigma0'].fillna(0, inplace=True)

    if len(calls) < 4:
       continue

    x_range = np.arange(.90, 1.05, 0.005)

    popt, _ = curve_fit(objective2, calls['S/K'], calls['sigma0'])
    # summarize the parameter values
    a, b, c = popt
    # print('y = %.5f * x * x + %.5f *x + %.5f %.5f' % (a, b, c, d))


    plt.plot(calls['S/K'], calls['sigma0'], 'x')

    plt.plot(x_range, objective2(x_range, a, b, c), '-')
    plt.show()

    print(calls.head(1))

    minKs.append(calls['S/K'].min())
    maxKs.append(calls['S/K'].max())
minK, maxK = min(minKs), max(maxKs)

print(minK, maxK)

