import jqdatasdk as jq
import pandas as pd
import numpy as np
import datetime

from jqdatasdk import query,finance
'''
Created on 2020年12月24日

@author: My
'''

jq.auth('18009020072','4187Xslc61')
"""
#data=jq.get_price('000001.XSHE',start_date='2015-01-01',end_date='2015-02-01',fq='pre')
#print(data)

q=jq.query(jq.finance.SW1_DAILY_PRICE).filter(
    jq.finance.SW1_DAILY_PRICE.code=='801010',
    jq.finance.SW1_DAILY_PRICE.date>'20200819').order_by(
        jq.finance.SW1_DAILY_PRICE.date.desc())
df=jq.finance.run_query(q)
print(df)
df.to_csv('农林牧渔_申万一级02.csv',encoding='gbk')

jq.logout()"""


'''df1=pd.read_csv(
    filepath_or_buffer='./data/农林牧渔_申万一级01.csv',
    encoding='gbk',
    sep=',',
    #skiprows=1,
    #nrows=10,
    index_col=['date'],
    #usecols=[],
    error_bad_lines=False,
    #no_value='NULL',
    )

df2=pd.read_csv(
    filepath_or_buffer='./data/农林牧渔_申万一级02.csv',
    encoding='gbk',
    sep=',',
    #skiprows=1,
    #nrows=10,
    index_col=['date'],
    #usecols=[],
    error_bad_lines=False,
    #no_value='NULL',
    )

df1.sort_index(ascending=False,inplace=True)
df1=df1.drop(df1.columns[0:2],axis=1)
df2=df2.drop(df2.columns[0:2],axis=1)


df3=pd.concat([df2,df1])

df3.to_csv('./data/农林牧渔_申万一级.csv',encoding='gbk')

'''

#统计函数
#df=pd.read_csv('./data/农林牧渔_申万一级.csv',encoding='gbk')
#均值
'''print(df['open'].mean())
print(df[['open','close']].mean())
print(df[['open','close']].mean(axis=1))  #两列的均值'''

'''print(df['open'].max())
print(df['open'].min())
print(df['open'].std())
print(df['open'].count())
print(df['open'].median())
print(df['open'].quantile(0.25))  #分位数'''


#shift类函数、删除列的方式
'''df['pre_close']=df['close'].shift(-1)
df['change']=df['close'].diff(-1)
#print(df[['date','close','pre_close']])
df['change_pct2']=df['change']/df['pre_close']*100
df['change_pct3']=df['close'].pct_change(-1)*100
print(df[['close','pre_close','change_pct','change_pct2','change_pct3']])'''

#cum(cumulative)函数
'''df['vol_cum']=df['volume'].cumsum()
print(df[['volume','vol_cum']])
df['资金曲线']=(df['change_pct']/100+1).cumprod()    #cumprod()累乘
print(df)'''


#其它列函数
#df['close_rank']=df['close'].rank(ascending=True,pct=False)    #输出排名
#print(df[['close','close_rank']])
#print(df['code'].value_counts())    #统计该列中每个元素出现的次数

#条件筛选
#print(df['code']==801010)
#print(df[df['code']==801010])  #判断为True输出
#print(df[df['code'].isin([801010,801011])])
#print(df[df['close']>1500])
#print(df[(df.date>='2020-07-15') & (df.date<='2020-08-01')])

#缺失值的处理
'''print(df.dropna(how='any'))
print(df.dropna(subset=['open','close'],how='all'))

df.fillna(value='xx')
df.fillna(value=df['open'])
df.fillna(method='ffill')   #向上寻找最近一个非空值，填充
df.fillna(method='bfill')   #向下寻找最近一个非空值，填充

df.notnull()
df.isnull()
df[df['open'].notnull()]'''

#排序函数
'''df.reset_index()
df.sort_values(by=['open'],ascending=True)
df.sort_values(by=['open','close'],ascending=[True,True])'''

#上下合并
"""df1=df.iloc[0:10][['open','close','high','low']]
df2=df.iloc[5:20][['open','close','high','low']]
df3=df1.append(df2,ignore_index=True)"""

#对数据进行去重
#print(df3)
'''df3.drop_duplicates(
    subset=['open','close'],
    keep='last',    #参数last、first、False
    inplace=True)
print(df3)'''

#其它常用的重要函数
"""print(df.rename(columns={'date':'日期'}))
df.empty
df.T"""


#字符串处理
#print(df['name'])
#print(df['name'].str[:2])  #.str.upper()  .str.lower() .str.len()
#print(df['name'].str.len())
#print(df['name'].str.strip())
#print(df['name'].str.contains('sz'))
#print(df['name'].str.replace('农','nong'))
#print(df['name'].str.split('林'))
#print(df['name'].str.split('林').str[1])
#print(df['name'].str.split('林',expand=True))    #分割后将数据分列


"""jq.auth('18009020072','4187Xslc61')
stock='002648.XSHE'

df=jq.get_price(
    stock,
    start_date='2020-01-01',
    end_date=datetime.datetime.today(),
    frequency='daily',
    fq=None,
    fields=['open','close','high','low','volume','money','factor','high_limit','low_limit','avg','pre_close','paused']
    )
df.sort_index(ascending=False,inplace=True)
df['date']=df.index

df.to_csv('./data/日行情_卫星石化_未复权.csv',encoding='gbk')
jq.logout()


df=pd.read_csv('./data/日行情_卫星石化.csv',encoding='gbk')
print(df)"""

#时间处理
"""df=pd.read_csv('./data/日行情_卫星石化_tushare.csv',
               encoding='gbk',
               dtype={'date':str}
               )
df['date']=pd.to_datetime(df['date'])   #将字符串转为日期格式
print(df)
print(df.iloc[0]['date'])

print(df['date'].dt.year)
print(df['date'].dt.week)   #month、dayofyear、dayofweek、weekday_name、dyas_in_month、is_month_start、is_month_end
print(df['date'].dt.weekday_name)

print(df['date']+pd.Timedelta(days=1))
print(df['date']+pd.Timedelta(days=1)-df['date'])"""

#rolling、expanding操作
#rolling计算当天算，最近N天的相关数值
#print(df)
"""df['ma_5']=df['close'].rolling(5).mean()    #mean()、max()、min()、std()
df['ma_5_max']=df['close'].rolling(5).max()
df.fillna(value=df['close'],inplace=True)
print(df)

#expanding 从头至今的数据，后面可以接各种计算类函数
df['close_至今均值']=df['close'].expanding().mean()
print(df)"""

df=jq.get_price('300001.XSHE',
                start_date='2009-10-30',
                end_date='2016-12-14',
                frequency='daily',
                fq=None,
                fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close'])
print(df.sort_index(ascending=False,inplace=True))
df.to_csv('./data/日行情_特锐德_未复权_jqdata.csv',encoding='gbk')

jq.logout()