import tushare as ts

import pandas as pd

#当列太多时，显示不换行
pd.set_option('expand_frame_repr',False)
#显示所有的列
pd.set_option('display.max_columns', None)
'''
Created on 2020年12月24日

@author: My
'''


ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')

pro=ts.pro_api()
#data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

"""stock='300001.SZ'
df=pro.daily(ts_code=stock,
             start_date='20091001',
             end_date='20161214')
df.rename(columns={'trade_date':'date'},inplace=True)
print(df)
df.to_csv('./data/日行情_特锐德_tushare.csv',
          encoding='gbk',
          index=False)"""
          
df=pd.read_csv('./data/日行情_特锐德_tushare.csv',encoding='gbk')
df.sort_values(by=['date',],inplace=True)
df['pct_chg']=df['pct_chg']/100.0

df['pct_chg_2']=df['close'].pct_change()
print(df[abs(df['pct_chg_2']-df['pct_chg'])>0.0001])

del df['pct_chg_2']

df['factor']=(df['pct_chg']+1).cumprod()
#print(df)
initi_price=df.iloc[0]['close']/df['factor'].iloc[0]
#print(initi_price)
df['close_post']=initi_price*df['factor']
#print(df)

initi_price_pre=df.iloc[-1]['close']/df['factor'].iloc[-1]
df['close_pre']=initi_price_pre*df['factor']
#print(df)

#df.sort_values(by=['date'],inplace=True)

print(df)

          