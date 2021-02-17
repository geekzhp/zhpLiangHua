"""
通过jqdata平台，完成数据的初始化操作，通常只会运行一次
初始化后的数据，通常为csv文件，保存到特定的文件目录中
"""
import os
import time
import tushare as ts

from study.utils.path import mkdirs
from study.utils.convert import normalize_code
from study.dailyUpdateJq import DailyUpdateJq
from study.companyInfoJq import CompanyInfo

ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')

def initDailyBasic():
    """
          首次更新每日市值数据
         存储位置：/data/daily/dailyBasic/jqdata
         存储格式：每日全A股的市值数据
    """
    updataObj=DailyUpdateJq()
    
    #获取所有的股票代码和交易日
    jqCodes=list(updataObj.getStockBasic().index)
    allTradeDays=updataObj.getTradeDays()    
    
    #设置.csv文件保存路径
    dailyBasicPath=mkdirs(os.path.join(mkdirs('data'),'daily','dailyBasic','jqdata'))
    print(dailyBasicPath)
    
    for tradeDay in allTradeDays:
        print(tradeDay.strftime('%Y-%m-%d'))
        dailyBasicFile=os.path.join(dailyBasicPath,tradeDay.strftime('%Y-%m-%d'))
        
        if os.path.isfile(dailyBasicFile):
            print('文件已经存在，跳过',dailyBasicFile)
            continue
        
        try:
            print(dailyBasicFile)
            df=updataObj.getDailyBasic(jqCodes,tradeDay)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(updataObj.lastQueryCount,e))
        else:
            if not df.empty:
                df.to_csv('./data/daily/dailyBasic/jqdata/'+tradeDay.strftime('%Y-%m-%d')+'.csv',
                          encoding='gbk',
                          index=False,
                          float_format='%.15f',)
    updataObj.logoutJq()
    
def initLgtMoneyflowByJq():
    """
          首次更新沪深股通的每日流向数据
         存储位置：/data/daily/hsgt/moneyflow/jqdata
         存储格式：按年存储，记录每日的陆股通数据流向
    """
    obj=DailyUpdateJq()
    
    #设置.csv文件保存路径
    hsgtPath=mkdirs(os.path.join(mkdirs('data'),'daily','hsgt','moneyflow','jqdata'))
    print(hsgtPath)
    
    for year in range(2014,2021):
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        moneyflowFile=os.path.join(hsgtPath,'{}.csv'.format(year))
       
        if os.path.isfile(moneyflowFile):
            print('文件已经存在，跳过',moneyflowFile)
            continue
        
        try:
            print(moneyflowFile)
            his=obj.lgtMoneyflow(startDate, endDate)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
        else:
            if not his.empty:
                his.to_csv(moneyflowFile,encoding='gbk',
                          index=False,
                          float_format='%.15f',)
        time.sleep(1) 
    obj.logoutJq()

def initExchangRateByJq():
    """
          首次更新沪深股通的每日市场汇率数据
         存储位置：/data/daily/hsgt/moneyflow/jqdata
         存储格式：按年存储，记录每日的陆股通数据流向
    """
    obj=DailyUpdateJq()
    
    #设置.csv文件保存路径
    hsgtPath=mkdirs(os.path.join(mkdirs('data'),'daily','hsgt','moneyflow','jqdata'))
    print(hsgtPath)
    
    for year in range(2014,2021):
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        exchangeRateFile=os.path.join(hsgtPath,'{}_rate.csv'.format(year))
        
        if os.path.isfile(exchangeRateFile):
            print('文件已经存在，跳过',exchangeRateFile)
            continue
        
        try:
            print(exchangeRateFile)
            his=obj.exchangeRate(startDate, endDate)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
        else:
            if not his.empty:
                his.to_csv(exchangeRateFile,encoding='gbk',
                          index=False,
                          float_format='%.15f',)
        time.sleep(1) 
    obj.logoutJq()

def initHKHoldInfo():
    """
          首次更新沪深股通的个股数据
         存储位置：/data/daily/hsgt/HKHold/jqdata
         存储格式：按个股年份存储，记录每日的陆股通数据流向
    """
    pro=ts.pro_api()
    
    #从tushare获取所有带有陆股通标识的股票代码，转换成jq格式
    stcokLgt=pro.stock_basic(exchange='', list_status='L', is_hs='H').append(
        pro.stock_basic(exchange='', list_status='L', is_hs='S'),
        ignore_index=True)
    
    lgtStocks=[normalize_code(code) for code in stcokLgt['ts_code'].tolist()]
    
    obj=DailyUpdateJq()

    hsgtHoldPath=mkdirs(os.path.join(mkdirs('data'),'daily','hsgt','HKHold','jqdata'))
    print(hsgtHoldPath)
    
    for year in range(2019,2013,-1):
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)

        for asset in lgtStocks:
            print(asset,startDate,endDate)
            
            hsgtHoldFile=os.path.join(hsgtHoldPath,'{}_{}.csv'.format(asset,year))
            if os.path.isfile(hsgtHoldFile):
                print('文件已经存在，跳过',hsgtHoldFile)
                continue
            try:
                #print(hsgtHoldFile)
                his=obj.HKHoldInfo(asset,startDate, endDate)
            except Exception as e:
                print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
            else:
                if not his.empty:
                    his.to_csv(hsgtHoldFile,encoding='gbk',
                              index=False,
                              float_format='%.15f',)
            time.sleep(1)
    obj.logoutJq()

def initMoneyFlow():
    """
          首次更新A股的个股资金流向
         存储位置：/daily/moneyFlow/jqdata/
         存储格式：按个股年份存储，记录个股的每日资金流向
    """
    obj=DailyUpdateJq()
    
    #从tushare获取所有的上市公司的股票代码
#     pro=ts.pro_api()
#     stockList=pro.stock_basic(exchange='', list_status='L')    
#     stockList=[normalize_code(code) for code in stockList['ts_code'].tolist()]
    
    #获取所有的股票代码和交易日
    jqCodes=list(obj.getStockBasic().index)
    
    #设置.csv文件保存路径
    moneyPath=mkdirs(os.path.join(mkdirs('data'),'daily','moneyFlow','jqdata'))
    print(moneyPath)
    
    for year in range(2019,2013,-1):
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)

        for asset in jqCodes:
            print(asset,startDate,endDate)
            
            moneyFlowFile=os.path.join(moneyPath,'{}_{}.csv'.format(asset,year))
            if os.path.isfile(moneyFlowFile):
                print('文件已经存在，跳过',moneyFlowFile)
                continue
            try:
                #print(hsgtHoldFile)
                his=obj.moneyFlow([asset,], startDate,endDate)
            except Exception as e:
                print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
            else:
                if not his.empty:
                    his.to_csv(moneyFlowFile,
                               encoding='gbk',
                               index=False,
                               float_format='%.15f',)
            time.sleep(1)
    
    obj.logoutJq()

def initExchangeTradInfo():
    """
         首次更新上交所、深交所及各市场的市值、成交数据
         存储位置：/data/daily/exchange/jqdata
         存储格式：按年存储
    """
    obj=DailyUpdateJq()
    
    #设置.csv文件保存路径
    moneyPath=mkdirs(os.path.join(mkdirs('data'),'daily','exchange','jqdata'))
    print(moneyPath)
    
    for year in range(2020,2004,-1):
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        exchangeFile=os.path.join(moneyPath,'{}.csv'.format(year))
        
        if os.path.isfile(exchangeFile):
            print('文件已经存在，跳过',exchangeFile)
            continue
        try:
            print(exchangeFile)
            df=obj.exchangeTradeInfo(startDate,endDate)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
        else:
            if not df.empty:
                df.to_csv(exchangeFile,
                          encoding='gbk',
                          index=False,
                          float_format='%.15f',)
        time.sleep(1)
        
    obj.logoutJq()

def initSwL1DailyPrice():
    """
         首次获取申万一级行业的日行情数据
         存储位置：/data/daily/swL1/dailyPrice/jqdata
         存储格式：按照每个行业按年存储
    """
    obj=DailyUpdateJq()
    
    #获取申万一级行业目录的code
    swL1Codes=obj.industyList().index.to_list()
    
    #设置.csv文件保存路径
    swL1PricePath=mkdirs(os.path.join(mkdirs('data'),'daily','swL1','dailyPrice','jqdata'))
    
    for year in range(2020,2004,-1): 
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        for code in swL1Codes:
            swL1PriceFile=os.path.join(swL1PricePath,'{}_{}.csv'.format(code,year))
            
            if os.path.isfile(swL1PriceFile):
                print('文件已经存在，跳过',swL1PriceFile)
                continue
            try:
                print(swL1PriceFile)
                df=obj.swL1DailyPrice([code,], startDate, endDate)
            except Exception as e:
                print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
            else:
                if not df.empty:
                    df.to_csv(swL1PriceFile,
                          encoding='gbk',
                          index=False,
                          float_format='%.15f',)
                
            time.sleep(1)
    obj.logoutJq()

def initSwL1DailyValuation():
    """
         首次获取申万一级行业的估值情数据
         存储位置：/data/daily/swL1/dailyValuelation/jqdata
         存储格式：按照每个行业按年存储
    """
    obj=DailyUpdateJq()
    
    #获取申万一级行业目录的code
    swL1Codes=obj.industyList().index.to_list()
    
    #设置.csv文件保存路径
    swL1ValuationPath=mkdirs(os.path.join(mkdirs('data'),'daily','swL1','dailyValuelation','jqdata'))
    
    for year in range(2020,2004,-1): 
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        for code in swL1Codes:
            swL1ValuationFile=os.path.join(swL1ValuationPath,'{}_{}.csv'.format(code,year))
            
            if os.path.isfile(swL1ValuationFile):
                print('文件已经存在，跳过',swL1ValuationFile)
                continue
            try:
                print(swL1ValuationFile)
                df=obj.swL1DailyValuation([code,], startDate, endDate)
            except Exception as e:
                print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
            else:
                if not df.empty:
                    df.to_csv(swL1ValuationFile,
                          encoding='gbk',
                          index=False,
                          float_format='%.15f',)
                
            time.sleep(1)
    obj.logoutJq()

def initTopList():
    """
          首次龙虎榜数据
         存储位置：/data/daily/topList/jqdata
         存储格式：按照每年存储   
          注意： 2005年、2006年的csv文件编码为:utf8 
    """
    obj=DailyUpdateJq()
    
    #设置.csv文件保存路径
    topListPaht=mkdirs(os.path.join(mkdirs('data'),'daily','topList','jqdata'))
    
    for year in range(2020,2004,-1): 
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)
        
        topListFile=os.path.join(topListPaht,'{}.csv'.format(year))
        
        if os.path.isfile(topListFile):
            print('文件已经存在，跳过',topListFile)
            continue
        try:
            print(topListFile)
            df=obj.topList(startDate, endDate)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
        else:
            if not df.empty:
                df.to_csv(topListFile,
                        encoding='gbk',
                        index=False,
                        float_format='%.15f',)
                
        time.sleep(1)
    
    obj.logoutJq()

def initMarin():
    """
          首次融资融券数据
         存储位置：/data/daily/margin/jqdata
         存储格式：按照每个股票每年存储   
    """
    
    obj=DailyUpdateJq()
    
    #获取所有的股票代码
    jqCodes=list(obj.getStockList().index)
    
    #设置.csv文件保存路径
    marginPath=mkdirs(os.path.join(mkdirs('data'),'daily','margin','jqdata'))
    print(marginPath)
    
    for year in range(2020,2009,-1):
        startDate='{}-01-01'.format(year)
        endDate='{}-01-02'.format(year+1)

        for asset in jqCodes:
            print(asset,startDate,endDate)
            
            marginFile=os.path.join(marginPath,'{}_{}.csv'.format(asset,year))
            if os.path.isfile(marginFile):
                print('文件已经存在，跳过',marginFile)
                continue
            
            try:
                print(marginFile)
                his=obj.margin([asset,], startDate,endDate)
            except Exception as e:
                print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
            else:
                if not his.empty:
                    his.to_csv(marginFile,
                               encoding='gbk',
                               index=False,
                               float_format='%.15f',)
            time.sleep(1)
    obj.logoutJq()
    

def initHolderTop10():
    obj=CompanyInfo()
    
    #获取所有的股票代码
    jqCodes=list(obj.getStockList().index)
    
    #设置.csv文件保存路径 /data/companyInfo/holderTop10
    holderTop10Path=mkdirs(os.path.join(mkdirs('data'),'companyInfo','holderTop10','jqdata'))
    print(holderTop10Path)
    
    for asset in jqCodes:
        print(asset)
        holderTop10File=os.path.join(holderTop10Path,'{}.csv'.format(asset))
        
        if os.path.isfile(holderTop10File):
            print('文件已经存在，跳过',holderTop10File)
            continue
        try:
            obj.setCodeList([asset,])
            df=obj.holderTop10(startDate='1990-12-19')
            del df['id']
            #print(df)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
        else:
            if not df.empty:
                df.to_csv(holderTop10File,
                            #encoding='gbk',
                            index=False,
                            float_format='%.15f',)
        time.sleep(1)

def initFloatingHolderTop10():
    """
    utf-8的编码
    """
    obj=CompanyInfo()
    
    #获取所有的股票代码
    jqCodes=list(obj.getStockList().index)
    
    #设置.csv文件保存路径 /data/companyInfo/floatingHolderTop10/jqdata
    floatingHolderTop10Path=mkdirs(os.path.join(mkdirs('data'),'companyInfo','floatingHolderTop10','jqdata'))
    print(floatingHolderTop10Path)
    
    for asset in jqCodes:
        print(asset)
        floatingHolderTop10File=os.path.join(floatingHolderTop10Path,'{}.csv'.format(asset))
        
        if os.path.isfile(floatingHolderTop10File):
            print('文件已经存在，跳过',floatingHolderTop10File)
            continue
        try:
            obj.setCodeList([asset,])
            df=obj.holderTop10(startDate='1990-12-19')
            del df['id']
            #print(df)
        except Exception as e:
            print('剩余查询条数:{},错误信息{}'.format(obj.lastQueryCount,e))
        else:
            if not df.empty:
                df.to_csv(floatingHolderTop10File,
                            #encoding='gbk',
                            index=False,
                            float_format='%.15f',)
        time.sleep(1)
                
    
if __name__=="__main__":
    #initExchangRateByJq()
    #initHKHoldInfo()
    #initMoneyFlow()
    #initExchangeTradInfo()
    #initSwL1DailyValuation()
    #initSwL1DailyPrice()
    #initTopList()
    #initMarin()
    
    initHolderTop10()
    #initFloatingHolderTop10()