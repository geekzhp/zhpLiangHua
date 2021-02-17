import os
import datetime
import pandas as pd
import numpy as np
import time

from jqdatasdk import (
    auth,
    is_auth,
    get_query_count,
    api as jqapi,
    logout)

from utils.path import (
    mkdirs)


def getMinPriceHs300(frequence='60m'):
    passwd=pd.DataFrame({'host':['jqdatasdk',],
                         #'username':['18009020072',],
                         'username':['18090679978',],
                         'passwd':['4187Xslc61',]},
                         columns=['host','username','passwd'])
    
    
    print(passwd)
    auth(passwd['username'][0],passwd['passwd'][0])
    
    print(get_query_count())
    
    #frequence='60min'
    #创建下载目录
    stockPath=mkdirs(os.path.join(mkdirs('datastore'),'kline','stock',frequence))
    print(stockPath)
    
    #for year in range(2017,2005,-1):
    #for year in range(2020,2005,-1):
    for year in range(2021,2020,-1):
        lastQueryCount=get_query_count()
        if lastQueryCount['spare']<1280:
            print('从jqdata查询数据已经不足，退出查询抓取...')
            break
              
        #获取当年的沪深300成分股代码，存放在stockLists列表中
#         stockLists=[]
#         for month in range (1,12):
#             indexDate='{}-{}-01'.format(year,month)
#             #print(indexDate)
#             
#             #获取特定日期截面的所有沪深300的股票成分
#             stockList=jqapi.get_index_stocks('000300.XSHG',date=indexDate)
#             time.sleep(0.2)
#             stockLists=stockLists+stockList
        
        #去除重复股票代码
#         stockLists=list(set(stockLists))
#         print('{}年 沪深300指数 一共有成分股:{}个'.format(year,len(stockLists)),stockLists)
        
        stockLists=jqapi.get_all_securities(['stock']).index.to_list()
        
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        for asset in stockLists:
            if lastQueryCount['spare']<1280:
                print('从jqdata查询数据已经不足，退出查询抓取...')
                break
            
            print(asset,startDate,endDate)
            stockFile=os.path.join(stockPath,'{}_{}_{}.csv'.format(asset,startDate,endDate))
            
            if os.path.isfile(stockFile):
                print('文件已经存在，跳过',stockFile)
                continue
            
            try:
                print(stockFile)
                his=jqapi.get_price(asset,
                                    startDate,
                                    endDate,
                                    frequency=frequence)
                
                his['date']=his.index
                his.reset_index(level=0,drop=True,inplace=True)
                
                his.to_csv(stockFile,
                           index=None)
            except Exception as e:
                lastQueryCount=get_query_count()
                print(asset,lastQueryCount,e)
                
            time.sleep(1)
                
    logout()

def getPrice():
    auth('18090679978','4187Xslc61')
    
    df = jqapi.get_price('000001.XSHE', start_date='2015-01-01', end_date='2015-01-06', frequency='daily')
    
    print(df)
    
    logout()

if __name__=="__main__":
    getMinPriceHs300('60m')