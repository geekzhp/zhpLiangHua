import tushare as ts

import pandas as pd


pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
#pd.set_option('display.max_rows', 500)  # 最多显示数据的行数 
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.4f' % x) #不显示科学计数法
'''
Created on 2020年12月24日

@author: My
'''


ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')
pro=ts.pro_api()






df=pd.read_csv('./data/daily/stock/tmp/sz300001.csv',encoding='gbk')

#df.columns=[i.encode('utf8').decode('utf8') for i in df.columns]
#rename={'交易日期 ':'date','股票代码':'code','开盘价':'open','最高价':'high','最低价':'low','收盘价':'close','涨跌幅':'pct_change'}
rename={df.columns[2]:'date','股票代码':'code','开盘价':'open','最高价':'high','最低价':'low','收盘价':'close','涨跌幅':'pct_change'}
df.rename(columns=rename,inplace=True)
df=df[[col for _,col in rename.items()]]
df['date']=pd.to_datetime(df['date'])
#print(df)




df=calAdjustPrice(df, adjType='post')
df=signalMa(df)
df=position(df)

#上市一年之后的交易日
df=df.iloc[250-1:]
#将第一天的仓位设置为0
#df.iloc[0]['pos']=0
df.iloc[0,-1]=0

df=calcuEquityCurve(df)
print(df)
exit()

#print(df.loc[df['signal'].isin([0,1])])
#print(df[(df['date']>'2009-10-17') & (df['date']>'2009-12-31' )])





#print(df)





print(df[df['date']>pd.to_datetime('2015-06-15')])
#print(df)
print(df[['commission','tax']].sum())
        