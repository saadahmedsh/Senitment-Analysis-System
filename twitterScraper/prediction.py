from datetime import date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from pandas.tseries.offsets import DateOffset
import statsmodels.api as sm
from .models import *


def adfuller_test(Polarity):
    result=adfuller(Polarity)
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")



def prediction_module(polarity, dates):
    df_pred=pd.DataFrame()
    df_pred['Day']=dates
    df_pred['Polarity']=polarity
    df_pred['Day']=pd.to_datetime(df_pred['Day'])
    df_pred.set_index('Day',inplace=True)

    adfuller_test(df_pred['Polarity'])
    df_pred['Polarity First Difference'] = df_pred['Polarity'] - df_pred['Polarity'].shift(1)
    df_pred['Polarity'].shift(1)
    df_pred['Seasonal First Difference']=df_pred['Polarity']-df_pred['Polarity'].shift(1)

    adfuller_test(df_pred['Seasonal First Difference'].dropna())

    model=sm.tsa.arima.ARIMA(df_pred['Polarity'],order=(1,1,1))
    model_fit=model.fit()

    forcasted=model_fit.predict(start=8,end=14,dynamic=True).to_frame()

    forcasted_arr=np.array(forcasted)
    future_dates=[df_pred.index[-1]+ DateOffset(days=x)for x in range(0,24)]
    dates=[]
    for i in range(1, 8):
        dates.append(str(future_dates[i].date().year) + '-' + str(future_dates[i].date().month) + '-' + str(future_dates[i].date().day))

    return forcasted_arr, dates



