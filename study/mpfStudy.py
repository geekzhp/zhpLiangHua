import mplfinance as mpf
import pandas_datareader as web
from datetime import datetime



print(mpf.__version__)

symbol='SPY'    #标普500 ETF
start=datetime(2020,1,1)
end=datetime(2020,12,31)

df=web.DataReader(symbol,data_source='yahoo',start=start,end=end)
df.info()

"""import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.grid()

plt.title(symbol)
plt.plot(df['Close'])

plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)

plt.show()"""

#mpf.plot(df)
#mpf.plot(df,type='candle')
#mpf.plot(df,type='pnf')

#mpf.plot(df,type='candle',style='yahoo')
#mpf.plot(df,type='candle',style='yahoo',volume=True)

"""mpf.plot(df,type='candle',
         style='yahoo',
         volume=True,
         mav=(20,60,120),
         figratio=(16,8),
         title='SPY',
         ylabel="price")
"""

my_color=mpf.make_marketcolors(
    up='red',
    down='green',
    edge='inherit')

my_style=mpf.make_mpf_style(marketcolors=my_color)

df['ma20']=df['Close'].rolling(20).mean()
df['ma20'].fillna(df['Close'].expanding().mean())

add_plot=[mpf.make_addplot(df['ma20'])]

mpf.plot(df,type='candle',
         style=my_style,
         volume=True,
         addplot=add_plot,
         ylabel='price',
         ylabel_lower='volume',
         savefig='spy_2020.png' )