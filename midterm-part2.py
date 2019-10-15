import pandas as pd
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt

files = ['AAPL.csv',
    'ADBE.csv',
    'AMZN.csv',
    'CRM.csv',
    'CS.csv',
    'FB.csv',
    'INTC.csv',
    'GOOG.csv',
    'IBM.csv',
    'MSFT.csv',
    'V.csv']

#ETF ticker
dfETF= pd.DataFrame(columns = [
    'Ticker',
    'Correlation',
    'Covariance',
    'Tracking Error',
    'Sharpe Ratio',
    'Annualized Volatility'
    ])

dfETF['Ticker'] = [
    'QQQ',
    'IYW'
]

list_of_df=[]
list_of_etf=[]
dates = '9/24/2019'

#getting the file
for i in range(len(files)):
    dataFrame = pd.read_csv(files[i],index_col=0, parse_dates=['Date'])
    list_of_df.append(dataFrame)


QQQ = pd.read_csv('QQQ.csv', index_col=0, parse_dates=['Date'])
list_of_etf.append(QQQ)
IYW = pd.read_csv('IYW.csv', index_col=0, parse_dates=['Date'])
list_of_etf.append(IYW)

df = pd.DataFrame()



#getting the Portfolio Return
for i in range(len(files)):
    daily_close = list_of_df[i]['Adj Close']
    df[i] = daily_close.pct_change()

df['portfolioReturn'] = df.mean(axis=1) #average of all the stocks daily portfolio return

# #Covariance of 1 year period
# year = 252
# for i in range(len(list_of_etf)):
#     daily_close = list_of_etf[i]['Adj Close']
#     list_of_etf[i]['dailyChange'] = daily_close.pct_change()
#     list_of_etf[i]['coVariance'] = list_of_etf[i]['dailyChange'].cov(df['portfolioReturn'], min_periods=year)
#     dfETF['Covariance'][i]= (list_of_etf[i]['coVariance'].loc[dates])*100

# #correlation = covariance(a,b)/(std.dev.A * std.dev.B)
#correlation of one year
# for i in range(len(list_of_etf)):
#     list_of_etf[i]['correlation'] = dfETF['Covariance'][i]/(df['portfolioReturn'].rolling(year).std()*list_of_etf[i]['dailyChange'].rolling(year).std())
#     dfETF['Correlation'][i] = list_of_etf[i]['correlation'].loc[dates]

#Covariance
for i in range(len(list_of_etf)):
    daily_close = list_of_etf[i]['Adj Close']
    list_of_etf[i]['dailyChange'] = daily_close.pct_change()
    list_of_etf[i]['coVariance'] = list_of_etf[i]['dailyChange'].cov(df['portfolioReturn'])
    dfETF['Covariance'][i]= (list_of_etf[i]['coVariance'].loc[dates])*100

#correlation = covariance(a,b)/(std.dev.A * std.dev.B)
for i in range(len(list_of_etf)):
    list_of_etf[i]['correlation'] = dfETF['Covariance'][i]/(df['portfolioReturn'].std()*list_of_etf[i]['dailyChange'].std())
    dfETF['Correlation'][i] = list_of_etf[i]['correlation'].loc[dates]

# double checking correlation
# for i in range(len(list_of_etf)):
#     list_of_etf[i]['corr'] = df['portfolioReturn'].corr(list_of_etf[i]['dailyChange'])
#     dfETF['corr'][i] = list_of_etf[i]['corr'].loc[dates]

year = 252
#trackingError =  Standard Deviation of (P - B)
for i in range(len(list_of_etf)):
    list_of_etf[i]['difference'] = (df['portfolioReturn'])-(list_of_etf[i]['dailyChange'])
    list_of_etf[i]['trackingError'] = list_of_etf[i]['difference'].std()
    dfETF['Tracking Error'][i] = list_of_etf[i]['trackingError'].loc[dates]*100



# #sharpe ratio of ETF? Portfolio?
# for i in range(len(list_of_etf)):
#     list_of_etf[i]['riskFree'] = df.apply(lambda x: 2, axis=1)
#     list_of_etf[i]['rx-rf'] = (list_of_etf[i]['dailyChange']*100)-(list_of_etf[i]['riskFree'])
#     average = list_of_etf[i]['rx-rf'].mean()
#     std = (list_of_etf[i]['dailyChange']*100).std()
#     dfETF['Sharpe Ratio'][i]= average/std

for i in range(len(list_of_etf)):
    list_of_etf[i]['riskFree'] = df.apply(lambda x: 2, axis=1)
    returns_annual = list_of_etf[i]['dailyChange'].mean()*250
    cov_daily = list_of_etf[i]['dailyChange'].cov(list_of_etf[i]['dailyChange'])
    cov_annual = cov_daily * 250
    returns = returns_annual - .02
    volatility = np.sqrt(cov_annual)
    sharpe = returns/volatility
    dfETF['Sharpe Ratio'][i] = sharpe


#annualized volatiliy
for i in range(len(list_of_etf)):
     list_of_etf[i]['Annualized Volatility'] = pd.rolling_std(list_of_etf[i]['dailyChange'], window=252) * np.sqrt(252)
     df['portfolioVolatility'] = pd.rolling_std(df['portfolioReturn'], window=252) * np.sqrt(252)
     list_of_etf[i]['Annualized Volatility Spread'] = df['portfolioVolatility'] - list_of_etf[i]['Annualized Volatility']
     dfETF['Annualized Volatility'][i]  = list_of_etf[i]['Annualized Volatility Spread'].loc[dates]*100



print(dfETF)
