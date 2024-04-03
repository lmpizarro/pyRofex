import yfinance as yf
import numpy as np

refTicker = 'EWZ'
tickers = ['JNJ', 'WMT', 'PG', 'PEP', 'KO', 'BRK-B', 'V']
tickers_ = ['SPY', 'DIA', 'EEM',  'XLF', 'EWZ'] # 'QQQ','^MERV', 'EWZ', 'ARKK', 'EWZ', 'IWM', 'XLE',
# Beta over 1.5
tickers = ['NVDA', 'TSLA', 'AMD', 'AMAT']
tickers = ['LRCX', 'C', 'BA', 'SHOP', 'KKR']
tickers = ['APO', 'HCA', 'CNQ', 'STLA', 'SLB']
tickers = ['MAR', 'MPC', 'PH', 'FCX', 'COIN', 'NXPI']
# 1 a 1.5
tickers = ['AAPL', 'GOOG', 'AMZN', 'META', 'TSM']
tickers = ['AVGO', 'JPM', 'MA', 'ASML', 'ORCL']
tickers = ['BAC', 'CRM', 'NFLX', 'ACN', 'ADBE']
#
tickers = ['MSFT', 'BRK-B', 'LLY', 'V', 'WMT']
tickers = ['XOM', 'UNH', 'NVO', 'HD', 'MRK']
tickers = ['SPY', 'DIA', 'EEM',  'XLF'] # 'QQQ','^MERV', 'EWZ', 'ARKK', 'EWZ', 'IWM', 'XLE',
tickers.append(refTicker)
df = yf.download(tickers=tickers, period='1Y')['Adj Close']


dflogRet = np.log(df) - np.log(df.shift(1))
dflogRet.dropna(inplace=True)

Var = True
if Var:
    stDevs = -dflogRet.quantile(0.05).to_frame().rename(columns={0.05:'stdev'})
    stDevs['cVar'] = 0.0
    means = []
    for ticker in tickers:
        mean = dflogRet[ticker][dflogRet[ticker] < -stDevs.loc[ticker]['stdev']].mean()
        stDevs.loc[ticker]['cVar'] = -mean

    stDevs['invRisk'] = 1 / stDevs['cVar']
    stDevs['portPct'] = 100*stDevs['invRisk']/stDevs['invRisk'].sum()
    print(stDevs)
else:
    stDevs = dflogRet.std().to_frame().rename(columns={0:'stdev'})

stDevs['invRisk'] = 1 / stDevs['stdev']
stDevs['portPct'] = 100*stDevs['invRisk']/stDevs['invRisk'].sum()
# refPct = stDevs['portPct'].loc[refTicker]
# stDevs['balance'] = stDevs['portPct'] / refPct

print(stDevs)


"""
Risk
ticker   risk      invRisk     pct       balance
DIA     0.006242  160.210349  26.668771  2.318252
EEM     0.009178  108.951588  18.136188  1.576535
EWZ     0.014470   69.108265  11.503829  1.000000
SPY     0.007224  138.422560  23.041954  2.002981
XLF     0.008061  124.048637  20.649257  1.794990

VaR
DIA     0.010039  99.606610  26.534347  2.116318
EEM     0.014480  69.062744  18.397723  1.467359
EWZ     0.021247  47.066002  12.537979  1.000000
SPY     0.012084  82.752740  22.044620  1.758228
XLF     0.013004  76.899362  20.485331  1.633862
"""

