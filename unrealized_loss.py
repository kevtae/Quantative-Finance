import pandas as pd
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt 

file_path = "SPY.csv"
data=OrderedDict()
data["SPY"] = pd.read_csv(file_path, index_col = 0, parse_dates=['Date'])

df= pd.DataFrame(columns = ['dr','av'])

#daily return = dr
daily_close = data['SPY']['Adj Close']
dr = daily_close.pct_change()
df['dr'] = round(dr*100,3)

#annualized Volatility = av
min_periods = 251
av = dr.rolling(min_periods).std()*np.sqrt(min_periods)
df['av'] = round(av*100,3)
print(df.loc['1/7/2002':'9/6/2019'].astype(str) + '%')


### Plot historgram of daily retrun
dr.hist(bins=250)
# #plot annualized volatility
# av.plot(figsize=(8,2))
# #plot Daily Close
# daily_close.plot(132)
plt.show()

spyShares = 889112600 
spyMarketValue = spyShares * data['SPY']['Adj Close'].loc['9/6/2019']
print("SPY shares:", spyShares)
print("SPY Market Value:",  spyMarketValue)

spyShares = 889112600 
date='9/6/2019'
spyMarketValue = spyShares * data['SPY']['Adj Close'].loc[date]

data['22_daily_volume'] = spyShares / (data['SPY']['Volume'].rolling(22).mean())
days_to_trade= np.ceil(data['22_daily_volume'].loc[date])
# print(days_to_trade)
print("Days to trade:", days_to_trade)

data['priVol'] = (data['SPY']["Adj Close"] * data['SPY']["Volume"]).rolling(int(days_to_trade)).sum()
VWAP = (data['priVol'])/(data['SPY']['Volume'].rolling(int(days_to_trade)).sum())
print("VMAP:", VWAP.loc[date])
unrealized_loss= (data['SPY']['Close'].loc[date]/VWAP)-1
print("Unrealized Gain/Loss:" , round(unrealized_loss.loc[date]*100,3).astype(str)+'%')
