import pandas as pd
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import os


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
    'V.csv',
    'QQQ.csv',
    'IYW.csv']

df= pd.DataFrame()
df_portfolio = pd.DataFrame()

list_of_df=[]



for i in range(len(files)):
    dataFrame = pd.read_csv(files[i],index_col=0, parse_dates=['Date'])
    list_of_df.append(dataFrame)

for i in range(len(files)):
    daily_close = list_of_df[i]['Adj Close']
    df[i] = daily_close.pct_change()

df.columns = df.columns.map(str)

df.rename(columns={
    "0": "AAPL",
    "1": "ADBE",
    "2": "AMZN",
    "3": "CRM",
    "4": "CS",
    "5": "FB",
    "6": "INTC",
    "7": "GOOG",
    "8": "IBM",
    "9": "MSFT",
    "10": "V",
    "11":"QQQ",
    "12": "IYW",
    }, inplace= True)

df_portfolio = df
df_portfolio = df_portfolio.drop(["QQQ","IYW"], axis=1)
df["portfolio"] = df_portfolio.mean(axis=1)

df_corr = df.corr()

print(df_corr)

#efficeint frontier
#https://github.com/PyDataBlog/Python-for-Data-Science/blob/master/Tutorials/Efficient%20Frontier%20with%20Quandl%20(Part%201).py


returns_daily = df_portfolio
returns_annual = returns_daily.mean() * 250

cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250


port_returns = []
port_volatility = []
stock_weights = []
sharpe_ratio = []

num_assets = len(df_portfolio.columns)
num_portfolios = 50000

np.random.seed(101)

for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)-.02
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
            'Sharpe Ratio': sharpe_ratio}

# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter,symbol in enumerate(df_portfolio.columns):
    portfolio[symbol+' weight'] = [weight[counter] for weight in stock_weights]

# make a nice dataframe of the extended dictionary
df1 = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' weight' for stock in df_portfolio.columns]

# reorder dataframe columns
df1 = df1[column_order]

min_volatility = df1['Volatility'].min()
max_sharpe = df1['Sharpe Ratio'].max()

# use the min, max values to locate and create the two special portfolios
sharpe_portfolio = df1.loc[df1['Sharpe Ratio'] == max_sharpe]
min_variance_port = df1.loc[df1['Volatility'] == min_volatility]

# plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df1.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

df2 = pd.DataFrame(columns = [
    'Ticker',
    'max sharpe weight',
    'min volatility weight'
])

df2['Ticker'] = [
    'AAPL.csv',
    'ADBE.csv',
    'AMZN.csv',
    'CRM.csv',
    'CS.csv',
    'FB.csv',
    'INTC.csv',
    'GOOG.csv',
    'IBM.csv',
    'MSFT.csv',
    'V.csv'
]

df2['max sharpe weight'] = [
        0.136660,
        0.093803,
        0.143156,
        0.004844,
        0.001342,
        0.184358,
        0.020959,
        0.014450,
        0.008951,
        0.119634,
        0.271843
]

df2['min volatility weight'] = [
        0.047330,
        0.042732,
        0.009631,
        0.009189,
        0.027498,
        0.019463,
        0.155342,
        0.160499,
        0.259192,
        0.079642,
        0.189482
]

print(df2)