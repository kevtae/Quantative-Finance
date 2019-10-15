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

df= pd.DataFrame(columns = [
    'Ticker',
    'Portfolio_Weight', 
    'Annualized_Volatility', 
    'Beta', 
    'Average Drawdown',
    'Maximum Drawdown', 
    'Total Return', 
    'Annualized Total Return'
    ])


df['Ticker'] = [
    'AAPL',
    'ADBE',
    'AMZN',
    'CRM',
    'CS',
    'FB',
    'INTC',
    'GOOG',
    'IBM',
    'MSFT',
    'V']

list_of_df=[]
dates = '9/24/2019'

#getting the file
for i in range(len(files)):
    dataFrame = pd.read_csv(files[i],index_col=0, parse_dates=['Date'])
    list_of_df.append(dataFrame)

dfQQQ = OrderedDict()
dfQQQ['QQQ'] = pd.read_csv('QQQ.csv', index_col=0, parse_dates=['Date'])


#TotalPortfolioValue
totalPortfolioValue = 0
for i in range(len(df['Ticker'])):
    totalPortfolioValue = totalPortfolioValue + list_of_df[i]['Adj Close'].loc[dates]

#calculate portfolio weight
for i in range(len(df['Ticker'])):
    # stockValue = list_of_df[i]['Adj Close'].loc[dates]
    # weight = (stockValue/totalPortfolioValue)
    weight = 100/(len(df['Ticker']))
    df['Portfolio_Weight'][i] = round(weight,3) 

#annualized Volatility - need to double check
for i in range(len(df['Ticker'])):
    daily_close = list_of_df[i]['Adj Close']
    list_of_df[i]['dailyChange'] = daily_close.pct_change()
    list_of_df[i]['annualized_Volatility'] = pd.rolling_std(list_of_df[i]['dailyChange'], window=60) * np.sqrt(252)
    df['Annualized_Volatility'][i] = round(list_of_df[i]['annualized_Volatility'].loc[dates]*100,3).astype(str) + '%'


#beta
daily_close_QQQ = dfQQQ['QQQ']['Adj Close']
dfQQQ['QQQ']['dailyChange'] = daily_close_QQQ.pct_change()
year= 251
dfQQQ['QQQ']['variance'] = dfQQQ['QQQ']['dailyChange'].rolling(year).var()
for i in range(len(df['Ticker'])):
    list_of_df[i]['coVariance'] = dfQQQ['QQQ']['dailyChange'].rolling(year).cov(list_of_df[i]['dailyChange'].rolling(year))
    df['Beta'][i] = list_of_df[i]['coVariance'].loc[dates]/dfQQQ['QQQ']['variance'].loc[dates]

#Max Drawdown
#is it Adj close or just close?
for i in range(len(df['Ticker'])):
    list_of_df[i]['low'] = list_of_df[i]['Adj Close'].rolling(year).min()
    list_of_df[i]['high'] = list_of_df[i]['Adj Close'].rolling(year).max()
    list_of_df[i]['maxDrawdown'] = (list_of_df[i]['high']-list_of_df[i]['low'])/list_of_df[i]['high']
    df['Maximum Drawdown'][i] = list_of_df[i]['maxDrawdown'].loc[dates]
    

#printing maxDrawdown
# list_of_df[0]['maxDrawdown'].plot()
# plt.show()

#Average Drawdown - taking average of all max drawdown
for i in range(len(df['Ticker'])):
    list_of_df[i]['averageDrawdown'] = list_of_df[i]['maxDrawdown'].rolling(year).mean()
    df['Average Drawdown'][i] = list_of_df[i]['averageDrawdown'].loc[dates]
    
initialDate = '1/4/2010'
endingDate = '9/24/2019'
#totalReturn without dividend
#facebook starts from year 2012
#Adj Close?
#stock split?
for i in range(len(df['Ticker'])):
    initialPrice = list_of_df[i]['Adj Close'].iloc[0]
    endingPrice = list_of_df[i]['Adj Close'].loc[endingDate]
    list_of_df[i]['Total Return']= ((endingPrice - initialPrice)/(initialPrice))
    df['Total Return'][i] = round((list_of_df[i]['Total Return'].loc[dates])*100,3).astype(str) + '%'

#annualzied return
#compound it?
for i in range(len(df['Ticker'])):
    df['Annualized Total Return'][i]  = round(((1 + list_of_df[i]['Total Return'][i])**(365/list_of_df[i].shape[0])-1)*100,3).astype(str) + '%'
    

print(df)



    
