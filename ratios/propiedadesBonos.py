import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
from pyxirr import xirr
from dbBonosOns import flujos, bonos


df = pd.read_csv(StringIO(flujos))

def getBono(bono='pmm29', value=100):
    dfBono = df[df['Bono']==bono].copy()

    today = datetime.now().date()
    todayStr = today.strftime('%d/%m/%Y')
    dfBono.loc[-1] = [bono, todayStr, 0,0, -value]
    dfBono.index = dfBono.index + 1
    dfBono.sort_index(inplace=True)
    dfBono['Fecha'] = pd.to_datetime(dfBono['Fecha'], format='%d/%m/%Y', errors='coerce')
    dfBono = dfBono[dfBono['Fecha'] >= pd.Timestamp(today)]
    return dfBono

def setFlujo0(bono, value):
    pass

def getInteresesCorridos(dfBond):
    daysForCupon = 360 / bono['per']
    nextPayDate = dfBond['Fecha'].iloc[1]
    previousPayDate = nextPayDate - pd.Timedelta(days=int(daysForCupon))
    diasCorridos = dfBond['Fecha'].iloc[0] - previousPayDate
    intCorr = dfBond['Interés'].iloc[1] * int(diasCorridos.days) / daysForCupon

    return intCorr if intCorr > 0 else np.nan

datos =[]
for bono in bonos:
    value = bono['value']
    if value:
        dfBond = getBono(bono=bono['ticker'], value=value)

        tir = 100 * xirr(dfBond['Fecha'], dfBond['Total'])
        maturity = (dfBond['Fecha'].iloc[-1] - dfBond['Fecha'].iloc[0]).days / 360
        flujoTotal = dfBond["Total"].sum()
        dfBond['T'] = dfBond['Fecha'] - dfBond['Fecha'].iloc[0]
        dfBond['T'] = dfBond['T'].dt.days / 360
        dfBond['Period'] = dfBond['T'].diff()
        dfBond['npv'] = dfBond['Total'] / np.power(1+tir/100, dfBond['T'])
        dfBond['dur'] = dfBond['npv'] * dfBond['T'] / value
        dPq = (dfBond['Fecha'].iloc[1] - dfBond['Fecha'].iloc[0]).days
        pQ = dfBond['Total'].iloc[1]
        pctPq = pQ / value
        intsCorr = getInteresesCorridos(dfBond=dfBond)
        datos.append({'ticker': bono['ticker'],
                    'tir': tir,
                    'last': value,
                    'inter': dfBond['Interés'].sum(),
                    'amort': dfBond['Amortización'].sum(),
                    'fTotal': flujoTotal,
                    'tToMat': maturity,
                    'dur': dfBond['dur'].sum(),
                    'dPq': dPq,
                    'pQ': pQ,
                    'pctPq': 100*pctPq,
                    'FNY': flujoTotal/maturity,
                    'FNYV': 100*(flujoTotal/maturity)/value,
                    'pToAmort': value / dfBond['Amortización'].sum(),
                    # 'period': bono['per'],
                    'intCorr': intsCorr,
                    #'durMat': dfBond['dur'].sum() / maturity,
                    # 'interY': 100*dfBond['Interés'].sum()/maturity/value,
                    })
reduxDf = pd.DataFrame.from_records(datos)
pd.options.display.float_format = '{:,.2f}'.format
print(reduxDf.sort_values(by='tir'))

