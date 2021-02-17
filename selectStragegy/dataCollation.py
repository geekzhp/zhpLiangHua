# -*- coding: utf-8 -*-

import os

import pandas as pd
from datetime import datetime
from multiprocessing.pool import Pool

import zhpLiangHua.dataPath as path
from utils.file import readCsv,saveCsv
from utils.convert import transferPeriodData

'''
Created on 2021年2月6日

@author: Administrator

整理选股数据，最终形成一个hdf文件
'''

import utils.pandasSetting

isBingXing=True


periodType='M'      #选股周期,W为周期、M为月
allStockData=pd.DataFrame() # 用于存储数据



def concatStockData(csvFile):
    #csvFile='000010.XSHE.csv'
    print(csvFile)
    df=readCsv(os.path.join(path.SELECT,csvFile))
    
    df.drop_duplicates(subset=["date"],keep="last",inplace=True)
    
    df['daily_pct_change']=df['close']/df['open']-1   #开盘买入涨跌幅,为之后开盘买入做好准备
    
    #计算一字涨停，无法买入
    df['one_high_limit']=False
    df.loc[df['low']>=df['high_limit'],'one_high_limit']=True
    
    #计算开盘涨停
    df['open_high_limit']=False
    df.loc[df['open']>=df['high_limit'],'open_high_limit']=True
    
    # 计算下个交易的相关情况
    df['next_day_paused']=df['paused'].shift(-1)                            #下日是否交易
    df['next_day_open_high_limit']=df['open_high_limit'].shift(-1)          #下日_开盘涨停
    df['next_day_one_high_limit']=df['one_high_limit'].shift(-1)            #下日_一字涨停
    df['next_day_st']=df['name'].str.contains('ST').shift(-1)               #下日_是否ST
    df['next_day_delist']=df['name'].str.contains('退').shift(-1)            #下日_是否退市
    df['next_day_pct_change']=df['daily_pct_change'].shift(-1)        #下日_开盘买入涨跌幅
           
    df=transferPeriodData(df,periodType)
        
    # =对数据进行整理
    df.drop([0],axis=0,inplace=True)                                            # 删除上市的第一个周期,会有巨额的涨跌幅
    df=df[df['date']>pd.to_datetime('2006-12-25')]                              # 删除2007年之前的数据
    df['next_ervery_day_pct_change']=df['ervery_day_pct_change'].shift(-1)      # 计算下周期每天涨幅
    del df['ervery_day_pct_change']
    
    # =删除不能交易的周期数
    
    #对股票进行基本筛选
    df=df[df['name'].str.contains('ST')==False]              #删除月末为ST状态的周期数
    df=df[df['name'].str.contains('退')==False]               #删除月末有退市风险的股票
    df=df[df['paused']==0.0]                                 #删除月末不能交易的周期数
    df=df[df['trad_days']/df['exchange_trad_days']>=0.8]     #删除交易天数过少的周期数
    
    df.drop(['trad_days','exchange_trad_days'],axis=1,inplace=True)
    
    return df
    
    
# 标记开始时间
startTime = datetime.now()

#普通方式
# for csvFile in os.listdir(path.SELECT):
#     """
#     选股数据整理耗时:0:20:53.524423
#     """
#     print(csvFile)
#     
#     df=concatStockData(csvFile)
#     allStockData=allStockData.append(df,ignore_index=True)  #随着allStockData的增长，append的效率会越来越低

if __name__=="__main__":
    startTime = datetime.now()
    #并行加速的方式
    with Pool(processes=12) as pool:
        dfList=pool.map(concatStockData,sorted(os.listdir(path.SELECT)))
        print('读入完成, 开始合并', datetime.now() - startTime)
        # 合并为一个大的DataFrame
        allStockData = pd.concat(dfList, ignore_index=True)
        
    allStockData.sort_values(by=['date','code'],inplace=True)
    allStockData.reset_index(drop=True,inplace=True)
    
    allStockData.to_hdf('./data/allStockData4_'+periodType+'.h5','df',mode='w')
    
    print('选股数据整理耗时:{}'.format(datetime.now()-startTime))
