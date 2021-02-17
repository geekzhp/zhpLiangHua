import pandas as pd
#当列太多时，显示不换行
pd.set_option('expand_frame_repr',False)
#显示所有的列
pd.set_option('display.max_columns', None)
'''
Created on 2020年12月31日

@author: My
'''

df=pd.read_csv('./data/日行情_特锐德_未复权_jqdata.csv',
               encoding='gbk'
               )


df.rename(columns={'Unnamed: 0':'date'},inplace=True)
df['date']=pd.to_datetime(df['date'])
df['pct_chg']=(df['close']-df['pre_close'])/df['pre_close']

df.sort_values(by='date',inplace=True)

df['factor']=(df['pct_chg']+1).cumprod()
df['factor']=df['factor']/df.iloc[-1]['factor']
#print(df)

"""init_price_pre=df.iloc[-1]['close']/df.iloc[-1]['factor']
print(init_price_pre)
df['close_pre']=init_price_pre*df['factor']
df['open_pre']=df['open']*df['close_pre']/df['close']
df['high_pre']=df['high']*df['close_pre']/df['close']
df['low_pre']=df['low']*df['close_pre']/df['close']"""

df['close_pre']=df['close']*df['factor']
df['open_pre']=df['open']*df['factor']
df['high_pre']=df['close']*df['factor']
df['low_pre']=df['low']*df['factor']
print(df)


