# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import pandas as pd
import tushare as ts
from datetime import datetime
from multiprocessing.pool import Pool

import zhpLiangHua.dataPath as path
from utils.path import mkdirs
from utils.file import readCsv,saveCsv
from utils.convert import normalize_code,jqcodeToXbxCode,mergeWithIndexData
from utils.calculation import priceLimit,amplitude
from zhpLiangHua.dataPath import STOCK_FUNDAMENTAL_JQ,STOCK_PRICE



'''
Created on 2021年1月21日

@author: My

用于整理数据
'''

import utils.pandasSetting
pd.set_option('display.max_rows', 500)  # 最多显示数据的行数

def sortSwL1Price():
    df=pd.DataFrame()
    for file in os.listdir(os.path.join(path.SWL1_VALUE,'tmp')):        
        if file.endswith('.csv'):
            filePath=os.path.join(path.SWL1_VALUE,'tmp',file)
            print(filePath)
            df=df.append(pd.read_csv(filePath,
                                   #encoding='gbk',
                                     dtype={'code':str},
                                     parse_dates=['date']
                                     ),
                    ignore_index=True)
    
   
    #del df['id']
    df['dividend_ratio']=df['dividend_ratio']/100.0
    df['money_ratio']=df['money_ratio']/100.0
    df['turnover_ratio']=df['turnover_ratio']/100.0
    
    for name,group in df.groupby('code'):
        print(name)
        group.to_csv(os.path.join(path.SWL1_VALUE,name+'.csv'),
            float_format='%.15f',
                     index=False,         
                     )
            
def sortK60min():
    path.K_60M
    
    df=pd.DataFrame()
   
    for csvFile in os.listdir(os.path.join(path.K_60M,'tmp')):
        if csvFile.endswith('.csv'):
            filePath=os.path.join(path.K_60M,'tmp',csvFile)
            print(filePath)
            K60Df=pd.read_csv(filePath, 
                                     dtype={'code':str},
                                     parse_dates=['date'])
            K60Df['code']=csvFile.split('_',1)[0]
            K60Df['date']=pd.to_datetime(K60Df['date'])
            
            K60Df.drop(K60Df[K60Df['money']==0].index,inplace=True)
            
            df=df.append(K60Df[['date','code', 'open','close','high','low','volume','money']],                                     
                        ignore_index=True)
      
            
    for name,group in df.groupby('code'):
        print(name)
        group.sort_values(by=['date'],inplace=True)
        group.to_csv(os.path.join(path.K_60M,name+'.csv'),
                     float_format='%.15f',
                     index=False,         
                     )
    

def sortedMoneyFlow():
    """
          整理A股的个股资金流向
         存储位置：/daily/moneyFlow/jqdata/sorted
         存储格式：按照个股的jqdata代码存储个股的资金流向：主力、超大单、大单、中单、小单
    """
    df=pd.DataFrame()

    rootPath='./data/daily/moneyFlow/jqdata'
    
    count=0
    for file in os.listdir(rootPath):
        if file.endswith('.csv'):            
            filePath=os.path.join(rootPath,file)
            count=count+1
            print(count)
            #print(filePath)
            df=df.append(pd.read_csv(filePath, encoding='gbk',
                                     dtype={'sec_code':str},
                                     ),
                         ignore_index=True)
    
    grouped=df.groupby('sec_code')
    
    for name,group in grouped:
        print(name)    
        
        #print(group[group.duplicated()==True])
        group.drop_duplicates(subset=['date'],keep='first',inplace=True)
        
        group['change_pct']=group['change_pct']/100.0
        
        group['net_amount_main']=group['net_amount_main']*10000.0
        group['net_pct_main']=group['net_pct_main']/100.0
        
        group['net_amount_xl']=group['net_amount_xl']*10000.0
        group['net_pct_xl']=group['net_pct_xl']/100.0
        
        group['net_amount_l']=group['net_amount_l']*10000.0
        group['net_pct_l']=group['net_pct_l']/100.0
        
        group['net_amount_m']=group['net_amount_m']*10000.0
        group['net_amount_m']=group['net_amount_m']/100.0
        
        group['net_amount_s']=group['net_amount_s']*10000.0
        group['net_pct_s']=group['net_pct_s']/100.0
        
        #print(group)
        group.to_csv(os.path.join(rootPath,'sorted',name+'.csv'),
                     float_format='%.15f',
                     index=False,)

def sortedHKHoldInfo():
    """
         整理新沪深股通的个股数据
         存储位置：/data/daily/hsgt/HKHold/jqdata/sorted
         存储格式：按照个股的jq代码存储，记录每日的陆股通数据流向，时序数据
    """
    
    df=pd.DataFrame()
    
    rootPath='./data/daily/hsgt/HKHold/jqdata'
          
    for file in os.listdir(rootPath):
        if file.endswith('.csv'):
                
            filePath=os.path.join(rootPath,file)
            print(filePath)
            df=df.append(pd.read_csv(filePath, encoding='gbk',
                                     dtype={'link_id':str,'code':str},),
                                     ignore_index=True)
    
    grouped=df.groupby('code')
    
    for name,group in grouped:
        print(name)    
        del group['id']
        
        group['share_ratio']=group['share_ratio']/100.0
        #print(group[group.duplicated()==True])
        group.drop_duplicates(subset=['day'],keep='first',inplace=True)
        
        #print(group)
        group.to_csv(os.path.join(rootPath,'sorted',name+'.csv'),
                     float_format='%.15f',
                     index=False,)
    

def sortedExchangRateByJq():
    """
          整理沪深股通的每日市场汇率数据
         存储位置：/data/daily/hsgt/moneyflow/jqdata/rate/sorted
         存储格式：按照陆股通的代码存储，时序数据
                 市场通编码    市场通名称
        310001    沪股通
        310002    深股通
        310003    港股通（沪）
        310004    港股通（深）
    """
    df=pd.DataFrame()

    rootPath='./data/daily/hsgt/moneyflow/jqdata/rate'
     
    for file in os.listdir(rootPath):
        if file.endswith('.csv'):
                
            filePath=os.path.join(rootPath,file)
            print(filePath)
            df=df.append(pd.read_csv(filePath, encoding='gbk',dtype={'link_id':str},),
                          ignore_index=True)
    
    grouped=df.groupby('link_id')
    
    for name,group in grouped:
        print(name)    
        del group['id']
       
        #print(group[group.duplicated()==True])
        group.drop_duplicates(subset=['day'],keep='first',inplace=True)

        group.to_csv(os.path.join(rootPath,'sorted',name+'.csv'),
                     float_format='%.15f',
                     index=False,)
        

def sortedLgtMoneyflowByJq():
    """
          整理沪深股通的每日流向数据
         存储位置：/data/daily/hsgt/moneyflow/jqdata/sorted
         存储格式：按照个股的jq代码存储，时序数据
    """
    df=pd.DataFrame()

    rootPath='./data/daily/hsgt/moneyflow/jqdata'
    #for root,dirs,files in os.walk('./data'):
        #print('root:',root)
        #print('dirs',dirs)
        #print('files',files)
        
    for file in os.listdir(rootPath):
        if file.endswith('.csv'):
                
            filePath=os.path.join(rootPath,file)
            print(filePath)
            df=df.append(pd.read_csv(filePath, encoding='gbk',dtype={'link_id':str},),
                          ignore_index=True)
    
    grouped=df.groupby('link_id')
    
    for name,group in grouped:
        print(name)    
        del group['id']
        #group.reset_index(level=0,drop=True,inplace=True)
        group['buy_amount']=group['buy_amount']*100000000
        group['sell_amount']=group['sell_amount']*100000000
        group['sum_amount']=group['sum_amount']*100000000
        group['quota']=group['quota']*10000
        group['quota_balance']=group['quota_balance']*100000000
        group['quota_daily']=group['quota_daily']*100000000
        group['quota_daily_balance']=group['quota_daily_balance']*100000000
      
        
        #print(group[group.duplicated()==True])
        group.drop_duplicates(subset=['day'],keep='first',inplace=True)
        
        #print(group)
        group.to_csv(os.path.join(rootPath,'sorted',name+'.csv'),
                     float_format='%.15f',
                     index=False,)

def sortedExchangeTradInfo():   
    """
        整理交易所的交易数据
        存储位置：/data/daily/exchange/jqdata/sorted
        存储方式：按照市场代码存储，时序数据
            市场编码    交易市场名称    备注
        322001    上海市场    
        322002    上海A股    
        322003    上海B股    
        322004    深圳市场    该市场交易所未公布成交量和成交笔数
        322005    深市主板    
        322006    中小企业板    
        322007    创业板
    """
    df=pd.DataFrame()
    
    rootPath='./data/daily/exchange/jqdata'
    
    for file in os.listdir(rootPath):
        if file.endswith('.csv'):
                
            filePath=os.path.join(rootPath,file)
            print(filePath)
            df=df.append(pd.read_csv(filePath, encoding='gbk',dtype={'exchange_code':str},),
                          ignore_index=True)
    
    grouped=df.groupby('exchange_code')
    
    for name,group in grouped:
        print(name)    
        del group['id']
        #group.reset_index(level=0,drop=True,inplace=True)
        group['total_market_cap']=group['total_market_cap']*100000000
        group['circulating_market_cap']=group['circulating_market_cap']*100000000
        group['circulating_market_cap']=group['circulating_market_cap']*100000000
        group['volume']=group['volume']*10000
        group['money']=group['money']*100000000;
        group['deal_number']=group['deal_number']*10000
        group['pe_average']=group['pe_average']/100.0
        group['turnover_ratio']=group['turnover_ratio']/100.0
        
        #print(group[group.duplicated()==True])
        group.drop_duplicates(subset=['date'],keep='first',inplace=True)
       
        group.to_csv(os.path.join(rootPath,'sorted',name+'.csv'),
                     float_format='%.15f',
                     index=False,)

def sortStockFundamentalJq():
    print(STOCK_FUNDAMENTAL_JQ)
    sortedPath=os.path.join(STOCK_FUNDAMENTAL_JQ,'sorted')
    
    df=pd.DataFrame()
    
    for file in os.listdir(STOCK_FUNDAMENTAL_JQ):
        print(file)
        if file.endswith('.csv'):
            df=df.append(pd.read_csv(os.path.join(STOCK_FUNDAMENTAL_JQ,file),encoding='gbk',),                      
                      ignore_index=True)
    
    del df['id']
    
    renameDict={'day':'date',
                'capitalization':'total_share',
                'circulating_cap':'float_share',
                'market_cap':'total_mv',
                'circulating_market_cap':'circ_mv',
                'pe_ratio':'pe_ttm',
                'pe_ratio_lyr':'pe',
                'pb_ratio':'pb',
                'ps_ratio':'ps_ttm',
                'pcf_ratio':'pcf_ttm',
                'turnover_ratio':'trunover'}
    
    df.rename(columns=renameDict,
              inplace=True)
    
    df['date']=pd.to_datetime(df['date'])
    df['trunover']=df['trunover']/100.0
    df['total_share']=df['total_share']*10000
    df['float_share']=df['float_share']*10000
    df['total_mv']=df['total_mv']*100000000
    df['circ_mv']=df['circ_mv']*100000000
    
    columns=['date','code','total_share','float_share','total_mv','circ_mv','trunover','pe_ttm','pe','pb','ps_ttm','pcf_ttm']
    df=df[columns]
    
    for name,group in df.groupby('code'):
        print(name)
        group.drop_duplicates(subset=['date'],keep='first',inplace=True)
        group.sort_values(by=['date'],inplace=True)
        group.to_csv(os.path.join(sortedPath,name+'.csv'),
                     float_format='%.15f',
                     index=False,)

def mergePriceFundamental():
    """
    合并股票日线行情与市值数据(jqdata)
    """
    xbxPath=r'Z:\股票知识\xbx_stock_day_data-2021-01-29\stock'
    
    columns=['date', 'code', 'name','open', 'close', 'high', 'low', 'pre_close', 'volume',
           'money', 'trunover','high_limit', 'low_limit', 'pct_change', 
           'circ_mv', 'total_mv', 'total_share', 'float_share', 
           'pe_ttm', 'pe', 'pb', 'ps_ttm', 'pcf_ttm', 'paused']
    
    #step1:遍历所有的日线行情
        #从刑不行数据中找出对应文件的市值数据和流动市值数据，合并到日线行情数据
        #从fundamental中找出对应的文件，补充市值数据
    for csvFile in os.listdir(STOCK_PRICE):
        code=csvFile.split('.csv')[0]        
        if os.path.exists(os.path.join(path.SELECT,code+'.csv')):
            continue
        print(code)
        if csvFile.endswith('.csv'):
            priceDf=readCsv(os.path.join(STOCK_PRICE,csvFile))
            #priceDf=priceDf[priceDf['date']>='2005-01-04'].head(10)
            #print(priceDf)
            
            xbxFile=os.path.join(xbxPath,jqcodeToXbxCode(code)+'.csv')
            xbxExists=False
            if os.path.exists(xbxFile):
                xbxExists=True
                xbxPriceDf=pd.read_csv(xbxFile,
                                       encoding='gbk',
                                       skiprows=1,
                                       usecols=['股票名称','交易日期','流通市值','总市值'],
                                       parse_dates=['交易日期'])
                
                #xbxPriceDf=xbxPriceDf[xbxPriceDf['交易日期']>='2005-01-04'].head(10)
                xbxPriceDf.rename(columns={'总市值':'total_mv','流通市值':'circ_mv','交易日期':'date','股票名称':'name'},inplace=True)
                #print(xbxPriceDf)
                
                priceDf=pd.merge(left=priceDf,
                                 right=xbxPriceDf,
                                 on='date',
                                 how='left',
                                 sort=True,
                                 indicator=False)
                #处理停牌
                
                #priceDf[['name','circ_mv','total_mv']]=priceDf[['name','circ_mv','total_mv']].fillna(method='ffill')    #此语句无效
                #print(priceDf)
            
            fundamentalFile=os.path.join(STOCK_FUNDAMENTAL_JQ,csvFile)            
            if os.path.exists(fundamentalFile):
                fundamentalDf=readCsv(fundamentalFile)
                if xbxExists==True:                    
                    fundamentalDf=fundamentalDf[['date','code','total_share','float_share','trunover','pe_ttm','pe','pb','ps_ttm','pcf_ttm']]#.head(10)
                    
                    #print(fundamentalDf)
                    priceDf=pd.merge(left=priceDf,
                                     right=fundamentalDf,
                                     on=['date','code'],
                                     how='left',
                                     sort=True,
                                     indicator=False)
                    #print(priceDf)
                    saveCsv(priceDf[columns],
                            os.path.join(path.SELECT,code+'.csv')
                            )
                else:
                    priceDf=pd.merge(left=priceDf,
                                     right=fundamentalDf,
                                     on=['date','code'],
                                     how='left',
                                     sort=True,
                                     indicator=False)
                    #print(priceDf)
                    priceDf['name']='待查'
                    saveCsv(priceDf[columns],
                            os.path.join(path.SELECT,code+'.csv')
                            ) 

def checkMergePriceFundamental():
    columns=['date', 'code', 'name','open', 'close', 'high', 'low', 'pre_close', 'volume',
           'money', 'trunover','high_limit', 'low_limit', 'pct_change', 
           'circ_mv', 'total_mv', 'total_share', 'float_share', 
           'pe_ttm', 'pe', 'pb', 'ps_ttm', 'pcf_ttm', 'paused']
    
    #step1：处理停牌时的数据
    for csvFile in os.listdir(path.SELECT):
        print(csvFile)
        df=readCsv(os.path.join(path.SELECT,csvFile))

        df.set_index(['date'],inplace=True)
        #df[['name','circ_mv','total_mv']]=df[['name','circ_mv','total_mv']].fillna(method='ffill')
        dfValue=readCsv(os.path.join(path.STOCK_FUNDAMENTAL_JQ,csvFile))[['date','code','circ_mv','total_mv','total_share', 'float_share', 'trunover',
                                                                          'pe_ttm', 'pe', 'pb', 'ps_ttm', 'pcf_ttm']]
        dfValue.set_index(['date'],inplace=True)
        #print(dfValue)
        df=df.combine_first(dfValue)
        df.reset_index(drop=False,inplace=True)
        
        df['name'].fillna(method='ffill',inplace=True)
        df[['circ_mv','total_mv']]=df[['circ_mv','total_mv']].fillna(method='ffill')
        #df[['name','circ_mv','total_mv']]=df[['name','circ_mv','total_mv']].fillna(method='ffill')
        
        try:
            saveCsv(df[columns],os.path.join(path.SELECT,csvFile))
        except Exception as e:
            print('problem:',csvFile)
        
        
    

def sortMargin():
    path.MARGIN   
    
    df=pd.DataFrame()
    for csvFile in os.listdir(os.path.join(path.MARGIN,'sorted')):
        print(csvFile)
        if csvFile.endswith('.csv'):
            df=df.append(
                readCsv(os.path.join(path.MARGIN,'sorted',csvFile)),
                ignore_index=True
                )
        
    
    for name,group in df.groupby('sec_code'):
        print(name)
        group.drop_duplicates(subset=['date'],keep='first',inplace=True)
        group.sort_values(by=['date'],inplace=True)
        group.to_csv(
            os.path.join(path.MARGIN,name+'.csv'),
            float_format='%.15f',
            index=False,
            )
    
            
          
        
def checkDailyPrice():
    path.STOCK_PRICE
    
    #problemDailyPriceList=[]
    
    for csvFile in os.listdir(path.STOCK_FUNDAMENTAL_JQ):
        if csvFile.endswith('.csv'):
            csvPath=os.path.join(path.STOCK_FUNDAMENTAL_JQ,csvFile)
            df=readCsv(csvPath)
            if not df[df['total_share'].isnull()].empty:
                print(csvFile)
                df['total_share'].fillna(method='ffill',inplace=True)
                saveCsv(df,csvPath)
                #problemDailyPriceList.append(csvFile)
    
    #print(problemDailyPriceList)

def dropDuplecateDate(dataPath):
    for csvFile in os.listdir(dataPath):
        print(csvFile)
        df=readCsv(os.path.join(dataPath,csvFile))
        df.drop_duplicates(subset=['date'], keep='first', inplace=True)
        saveCsv(df,os.path.join(dataPath,csvFile))

class SortDailyData():
    def __init__(self):
        pass
    
    def mergeIndex(self):
        pass
    
    def mergeDailyValue(self):
        pass
    

def checkLimitPrice():
    for csvFile in os.listdir(path.STOCK_PRICE):
        print(csvFile)
        filePath=os.path.join(path.STOCK_PRICE,csvFile)
        df=readCsv(filePath)
        df=priceLimit(df)
        
        #print(df.loc[df['name'].str.contains('ST')])
        #print(df)
        saveCsv(df,filePath)
        
def calcuAmplitude():
    for csvFile in os.listdir(path.SELECT):
        print(csvFile)
        filePath=os.path.join(path.SELECT,csvFile)
        df=readCsv(filePath)
        df=amplitude(df)        
        saveCsv(df,filePath)

def completionTradDays():
    indexDf=readCsv(os.path.join(path.INDEX_PRICE,'000001.XSHG.csv'))[['date']]
    
    for csvFile in os.listdir(path.STOCK_PRICE):
        print(csvFile)
        filePath=os.path.join(path.STOCK_PRICE,csvFile)
        df=readCsv(filePath)
        df=mergeWithIndexData(df,indexDf)
        df.drop_duplicates(subset=['date'], keep='first', inplace=True)
        saveCsv(df,filePath)

def completionSelectNa(csvFile):
    #for csvFile in os.listdir(path.SELECT):
        #csvFile='600627.XSHG.csv'
        print(csvFile)
        filePath=os.path.join(path.SELECT,csvFile)
        
        df=readCsv(filePath)
        
        df['close'].fillna(method='ffill',inplace=True)
        df['paused']
    
        df['open'].fillna(value=df['close'],inplace=True)
        df['high'].fillna(value=df['close'],inplace=True)
        df['low'].fillna(value=df['close'],inplace=True)
        
        df['pre_close'].fillna(value=df['close'].shift(),inplace=True)
        
        df.loc[:,['pct_change','money','volume']]=df[['pct_change','money','volume']].fillna(value=0)
        
        # ===用前一天的数据，补全其余空值
        df['paused'].fillna(value=1,inplace=True)
        df.fillna(method='ffill', inplace=True)
        
        
        saveCsv(df,filePath)

    
if __name__=="__main__":
    with Pool(processes=12) as pool:
        pool.map(completionSelectNa,sorted(os.listdir(path.SELECT)))

    #sortedExchangeTradInfo()
    #sortedLgtMoneyflowByJq()
    #sortedExchangRateByJq()
    #sortStockFundamentalJq()
    
    #mergePriceFundamental()
    
    #checkDailyPrice()
    #sortSwL1Price()
    #sortMargin()
    
    #mergePriceFundamental()
    
    #checkMergePriceFundamental()
    
    #dropDuplecateDate(path.SELECT)
    
    #sortK60min()
    #checkLimitPrice()
    #calcuAmplitude()
    #completionTradDays()
    
    #completionSelectNa()