import zhpLiangHua.djangoShell

import os
import numpy as np
import pandas as pd
import jqdatasdk as jq
import tushare as ts
from datetime import datetime,timedelta

from updateData.calculation import junXian
from utils.convert import normalize_code
from stock_hs_A.models import Securities,IndustryType,SecurityType
from updateData.calculation import junXian
from updateData.thirdLibrary.dailyUpdateJq import  DailyQuotesUpdateJq

import utils.pandasSetting

def initiIndustryDailyPrice():
    """
    注意：该程序只运行一次，后续增量式更细数据
    第一次获取申万一级行业的日行情数据
    
    ret:申万一级的日行情数据存储到 ./data/dailyPrice/industry
    """
     
    
    for industryObj in IndustryType.objects.get(name="申万一级行业").industries_set.all():
        q=jq.query(jq.finance.SW1_DAILY_PRICE).filter(
            jq.finance.SW1_DAILY_PRICE.code==industryObj.code).order_by(
                jq.finance.SW1_DAILY_PRICE.date.desc())
        df=jq.finance.run_query(q)
        del df['id']
    
        
        dailyPrice=df.copy()
        
        while len(df)>0:             
            q=jq.query(jq.finance.SW1_DAILY_PRICE).filter(
                jq.finance.SW1_DAILY_PRICE.code==industryObj.code,
                jq.finance.SW1_DAILY_PRICE.date<df.iloc[len(df)-1,0]).order_by(
                    jq.finance.SW1_DAILY_PRICE.date.desc())
            df=jq.finance.run_query(q)
            
            df['change_pct']=df['change_pct']/100
            del df['id']
            dailyPrice=pd.concat([dailyPrice,df],ignore_index=True)
          
        dailyPrice=junXian(dailyPrice)
        
        dailyPrice.to_csv('./data/dailyPrice/industry/'+industryObj.code+'.csv',
                  encoding='gbk',
                  index=False,
                  float_format='%.15f')
   


def queryMarketData(code,dates):
    """
    获取code的市值数据，该数据随着日行情数据，每日更新
    code
    dates：日期列表
    
    ret:DataFrame
    ['id' ,'code','pe_ratio',  'turnover_ratio',  'pb_ratio',  'ps_ratio','pcf_ratio','capitalization','market_cap','circulating_cap','circulating_market_cap' ,'day','pe_ratio_lyr']
    """
    dfList=[]
    
    for date in dates:
        q = jq.query(
                    jq.valuation
                ).filter(
                    jq.valuation.code == code
                )
        #print(jq.get_fundamentals(q, date))
        dfList.append(jq.get_fundamentals(q, date))
    
    return pd.concat(dfList,ignore_index=True)
    
def initiStockDailyPrice():
    """
    注意：该函数只能运行一次，初始化所有股票的日行情数据
    初始化所有股票的日行情数据,基础数据基于刑不行给的日行情数据
    """
    
    #更新刑不行未给出的新股数据
#     updataObj=DailyQuotesUpdateJq()
#     dbJqCodes=[obj.code for obj in SecurityType.objects.get(name='stock').mainType.all()]
#     
#     path=r'E:\python\src\zhpLiangHua\updateData\data\dailyPrice\stock\price'
#     
#     zhpCodes=[]
#     for file in os.listdir(path):
#         zhpCodes.append(file.split('.csv')[0])
#         
#     for jqCode in set(dbJqCodes)-set(zhpCodes):
#         try:
#             updataObj.setCodeList([jqCode,])
#             newDf=updataObj.stockPrice('1999-01-01', pd.datetime.today())
#             
#             #处理nan数据
#             newDf.dropna(subset=['open','close'],how='all',inplace=True)
#             
#             if not newDf.empty:
#                 newDf['date']=pd.to_datetime(newDf['time'])
#                 newDf.reset_index(level=0,drop=True,inplace=True)
#                 newDf['code']=jqCode
#         except Exception as e:
#             print(e)
#         else:
#             #step6:保存数据
#             #columnsOrder=['date','code','open','close','high','low','paused','pre_close','volume','money','turnover_ratio','high_limit','low_limit','capitalization','circulating_cap','circulating_market_cap','market_cap','pe_ratio','pe_ratio_lyr','pb_ratio','ps_ratio','pcf_ratio']                     
#             columnsOrder=['date','code','open','close','high','low','pre_close','volume','money','high_limit','low_limit','paused']                     
#             newDf[columnsOrder].to_csv('../data/dailyPrice/stock/price/new/'+jqCode+'.csv',
#                                  index=False,
#                                  float_format='%.15f')
#        
#     updataObj.logoutJq()
#     exit()
    
    problemList=['000013.XSHE', '000015.XSHE', '000047.XSHE', '000405.XSHE', '000412.XSHE', '000508.XSHE', '000542.XSHE', '000556.XSHE', '000588.XSHE', '000621.XSHE', '000653.XSHE', '000658.XSHE', '000660.XSHE', '000675.XSHE', '000689.XSHE', '000730.XSHE', '600625.XSHG', '600632.XSHG', '600646.XSHG', '600669.XSHG', '600670.XSHG', '600709.XSHG', '600813.XSHG', '600878.XSHG']
    
#     for code in problemList:        
#         os.remove('../data/dailyPrice/stock/price/'+code+'.csv')
#         
#     exit()
    
    updataObj=DailyQuotesUpdateJq()
    #step1:获取文件夹下的所有文件，文件名转换成jq格式
    filePath=r'Z:\股票知识\xbx_stock_day_data-2020-09-25\xbx_stock_day_data-2020-09-25\stock'
    
#     csvFiles=os.listdir(filePath)
#     
#     for csvFile in csvFiles:
#         #print(csvFile)
#         if csvFile.startswith('sh') or csvFile.startswith('sz'):
#             newName=normalize_code(csvFile.split('.')[0])+'.csv'
#             os.rename(filePath+'/'+csvFile,filePath+'/'+newName)
    
    #step2:打开股票日行情csv文件，转换数据格式
    
    #for csvFile in os.listdir(filePath):
    for code in problemList:
        #csvFile='000001.XSHE.csv'
        #code='.'.join(csvFile.split('.',-2)[0:2])
         
        df=pd.read_csv(filePath+'/'+code+'.csv',
                       encoding='gbk',
                       skiprows=1,)
         
        del df['股票名称']
        df.rename(columns={'股票代码':'code','交易日期':'date','开盘价':'open','收盘价':'close','最高价':'high','最低价':'low','前收盘价':'pre_close','成交量':'volume','成交额':'money','总市值':'market_cap','流通市值':'circulating_market_cap'},inplace=True)
        df['code']=code
        df['date']=pd.to_datetime(df['date'])
        df['high_limit']=df['pre_close']*1.097
        df['low_limit']=df['pre_close']*0.903
        
        #step3:处理停牌数据，与上证指数的行情数据合并对比
        startDate=df.iloc[0]['date']
        endDate=df.iloc[-1]['date']
         
        #获取上证指数的行情数据
        indexDf=pd.read_csv('../data/dailyPrice/index/000001.XSHG.csv',
                          parse_dates=['date'])
        indexDf=(indexDf[(indexDf['date']>=startDate) & (indexDf['date']<=endDate)])[['date','code']]
        indexDf.rename(columns={'code':'c'},inplace=True)
        #print(indexDf)
         
        df=pd.merge(
            left=df,
            right=indexDf,
            on=['date'],
            how='outer',
            sort=True,        
            )
         
         
        df[['code','open','high_limit','low_limit','circulating_market_cap','market_cap']]=df[['code','open','high_limit','low_limit','circulating_market_cap','market_cap']].fillna(method='ffill')
        #df['pre_close']=df['pre_close'].fillna(value=df['open'])
        df['pre_close'].fillna(value=df['open'],inplace=True)
        df['close']=df['close'].fillna(value=df['open'])
        df['high']=df['high'].fillna(value=df['open'])
        df['low']=df['low'].fillna(value=df['open'])
         
        df[['volume','money']]=df[['volume','money']].fillna(value=0)
         
        df.loc[df[df['volume']==0].index,'paused']=1
        df['paused'].fillna(value=0,inplace=True)
         
        del df['c']
          
        #step4：获取jq数据，完成数据的更新
        startDate=df.iloc[-1]['date']+pd.Timedelta(days=1)
          
        #try:
        if False:
            updataObj.setCodeList([code,])
            newDf=updataObj.stockPrice(startDate, pd.datetime.today())
#             newDf=jq.get_price(
#                 code,
#                 start_date=startDate+timedelta(days=1),
#                 end_date=pd.datetime.today(),#startDate+Timedelta(days=10),#datetime.today(),
#                 frequency='daily',
#                 fields=['open', 'close', 'low', 'high', 'volume', 'money', 'high_limit','low_limit', 'pre_close', 'paused'],
#                 fq=None
#                 )
            #print(newDf)
            if not newDf.empty:
                newDf['date']=pd.to_datetime(newDf['time'])
                newDf.reset_index(level=0,drop=True,inplace=True)
                newDf['code']=code
                #print(newDf)
                 
                 
                tmpDf=pd.concat([df,newDf],ignore_index=True,sort=False)
                #print((tmpDf[tmpDf['market_cap'].isnull()]['date']).dt.strftime('%Y-%m-%d').tolist())
                 
                #step5：补充完善市值数据
    #             marketData=queryMarketData(code,(tmpDf[tmpDf['market_cap'].isnull()]['date']).dt.strftime('%Y-%m-%d').tolist())
    #              
    #             marketData['capitalization']=marketData['capitalization']*10000
    #             marketData['circulating_cap']=marketData['circulating_cap']*10000
    #             marketData['market_cap']=marketData['market_cap']*100000000
    #             marketData['circulating_market_cap']=marketData['circulating_market_cap']*100000000
    #              
    #             del marketData['id']
    #              
    #             marketData.rename(columns={'day':'date'},inplace=True)
    #             marketData['date']=pd.to_datetime(marketData['date'])
    #              
    #             tmpDf.index=tmpDf['date']
    #             marketData.index=marketData['date']
    #             
    #             tmpDf=tmpDf.combine_first(marketData)
                 
            
        #except Exception as e:
        #    print(e)
            
        #step6:保存数据
        #columnsOrder=['date','code','open','close','high','low','paused','pre_close','volume','money','turnover_ratio','high_limit','low_limit','capitalization','circulating_cap','circulating_market_cap','market_cap','pe_ratio','pe_ratio_lyr','pb_ratio','ps_ratio','pcf_ratio']                     
        columnsOrder=['date','code','open','close','high','low','pre_close','volume','money','high_limit','low_limit','paused']                     
        #tmpDf[columnsOrder].to_csv('../data/dailyPrice/stock/price/'+code+'.csv',
        df[columnsOrder].to_csv('../data/dailyPrice/stock/price/'+code+'.csv',
                             index=False,
                             float_format='%.15f')
        
    
    updataObj.logoutJq()
            
def initiIndexDailyPrice(indexCode):
    """
    初始化指数日行情
    初始数据：行不行提供的上证指数数据
    注意：构建初始数据时使用，以后不再使用
    """
    df=pd.read_csv('./data/dailyPrice/index/sh000001.csv')
    
    df['date']=pd.to_datetime(df['date'])
    df.rename(columns={'index_code':'code','change':'change_pct'},inplace=True)
    
    df.sort_values(by='date',inplace=True)
    df.fillna(value=0.0,inplace=True)    
    
    df['pre_close']=df['close'].shift(1)
    df['pre_close'].fillna(value=df['close'],inplace=True)
    
    df['code']='000001.XSHG'
    df['paused']=0.0
    
    print(df)
    
    df.to_csv('./data/dailyPrice/index/'+indexCode+'.csv',
              index=False)



def updateIndexDailyPrice(indexCode='000001.XSHG'):
    """
    更细指数的日行情数据
    indexCode:默认上证指数
    """
    #index='000001.XSHG'
    #step1:获取到最后一行数据的日期
    df1=pd.read_csv('./data/dailyPrice/index/000001.XSHG.csv',
                   parse_dates=['date',])
    
    #print(df1.tail(10))
    df1.dropna(how='all',inplace=True)
    exisDate=df1.iloc[-1]['date']
    
    #step2:从jqdata中获取从现有数据到今天的数据
    
    
    df=jq.get_price(indexCode,
                  start_date=exisDate+pd.Timedelta(days=1),
                  end_date=datetime.today(),#'2016-12-25',
                  frequency='daily',
                  fields=['open', 'close', 'low', 'high', 'volume', 'money', 'pre_close', 'paused'],
                  fq=None
            )
    df['change_pct']=(df['close']-df['pre_close'])/df['pre_close']
    df['date']=df.index
    df['code']=indexCode
    df.reset_index(level=0,drop=True,inplace=True)
    #print(pd.concat([df1,df],ignore_index=True,sort=False))
    
    
    
    #step3:两者合并并保存
    (pd.concat([df1,df],ignore_index=True,sort=False)).to_csv('./data/dailyPrice/index/000001.XSHG.csv',
              index=False,
              float_format='%.4f')
    

def calculateIndex():
    """
    计算指标：
        均线：junXian()
    """
    
    csvFile='./data/dailyPrice/index/000001.XSHG.csv'
    df=pd.read_csv(csvFile)
    
    df=junXian(df)
    print(df)
    
    df.to_csv(csvFile,
              index=False,
              float_format='%.15f')

def getDailyPriceByTushare():
    ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')
    pro=ts.pro_api()
    df=pro.daily(ts_code='000585.SZ',start_date='20210101',end_date='20210113')
    print(df)

if __name__=='__main__':    
    #initiIndustryDailyPrice()
    #zuHeDf()
    initiStockDailyPrice()
    #updateIndexDailyPrice()
    #initiIndexDailyPrice('000001.XSHG')
    #updateIndexDailyPrice('000001.XSHG')
    
    #initiStockDailyPrice()
    #queryMarketData()
    
    '''sObjs=Securities.objects.filter(code__contains='002019.XSHG')
    print(sObjs)
    
    jqdataAuth()
    df=jq.get_price('002019.XSHG',start_date='2020-01-01')
    print(df)
    jq.logout()'''
    
    #calculateIndex()
    #getDailyPriceByTushare()
    