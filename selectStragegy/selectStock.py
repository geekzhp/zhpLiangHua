# -*- coding: utf-8 -*-

import os

import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from multiprocessing.pool import Pool

import zhpLiangHua.dataPath as path
from utils.file import readCsv,saveCsv
from utils.convert import transferPeriodData
from asyncio.tasks import sleep
from unittest.mock import inplace

import utils.pandasSetting
pd.set_option('display.max_rows', 500)  # 最多显示数据的行数
'''
Created on 2021年2月6日

@author: Administrator
'''

#参数设定
selectStockNum=3    #选个股数量，取决于资金量，资金量多可以多选一些
cRate=1.5/10000     #手续费
tRate=1/1000        #印花税，卖出股票时交，交给国家的

#导入数据
df=pd.read_hdf('./data/allStockData4_M.h5','df')
df.dropna(subset=['next_ervery_day_pct_change'],inplace=True)   #下周期没有数据的删除，最近的数据


#选股
# 删除下个交易日不交易、开盘涨停的股票，因为这些股票在下个交易日开盘时不能买入。
df=df[df['next_day_paused']==0]
df=df[df['next_day_open_high_limit']==False]
df=df[df['next_day_one_high_limit']==False]
df=df[df['next_day_st']==False]
df=df[df['next_day_delist']==False]

# 计算选股因子，根据选股因子对股票进行排名
#df['rank']=df.groupby('date')['total_mv'].rank()           #小市值
#df['rank']=df.groupby('date')['pct_change'].rank()          #周期跌幅最大  
#df['rank']=df.groupby('date')['pct_change'].rank(ascending = False)          #周期跌幅最大 

#df['rank']=df.groupby('date')['trunover'].rank()          #周期换手率最小
#df['rank']=df.groupby('date')['trunover'].rank(ascending = False)          #周期换手率最大

#df['rank']=df.groupby('date')['ampitude_20_1'].rank()          #振幅1最小
#df['rank']=df.groupby('date')['ampitude_20_1'].rank(ascending = False)          #振幅1最大

df['rank']=df.groupby('date')['ampitude_20_2'].rank()          #振幅1最大
#df['rank']=df.groupby('date')['ampitude_20_2'].rank(ascending = False)          #振幅1最大


df=df[df['rank']<=selectStockNum]

#print(df.groupby('date')['total_mv'].rank())

#print(df.head(6))

# 按照开盘买入的方式，修正选中股票在下周期每天的涨跌幅。
# 即将下周期每天的涨跌幅中第一天的涨跌幅，改成由开盘买入的涨跌幅
df['next_day_pct_change']=df['next_day_pct_change'].apply(lambda x:[x])
df['next_ervery_day_pct_change']=df['next_ervery_day_pct_change'].apply(lambda x:x[1:])
df['next_ervery_day_pct_change']=df['next_day_pct_change']+df['next_ervery_day_pct_change']

#del df['next_day_pct_change']


#整理选中股票数据
df['name']+=' '
df['code']+=' '

grouped=df.groupby('date')

selectStock=pd.DataFrame()
selectStock['buy_stock_code']=grouped['code'].sum()
selectStock['buy_stock_name']=grouped['name'].sum()

#print(df)

#计算下周期每天的资金曲线,选股下周期每天资金曲线
# selectStock['next_ervery_day_equity_curve']=grouped['next_ervery_day_pct_change'].apply(
#      lambda x: np.cumprod(np.array(list(x))+1, axis=1).mean(axis=0))

#TypeError: can only concatenate list (not "int") to list

def f(x):
    try:
        ret=np.cumprod( np.array(list(x))+1  ,axis=1).mean(axis=0)
    except Exception as e:
        print(e)
        print(list(x))
        return None
    
    return ret

for name,group in grouped: 
    x=group['next_ervery_day_pct_change']
    
    try:
        np.cumprod( np.array(list(x))+1  ,axis=1).mean(axis=0)
    except Exception as e:
        print(e)
        print(np.array(list(x)))
        print(x.apply(lambda z:len(z)))
        #print( list(group.loc[22146][['code','name','next_ervery_day_pct_change']]) )
#     print(name)
#     try:
# #         print(group['next_ervery_day_pct_change'].apply(
# #          lambda x: np.cumprod( np.array(list(x))+1  ,axis=1).mean(axis=0) ) )
#         print(f(group['next_ervery_day_pct_change']))
#     except Exception as e:
#         print('error:')
#         x=group['next_ervery_day_pct_change']
#         print(x)
#         #print(np.array(list(x)+1))
#         print( f(x))
#         break

print('no error')
exit()
# x=df.iloc[:3]['next_ervery_day_pct_change']
# print(x)
# print(list(x))  # 将x变成list
# 
# print(np.array(list(x)))  # 矩阵化
# exit()
#print(np.array(list(x)) + 1)  # 矩阵中所有元素+1
#print(np.cumprod(np.array(list(x)) + 1, axis=1))  # 连乘，计算资金曲线 每个股票的资金曲线，每个周期开盘买入1元，最后一天变成了多少钱
#print(np.cumprod(np.array(list(x)) + 1, axis=1).mean(axis=0))  # 连乘，计算资金曲线，选中的三支股票作为整体的资金曲线，及三个股票的均值

#print(selectStock)

# 扣除买入手续费
selectStock['next_ervery_day_equity_curve']=selectStock['next_ervery_day_equity_curve']*(1-cRate)   #计算有不精准的地方

# 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费
selectStock['next_ervery_day_equity_curve'] = selectStock['next_ervery_day_equity_curve'].apply(
    lambda x: list(x[:-1]) + [x[-1] * (1 - cRate - tRate)])

# 计算下周期整体涨跌幅
selectStock['next_pct_change']=selectStock['next_ervery_day_equity_curve'].apply(lambda x: x[-1]-1)

# 计算下周期每天的涨跌幅
selectStock['next_every_day_pct_change'] = selectStock['next_ervery_day_equity_curve'].apply(
    lambda x: list(pd.DataFrame([1] + x).pct_change()[0].iloc[1:]))
#print(selectStock)

del selectStock['next_ervery_day_equity_curve']

# 计算整体资金曲线
selectStock.reset_index(inplace=True)   #设置前的index为date
selectStock['equity_curve']=(selectStock['next_pct_change']+1).cumprod()

#print(selectStock)

# ===计算选中股票每天的资金曲线
indexData=readCsv(os.path.join(path.INDEX_PRICE,'000001.XSHG.csv'))
indexData['index_pct_change']=indexData['close']/indexData['pre_close']-1.0
indexData=indexData[['date','index_pct_change']]
indexData.sort_values(by=['date'],inplace=True)
indexData.reset_index(drop=True,inplace=True)
#print(indexData)

equity=pd.merge(
    left=indexData,
    right=selectStock[['date','buy_stock_code']],
    on=['date'],
    how='left',
    sort=True)

equity['hold_stock_code']=equity['buy_stock_code'].shift()
equity['hold_stock_code'].fillna(method='ffill',inplace=True)
equity.dropna(subset=['hold_stock_code'],inplace=True)
del equity['buy_stock_code']

equity['pct_change']=selectStock['next_every_day_pct_change'].sum()
equity['equity_curve']=(equity['pct_change']+1).cumprod()
equity['benchmark'] = (equity['index_pct_change'] + 1).cumprod()

print(equity.tail(100))

# ===画图
equity.set_index('date', inplace=True)
plt.plot(equity['equity_curve'])
plt.plot(equity['benchmark'])
plt.legend(loc='best')
plt.show()