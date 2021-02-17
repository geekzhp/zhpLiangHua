'''
Created on 2021年1月24日

@author: Administrator

每日执行，主要用于更新日行情相关数据
'''

import zhpLiangHua.djangoShell

import os
import time
import pandas as pd
import jqdatasdk as jq
from datetime import datetime,timedelta

from utils.file import readCsv,saveCsv
import zhpLiangHua.dataPath as path
from updateData.thirdLibrary.basic import UpdataBasic
from updateData.thirdLibrary.dailyUpdateJq import DailyQuotesUpdateJq
from stock_hs_A.models import TradeDay,SecurityType,IndustryType, Securities
#from updateData.thirdLibrary.dailyUpdateJq import DailyQuotesUpdateJq

import utils.pandasSetting

"""
更新基础数据
    更新交易日历
    更新股票列表

更新日行情数据
    更新指数数据
    更新全部A股日行情数据
    更新全部A股的市值数据
"""

#---------------基础数据更新---------------------
def tradDay(updateObj):  #更新交易日历
    """
    更新国内所有交易所的交易日历
    """
    print('更新国内所有交易所的交易日历')
    
    tradeDayObj=TradeDay.objects.filter(exchagne__tsCode='SSE').last()
    #print(tradeDayObj.date+timedelta(days=1))
         
    updateObj.tradeDay((tradeDayObj.date+timedelta(days=1)).strftime('%Y%m%d'))      
  
def stockList(updateObj):   #更新股票列表
    """
    更新股票列表
    """
    print('更新股票列表')
    return updateObj.stockByJq()


def exchangeJqdata(updateObj):    #交易所日交易数据
    """
    交易所日交易数据
    """
    
    print('更新交易所交易数据')
    today=datetime.today().date()
    #path.EXCHANGE_JQ
    #step1:获取路径下的所有csv文件
    for file in os.listdir(path.EXCHANGE_JQ):   #此处只需要循环一次，将会获取到所有交易所的数据
        if file.endswith('.csv'):
    #step2：获取文件的最后日期
            startDt=readCsv(os.path.join(path.EXCHANGE_JQ,file)).iloc[-1]['date'].date()
            if startDt>=today:
                print('无需更新')                
            else:                
                ret=updateObj.exchangeTradeInfo(startDt+timedelta(days=1),today)
                if not ret.empty:
                    del ret['id']
                    #group.reset_index(level=0,drop=True,inplace=True)
                    ret['total_market_cap']=ret['total_market_cap']*100000000
                    ret['circulating_market_cap']=ret['circulating_market_cap']*100000000
                    ret['circulating_market_cap']=ret['circulating_market_cap']*100000000
                    ret['volume']=ret['volume']*10000
                    ret['money']=ret['money']*100000000;
                    ret['deal_number']=ret['deal_number']*10000
                    ret['pe_average']=ret['pe_average']/100.0
                    ret['turnover_ratio']=ret['turnover_ratio']/100.0
                    
                    for name,group in ret.groupby('exchange_code'):
                        saveCsv(group,
                                os.path.join(path.EXCHANGE_JQ,name+'.csv'),
                                isAppend=True)
                else:
                    print('jqdata返回空值，请检查,数据的最新日期是:{},当前日期是:{},从jqdata获取数据剩余:{}'.format(startDt,today,updateObj.lastQueryCount['spare']))
                        
                
        break

def hsgt(updateObj):    #更新沪深股通的数据
    """
    更新沪深股通的数据，包括资金流向、个股持股、利率数据
    """
    #path.HSGT
    
    #更新moneyFlow，并且获取到startDate    
    #更新Price
    print('更新市场通资金流向数据')
    startDt=readCsv(os.path.join(path.HSGT_PRICE,'310001.csv')).iloc[-1]['date']    #310001    沪股通
    if startDt>=datetime.today():
        print('市场通资金流向数据，无需更新')
    else:
        endDt=datetime.today()
        
        ret=updateObj.lgtMoneyflow(startDt+timedelta(days=1),endDt)
        if not ret.empty:
            ret.rename(columns={'day':'date'},inplace=True)
            ret[['link_id']] = ret[['link_id']].astype(str)
            del ret['id']
              
            ret['buy_amount']=ret['buy_amount']*100000000
            ret['sell_amount']=ret['sell_amount']*100000000
            ret['sum_amount']=ret['sum_amount']*100000000
            ret['quota']=ret['quota']*10000
            ret['quota_balance']=ret['quota_balance']*100000000
            ret['quota_daily']=ret['quota_daily']*100000000
            ret['quota_daily_balance']=ret['quota_daily_balance']*100000000
              
            for name,group in ret.groupby('link_id'):
                #print(name)
                #print(group)
                saveCsv(group,
                        os.path.join(path.HSGT_PRICE,name+'.csv'),
                        isAppend=True)
        else:
            print('jqdata返回空值，请检查,数据的最新日期是:{},当前日期是:{},从jqdata获取数据剩余:{}'.format(startDt,datetime.today(),updateObj.lastQueryCount['spare']))
                  
        #更新Rate
        ret=updateObj.exchangeRate(startDt+timedelta(days=1),endDt)
        if not ret.empty:
            ret.rename(columns={'day':'date'},inplace=True)
            ret[['link_id']] = ret[['link_id']].astype(str)
            del ret['id']
              
            for name,group in ret.groupby('link_id'):
                print(name)
                #print(group)
                saveCsv(group,
                        os.path.join(path.HSGT_RATE,name+'.csv'),
                        isAppend=True)
        else:
            print('jqdata返回空值，请检查,数据的最新日期是:{},当前日期是:{},从jqdata获取数据剩余:{}'.format(startDt,datetime.today(),updateObj.lastQueryCount['spare']))

def hsgtHold(updateObj):
    """
    更新市场通的个股持股数据，通常是第二日才会更新
    """
    print('更新市场通个股数据')
    today=datetime.today()
    startDt=readCsv(os.path.join(path.HSGT_HK_HOLD,'000001.XSHE.csv')).iloc[-1]['date']
    if startDt>=today:
        print('市场通个股数据，无需更新')
    else:                
        #更新HkHold
        for tradDay in TradeDay.objects.filter(exchagne__tsCode='SSE',isOpen=True,date__range=(startDt+timedelta(days=1),today)):
            #print('市场通个股持股数据更新日期:{}'.format(tradDay.date))
            ret=updateObj.HKHoldInfo(tradDay.date) 
            if not ret.empty:
                ret.rename(columns={'day':'date'},inplace=True)
                ret[['link_id']] = ret[['link_id']].astype(str)
                del ret['id']
                ret['share_ratio']=ret['share_ratio']/100.0
                 
                for name,group in ret.groupby('code'):
                    csvFile=os.path.join(path.HSGT_HK_HOLD,name+'.csv')
                    if os.path.exists(csvFile):
                        saveCsv(group,csvFile,isAppend=True)
                    else:
                        saveCsv(group,csvFile)
            else:
                print('jqdata返回空值，请检查,数据的最新日期是:{},当前日期是:{},从jqdata获取数据剩余:{}'.format(startDt,datetime.today(),updateObj.lastQueryCount['spare']))



def moneyflow(updateObj):   #更新资金流向
    """
    更新资金流向,从jqdata更细资金流向信息，超大单、大单、中单、小单、主力
    """
    #path.MONEY_FLOW
    print('更新个股的资金流向:超大单、大单、中单、小单、主力')
    
    columns=['date', 'sec_code', 'change_pct', 'net_amount_main', 'net_pct_main',
           'net_amount_xl', 'net_pct_xl', 'net_amount_l', 'net_pct_l',
           'net_amount_m', 'net_pct_m', 'net_amount_s', 'net_pct_s']
    
    today=datetime.today().date()
    jqCodeList=[obj.code for obj in SecurityType.objects.get(name='stock').mainType.filter(end_date__gt=today)]

    for code in jqCodeList:
        #print(code)
        csvFile=os.path.join(path.MONEY_FLOW,code+'.csv')
        if os.path.exists(csvFile):
            df=readCsv(csvFile)
            
            startDt=df.iloc[-1]['date'].date()+timedelta(days=1)
            if startDt<=today:
                updateObj.setCodeList([code,])           
                ret=updateObj.moneyFlow(startDt,today)
                
                if not ret.empty:          
                    ret['change_pct']=ret['change_pct']/100.0         
                    ret['net_amount_main']=ret['net_amount_main']*10000.0
                    ret['net_pct_main']=ret['net_pct_main']/100.0                 
                    ret['net_amount_xl']=ret['net_amount_xl']*10000.0
                    ret['net_pct_xl']=ret['net_pct_xl']/100.0                 
                    ret['net_amount_l']=ret['net_amount_l']*10000.0
                    ret['net_pct_l']=ret['net_pct_l']/100.0                 
                    ret['net_amount_m']=ret['net_amount_m']*10000.0
                    ret['net_amount_m']=ret['net_amount_m']/100.0                 
                    ret['net_amount_s']=ret['net_amount_s']*10000.0
                    ret['net_pct_s']=ret['net_pct_s']/100.0
                          
                    saveCsv(ret[columns],csvFile,isAppend=True)
        else:
            updateObj.setCodeList([code,]) 
            ret=updateObj.moneyFlow('2005-01-01',today)
            if not ret.empty:
                ret['change_pct']=ret['change_pct']/100.0         
                ret['net_amount_main']=ret['net_amount_main']*10000.0
                ret['net_pct_main']=ret['net_pct_main']/100.0                 
                ret['net_amount_xl']=ret['net_amount_xl']*10000.0
                ret['net_pct_xl']=ret['net_pct_xl']/100.0                 
                ret['net_amount_l']=ret['net_amount_l']*10000.0
                ret['net_pct_l']=ret['net_pct_l']/100.0                 
                ret['net_amount_m']=ret['net_amount_m']*10000.0
                ret['net_amount_m']=ret['net_amount_m']/100.0                 
                ret['net_amount_s']=ret['net_amount_s']*10000.0
                ret['net_pct_s']=ret['net_pct_s']/100.0  
                 
                saveCsv(ret[columns],csvFile)
         

def topList(updateObj):     #更新龙虎榜数据
    """
    更新龙虎榜数据
    """
    pass




def indexPrice(updateObj):  #更新指数行情，沪深300指数、中证800、中证1000等
    """
    上证指数:000001.XSHG
    上证50:000016.XSHG
    沪深300:000300.XSHG
    中证800:000906.XSHG
    中证1000指数:000852.XSHG
    创业板指:399006.XSHE
    
    df=df[['date','code','open' ,'close', 'low','high', 'volume' , 'money','pre_close']]
    """
    
    print('更新指数日行情')
    #path.INDEX_PRICE
    
    indexList=['000001.XSHG','000016.XSHG','000300.XSHG','000906.XSHG','000852.XSHG','399006.XSHE']
    
    #startDate=readCsv(path+'/000001.XSHG.csv').iloc[-1]['date']+timedelta(days=1)
    
    today=datetime.today().date()
    for code in indexList:
        csvFile=os.path.join(path.INDEX_PRICE,code+'.csv')
        
        startDate=readCsv(csvFile).iloc[-1]['date'].date()
        if startDate>=today:
            print('{}:指数行情已更新'.format(code))
            continue
        else:
            #print('更新指数行情:',code)
            updateObj.setCodeList([code,])
            df=updateObj.stockPrice(startDate+timedelta(days=1),today,isIndex=True)
            df.rename(columns={'time':'date'},inplace=True)          
            saveCsv(df,csvFile,isAppend=True)
    
   
    

def stockPrice(updateObj):  #更新全部A股日行情数据
    print('更新A股日行情:')
    
    newData=pd.DataFrame()
    
    today=datetime.today().date()
    #today=datetime(2021,2,5).date()
    
    column=['date','code','open','close','high','low','pre_close','volume','money','high_limit','low_limit','paused','pct_change']
    #step1:获取所有当前上市的股票代码
    stocks=SecurityType.objects.get(name='stock').mainType.filter(end_date__gt=today)#(end_date__year=2200)
    
    #step2:读取.csv文件，获取最后一条数据的日期，更新到今日
    for code in [stock.code for stock in stocks]:
        csvPath=os.path.join(path.STOCK_PRICE,code+'.csv')        
        updateObj.setCodeList([code,])
        
        if os.path.exists(csvPath):
            #print('更新股票日行情:',code)
            df=readCsv(csvPath)
            
            try:
                startDate=df.iloc[-1]['date'].date()
            except Exception as e:  #csv文件无数据
                df=updateObj.stockPrice('2021-01-01',
                                         today)
                if not df.empty:
                    df.rename(columns={'time':'date'},inplace=True)
                    df['pct_change']=(df['close']-df['pre_close'])/df['pre_close']
                    saveCsv(df[column],csvPath,isAppend=True)
            else:
                if startDate>=today:
                    #print(prefixStr+'{}已更新'.format(code))
                    continue
                else:
                    
                    df=updateObj.stockPrice(startDate+timedelta(days=1),
                                         today)
                    
                    if not df.empty:
                        df.rename(columns={'time':'date'},inplace=True)
                        df['pct_change']=(df['close']-df['pre_close'])/df['pre_close']
                        
                        newData=newData.append(df[column])
                        saveCsv(df[column],csvPath,isAppend=True)
                
        else:
            print('新股上市:{}'.format(code))
            df=updateObj.stockPrice(datetime(2021,1,1).date(),
                                    today).dropna(subset=['open','close'],how='all',inplace=True)   
            #print(df)
            if df!=None:
                if  not df.empty:
                    df.rename(columns={'time':'date'},inplace=True)
                    df['pct_change']=(df['close']-df['pre_close'])/df['pre_close']  
                    
                    newData=newData.append(df[column])          
                    saveCsv(df[column],csvPath)
        #time.sleep(0.5)
        
    #新数据更新到选股数据
#     if not newData.empty:
#         print('将更新的行情数据合并到选股数据')
#         for code,group in newData.groupby('code'):
#             selectPath=os.path.join(path.SELECT,code+'.csv')
#             if os.path.exists(selectPath):
#                 selectDf=readCsv(selectPath)
#                 name=Securities.objects.get(code=code).display_name
#                 group['name']=name
#                 selectDf=selectDf.append(group)
#                 saveCsv(selectDf,selectPath)
#             else:
#                 name=Securities.objects.get(code=code).display_name
#                 group['name']=name
#                 saveCsv(group,selectPath)

def stockFundamental(updateObj):    #更新股票的市值数据
    """
    更新股票的市值数据，用于估值
    """
    print('更新股票的市值数据:')
    today=datetime.today()
    column=['date', 'code', 'total_share', 'float_share', 'total_mv', 'circ_mv',
            'trunover', 'pe_ttm', 'pe', 'pb', 'ps_ttm', 'pcf_ttm']
    
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
    
    #step1:获取所有当前上市的股票代码,排除退市的股票
    stocks=SecurityType.objects.get(name='stock').mainType.filter(end_date__gt=today)    
    stockCodes=[stock.code for stock in stocks]
    
    startDt=(readCsv(os.path.join(path.STOCK_FUNDAMENTAL_JQ,'000001.XSHE.csv')).iloc[-1]['date'])
    
    if startDt>=today:
        print('个股每日市值数据已更新')
        return
    
    dates=[obj.date for obj in TradeDay.objects.filter(exchagne__tsCode='SSE',isOpen=True,date__range=(startDt+timedelta(days=1),today),)]
    for date in dates:
        #print('更新日期:',date)
        updateObj.setCodeList(stockCodes)  
        
        df=updateObj.getDailyBasic(date)
        
        del df['id']
        df.rename(columns=renameDict,inplace=True)
        df['date']=pd.to_datetime(df['date'])
        df['trunover']=df['trunover']/100.0
        df['total_share']=df['total_share']*10000
        df['float_share']=df['float_share']*10000
        df['total_mv']=df['total_mv']*100000000
        df['circ_mv']=df['circ_mv']*100000000        
        df=df[column]
        
        for name,group in df.groupby('code'):
            csvFile=os.path.join(path.STOCK_FUNDAMENTAL_JQ,name+'.csv')
            if os.path.exists(csvFile):
                saveCsv(group,csvFile,isAppend=True)
            else:
                saveCsv(group,csvFile)
    

def stockSwL1(updateObj):  #更新申万一级行业的股票列表
    """
    更新申万一级行业的股票列表
    """
       
    swL1Codes=[obj.code for obj in IndustryType.objects.get(name='申万一级行业').industries_set.all()]
    
    for year in range(2009,2004,-1):
        print(year)
        tradDaysObjs=TradeDay.objects.filter(exchagne__tsCode='SSE',
                                             isOpen=True,
                                             date__range=[datetime(year,1,1),datetime(year,12,31)])
        
        stocksSwL1=pd.DataFrame()
        
        filePath=os.path.join(path.SWL1_STOCKS,str(year)+'.csv')
        if os.path.exists(filePath):
            continue
        else:
            for tradDay in tradDaysObjs:        
                df=updateObj.swL1Stocks(swL1Codes,tradDay.date)
                if not df.empty:
                    stocksSwL1=stocksSwL1.append(df,ignore_index=True)
            stocksSwL1.to_csv(filePath,
                              index=False)
    

def swL1Price(updateObj):   #更新申万一级行业日行情
    """
    更新申万一级行业日行情
    """
    print('更新申万一级行业的日行情')
    column=['date', 'code', 'name', 'open', 'high', 'low', 'close', 'volume',
            'money', 'change_pct']
    codes=[obj.code for obj in IndustryType.objects.get(name='申万一级行业').industries_set.all()]
    
    today=datetime.today().date()
    
    for code in codes:
        #print(code)
        csvPath=os.path.join(path.SWL1_PRICE,code+'.csv')
        
        if os.path.exists(csvPath):
            startDt=readCsv(csvPath).iloc[-1]['date'].date()
            
            #print(startDt,today)
            if startDt>=today:
                print('无需更新')
            else:
                df=updateObj.swL1DailyPrice(code, startDt+timedelta(days=1), today)
                
                if not df.empty:
                    del df['id']
                    df['change_pct']=df['change_pct']/100.0
                    saveCsv(df[column],csvPath,isAppend=True)
        else:
            print('新的申万一级行业分类')
            df=updateObj.swL1DailyPrice(code, '2021-01-01', today)
                
            if not df.empty:
                del df['id']
                df['change_pct']=df['change_pct']/100.0
                saveCsv(df[column],csvPath)
    
def swL1Value(updateObj):
    """
    更新申万一级行业市值数据
    """
    
    print('更新申万一级行业的市值数')
    column=['date', 'code', 'name', 'turnover_ratio', 'pe', 'pb', 'average_price',
            'money_ratio', 'circulating_market_cap',
            'average_circulating_market_cap', 'dividend_ratio']
    codes=[obj.code for obj in IndustryType.objects.get(name='申万一级行业').industries_set.all()]
    
    today=datetime.today().date()
    
    for code in codes:
        #print(code)
        csvPath=os.path.join(path.SWL1_VALUE,code+'.csv')
        
        if os.path.exists(csvPath):
            startDt=readCsv(csvPath).iloc[-1]['date'].date()

            if startDt>=today:
                print('无需更新')
            else:
                df=updateObj.swL1DailyValuation(code, startDt+timedelta(days=1), today)
                
                if not df.empty:
                    df['dividend_ratio']=df['dividend_ratio']/100.0
                    df['money_ratio']=df['money_ratio']/100.0
                    df['turnover_ratio']=df['turnover_ratio']/100.0
                    saveCsv(df[column],csvPath,isAppend=True)
        else:
            print('新的申万一级行业分类')
            df=updateObj.swL1DailyValuation(code, '2021-01-01', today)
                
            if not df.empty:                
                df['dividend_ratio']=df['dividend_ratio']/100.0
                df['money_ratio']=df['money_ratio']/100.0
                df['turnover_ratio']=df['turnover_ratio']/100.0
                saveCsv(df[column],csvPath)
    

def margin(updateObj): #更新股票的融资融券
    """
    更新股票的融资融券
    """
    print('更新股票的融资融券')
    
    today=datetime.today().date()
    
    #step1：获取有融资融券标的股票
    if updateObj.checkQueryCount():
        codes=jq.get_marginsec_stocks(today)+jq.get_marginsec_stocks(today)
    else:
        print('jqdata查询余额不足，退出')
        return
         
#    print(codes)
        
    #step2：从jqdata获取数据，并保存
    startDt=readCsv(os.path.join(path.MARGIN,'000001.XSHE.csv')).iloc[-1]['date'].date()
    
    if startDt>=today:
        print('已更新')
        return 
    else:
        updateObj.setCodeList(codes)
        for tradDay in TradeDay.objects.filter(date__range=(startDt+timedelta(days=1),today),
                                               exchagne__tsCode='SSE',
                                               isOpen=True):
            print(tradDay.date)
            ret=updateObj.margin(tradDay.date)
            if not ret.empty:
                for name,group in ret.groupby('sec_code'):
                    csvFile=os.path.join(path.MARGIN,name+'.csv')
                    if os.path.exists(csvFile):
                        saveCsv(group,csvFile,isAppend=True)
                    else:
                        saveCsv(group,csvFile)
            
    

def initSwL1Valuation(updateObj):
    
    codes=[obj.code for obj in IndustryType.objects.get(name='申万一级行业').industries_set.all()]
    #print(len(codes))
        
    for year in range(2020,2004,-1):
        stratDt='{}-01-01'.format(year)
        endDt='{}-01-01'.format(year+1)
        for code in codes:
            csvFile=os.path.join(path.SWL1_VALUE,code+'_'+str(year)+'.csv')
            if os.path.exists(csvFile):
                continue
            else:
                print(csvFile)
                df=updateObj.swL1DailyValuation(code, stratDt, endDt)
                if not df.empty:
                    del df['id']
                    #print(df)
                    saveCsv(df,csvFile)
            

def dropDuplate():
    print('删除重复项，开始数据清理。。。')
    #融资融券
    for csvFile in os.listdir(path.MARGIN):
        if csvFile.endswith('.csv'):
            df=readCsv(os.path.join(path.MARGIN,csvFile))  
            df.drop_duplicates(subset=['date'], keep='first', inplace=True)  
            saveCsv(df,os.path.join(path.MARGIN,csvFile))   


if __name__=="__main__":
    
    #更新基础数据
#     updateObj=UpdataBasic() 
#          
#     tradDay(updateObj)
#     stockList(updateObj)
#          
#          
#     updateObj.logoutJq()
    
     
    #更新日行情数据
    updateObj=DailyQuotesUpdateJq()
    
    #exchangeJqdata(updateObj)
    #indexPrice(updateObj)
  
    #stockPrice(updateObj) 
    #stockFundamental(updateObj)
#       
    #hsgt(updateObj)
    #hsgtHold(updateObj)
#       
    #moneyflow(updateObj)
#     
#    stockSwL1(updateObj)
    #swL1Price(updateObj)
    #swL1Value(updateObj)
      
    margin(updateObj)
    
    #dropDuplate()
    
    updateObj.logoutJq()
    

    
    
