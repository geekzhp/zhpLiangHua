import os
import datetime
import pandas as pd
import numpy as np
import time

from jqdatasdk import (auth,
                       is_auth,
                       get_query_count,
                       query,
                       finance,
                       logout,
                       api as jqapi,)

def initiExchangeTradInfo():
    password=pd.DataFrame({'host':['jqdatasdk'],
                           'username':['18009020072'],
                           'password':['4187Xslc61']},
                           columns=['host','username','password'])
    
    auth(password['username'][0],password['password'][0])
    is_auth=is_auth()
    
    lastQueryCount=get_query_count()  #{'total': 10000000, 'spare': 17485426}
    if lastQueryCount['spare']<=5000:
        print('剩余查询条数已经不足，退出行情查询抓取...')
    else:
        startDate='2005-01-01'
        q=query(finance.STK_EXCHANGE_TRADE_INFO).filter(finance.STK_EXCHANGE_TRADE_INFO.date>=startDate)
        df=finance.run_query(q)
        #df['date']=pd.to_datetime(df['date'])
        
        while lastQueryCount['spare']>5000:
            print(df.iloc[-1]['date'])
            q=query(finance.STK_EXCHANGE_TRADE_INFO).filter(
                finance.STK_EXCHANGE_TRADE_INFO.date>=df.iloc[-1]['date'])
            newDf=finance.run_query(q)
            #newDf['date']=newDf.to_datetime(df['date'])
            
            df=pd.concat([df,newDf],ignore_index=True)
            if newDf.empty or newDf.iloc[-1]['date']==datetime.date(2021,1,14):
                break
            
            lastQueryCount=get_query_count()
        #print(df)
    
    df.to_csv('./data/exchangeTradInfo/exchangeTradInfo.csv',
              encoding='gbk',
              index=None)
              
    logout()
    
def initiLgtChengJiao():
    password=pd.DataFrame({'host':['jqdatasdk'],
                           'username':['18009020072'],
                           'password':['4187Xslc61']},
                           columns=['host','username','password'])
    
    auth(password['username'][0],password['password'][0])
    
    lastQueryCount=get_query_count()  #{'total': 10000000, 'spare': 17485426}
    if lastQueryCount['spare']<=5000:
        print('剩余查询条数已经不足，退出行情查询抓取...')
    else:
        startDate='2005-01-01'
        q=query(finance.STK_ML_QUOTA).filter(finance.STK_ML_QUOTA.day>='2014-11-7')
        df=finance.run_query(q)
        #df['date']=pd.to_datetime(df['date'])
        
        while lastQueryCount['spare']>5000:
            print(df.iloc[-1]['day'])
            q=query(finance.STK_ML_QUOTA).filter(
                finance.STK_ML_QUOTA.day>=df.iloc[-1]['day'])
            newDf=finance.run_query(q)
            #newDf['date']=newDf.to_datetime(df['date'])
            
            df=pd.concat([df,newDf],ignore_index=True)
            if newDf.empty or newDf.iloc[-1]['day']==datetime.date(2015,4,17):
                break
            
            lastQueryCount=get_query_count()
        #print(df)
    
    df.to_csv('./data/exchangeTradInfo/陆股通成交和额度信息.csv',
              encoding='gbk',
              index=None)
   
    logout()



def lgtStock():
    password=pd.DataFrame({'host':['jqdatasdk'],
                           'username':['18009020072'],
                           'password':['4187Xslc61']},
                           columns=['host','username','password'])
    
    auth(password['username'][0],password['password'][0])
    
    lastQueryCount=get_query_count()  #{'total': 10000000, 'spare': 17485426}
    if lastQueryCount['spare']<=5000:
        print('剩余查询条数已经不足，退出行情查询抓取...')
    else:
        startDate='2005-01-01'
        q=query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.day>=startDate)
        df=finance.run_query(q)
        #df['date']=pd.to_datetime(df['date']) 
        
        while lastQueryCount['spare']>5000:
            print(df.iloc[-1]['day'])
            q=query(finance.STK_HK_HOLD_INFO).filter(
                finance.STK_HK_HOLD_INFO.day>=df.iloc[-1]['day'])
            newDf=finance.run_query(q)
            #newDf['date']=newDf.to_datetime(df['date'])
            
            df=pd.concat([df,newDf],ignore_index=True)
            if newDf.empty or newDf.iloc[-1]['day']==datetime.date(2017,3,17):
                break
            
            lastQueryCount=get_query_count()
        #print(df)
    
    df.to_csv('./data/exchangeTradInfo/陆股通个股2.csv',
              encoding='gbk',
              index=None)
   
    logout()
if __name__=="__main__":
    #initiLgt()
    
    #initiLgtChengJiao()
    lgtStock()
    """auth('18009020072','4187Xslc61')
    print(get_query_count())
    logout()"""
