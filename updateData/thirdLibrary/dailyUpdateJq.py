"""
通过jqdata平台，更新各类日行情数据，包括：
            日行情数据：getDailyPrice(self,jqCodeList,startDate,endDate=None)              (2005至今)盘中实时更新（每3s刷新一次）
            每日市值（每日指标）数据：getDailyBasic(self,jqCodeList,date)
    
            指数行情的更新
     
            资金流向：moneyFlow(self,jqCodeList,startDate,endDate=None)                    (2010至今)盘后20:00更新
            
            陆股通流向：lgtMoneyflow(self,startDate,endDate)                                (上市至今)交易日20:30-24:00更新
            市场汇率（人民币和港币):HKHoldInfo(self,code,startDay,endDay)
            陆股通个股:HKHoldInfo(self,jqCodeList,startDay,endDay)                          (上市至今)交易日20:30-06:30更新   
     
             融资融券:margin(self,jqCodeList,startDate,endDate=None)                        (2010至今)下一个交易日10点之前更新
     
            分红拆分送股
            
            申万一级行业日行情:swL1DailyPrice(self,codeList,startDate,endDate=None)           (上市至今)交易日17:40更新
            申万一级行业的估值数据:swL1DailyValuation(self,codeList,startDate,endDate=None)    (上市至今)交易日17:40更新
     
             龙虎榜数据：topList(self,startDate,endDate=None)                                (2005至今)盘后18:00更新
             
            沪深市场每日成交概况 :exchangeTradeInfo(self,startDate,endDate)                    (2005年至今)交易日20:30-24:00更新
"""
import zhpLiangHua.djangoShell

import pandas as pd
import jqdatasdk as jq

from stock_hs_A.models import IndustryType
from updateData.thirdLibrary.base import BaseJq,BaseTs



class DailyQuotesUpdateJq(BaseJq,BaseTs):
    """
            从jqdata中获取每日更新的数据：
            日行情数据：stockPrice(self,jqCodeList,startDate,endDate=None)              (2005至今)盘中实时更新（每3s刷新一次）
            每日市值（每日指标）数据：getDailyBasic(self,jqCodeList,date)
            
             指数行情
            
            资金流向：moneyFlow(self,jqCodeList,startDate,endDate=None)                    (2010至今)盘后20:00更新
            
            陆股通流向：lgtMoneyflow(self,startDate,endDate)                                (上市至今)交易日20:30-24:00更新
            市场汇率（人民币和港币):HKHoldInfo(self,code,startDay,endDay)
            陆股通个股:HKHoldInfo(self,jqCodeList,startDay,endDay)                          (上市至今)交易日20:30-06:30更新   
     
             融资融券:margin(self,jqCodeList,startDate,endDate=None)                        (2010至今)下一个交易日10点之前更新
             获取融资融券汇总数据
            分红拆分送股
            
            申万一级行业日行情:swL1DailyPrice(self,codeList,startDate,endDate=None)           (上市至今)交易日17:40更新
            申万一级行业的估值数据:swL1DailyValuation(self,codeList,startDate,endDate=None)    (上市至今)交易日17:40更新
            申万一级行业的股票列表
     
             龙虎榜数据：topList(self,startDate,endDate=None)                                (2005至今)盘后18:00更新
             
            沪深市场每日成交概况 :exchangeTradeInfo(self,startDate,endDate)                    (2005年至今)交易日20:30-24:00更新
    """
    def __init__(self):
        BaseJq.__init__(self)
        BaseTs.__init__(self)
        #18009020072  18090679978
        #super().__init__(userName, passwd)
        
        #self.jqCodeList=self.getStockList().index.to_list()
        #self.swL1CodeList=jqCodeList if  jqCodeList else self.getIndustyList().index.to_list()
    
    def stockPrice(self,startDate,endDate=None,isIndex=False):
        """
        从jqdata，更新每日行情
        :jqCodeList 所有A股的列表，格式为jq格式
        :startDate
        :endDate 如果endDate为None，则更新指定日期startDate的日行情
        """
        
        if isIndex:
            fields=['open', 'close', 'low', 'high', 'volume', 'money', 'pre_close']
        else:
            fields=['open', 'close', 'low', 'high', 'volume', 'money', 'high_limit','low_limit', 'pre_close', 'paused']
        
        if self.checkQueryCount() and self.jqCodeList:
            if endDate:
                df=jq.get_price(self.jqCodeList,
                                start_date=startDate,
                                end_date=endDate,
                                frequency='daily',
                                panel=False,
                                fq=None,
                                fields=fields)
            else:
                df=jq.get_price(self.jqCodeList,
                                #start_date=startDate,
                                end_date=startDate,
                                frequency='daily',
                                panel=False,
                                fq='None',
                                count=1,
                                fields=fields)     
            return df
        else:
            return pd.DataFrame()
        
    def getDailyBasic(self,date):
        """
        获取每日市值指标
        :jqCodeList 股票代码的List
        :date 日期
        :return 返回查询结果df，如果查询量不足，返回空df
        """
        if self.checkQueryCount() and self.jqCodeList:
            q = jq.query(
                jq.valuation
            ).filter(
                jq.valuation.code.in_(self.jqCodeList)
            )
            df = jq.get_fundamentals(q,date)
                  
            return df
        else:
            return pd.DataFrame()
    
    def moneyFlow(self,startDate,endDate=None):
        """
        从jqdata更细资金流向信息，超大单、大单、中单、小单、主力
        :codeList 股票代码列表
        :startDate 开始时间
        :endDate 结束时间，如果结束时间为0，获取startDate当天的行情数据
        """
        if self.checkQueryCount(): #and self.jqCodeList:
            if endDate:
                df=jq.get_money_flow(self.jqCodeList, 
                                     startDate, 
                                     endDate)
            else:
                df=jq.get_money_flow(self.jqCodeList, 
                                     end_date=startDate,
                                     count=1)
            return df
        else:
            return pd.DataFrame()
        
    def lgtMoneyflow(self,startDate,endDate=None):  		#finance.STK_ML_QUOTA
        """
                    记录沪股通、深股通和港股通每个交易日的成交与额度的控制情况。
                    市场通编码    市场通名称
        310001    沪股通
        310002    深股通
        310003    港股通（沪）
        310004    港股通（深）
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.STK_ML_QUOTA).filter(jq.finance.STK_ML_QUOTA.day>=startDate,
                                                           jq.finance.STK_ML_QUOTA.day<=endDate,
                                                           )
            else:
                q=jq.query(jq.finance.STK_ML_QUOTA).filter(jq.finance.STK_ML_QUOTA.day==startDate)
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()
        
    def exchangeRate(self,startDate,endDate=None):  		#finance.STK_EXCHANGE_LINK_RATE
        """
                    人民币和港币之间的参考汇率/结算汇兑比率信息,用于计算南向资金
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.STK_EXCHANGE_LINK_RATE).filter(jq.finance.STK_EXCHANGE_LINK_RATE.day>=startDate,
                                                       jq.finance.STK_EXCHANGE_LINK_RATE.day<=endDate,
                                                       )
            else:
                q=jq.query(jq.finance.STK_EXCHANGE_LINK_RATE).filter(jq.finance.STK_EXCHANGE_LINK_RATE.day==startDate)
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()
    
    def HKHoldInfo(self,startDay,endDay=None):      		#finance.STK_EXCHANGE_LINK_RATE
        """
        记录了北向资金（沪股通、深股通）和南向资金港股通的持股数量和持股比例，数据从2017年3月17号开始至今，一般在盘前6:30左右更新昨日数据。
        问题：返回5000行数据的限制，导致无法一次性更新，更新数据时，最好一天一天更新
        """
        if self.checkQueryCount():  # and self.jqCodeList:
            if endDay:
                q=jq.query(jq.finance.STK_HK_HOLD_INFO).filter(
                    jq.finance.STK_HK_HOLD_INFO.day>=startDay,
                    jq.finance.STK_HK_HOLD_INFO.day<=endDay)
                    #jq.finance.STK_HK_HOLD_INFO.code.in_(self.jqCodeList))
            else:
                q=jq.query(jq.finance.STK_HK_HOLD_INFO).filter(
                    jq.finance.STK_HK_HOLD_INFO.day==startDay)
                    #jq.finance.STK_HK_HOLD_INFO.code.in_(self.jqCodeList))
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame() 
    
    def swL1DailyPrice(self,code,startDate,endDate=None):    	#finance.SW1_DAILY_PRICE
        """
                    申万一级行业指数的历史日行情数据，每日18:00更新。
        """
        if self.checkQueryCount():# and self.swL1CodeList:
            if endDate:
                q=jq.query(jq.finance.SW1_DAILY_PRICE).filter(
                                                    jq.finance.SW1_DAILY_PRICE.code==code,
                                                    jq.finance.SW1_DAILY_PRICE.date>=startDate,
                                                    jq.finance.SW1_DAILY_PRICE.date<=endDate)
            else:
                q=jq.query(jq.finance.SW1_DAILY_PRICE).filter(
                                                    jq.finance.SW1_DAILY_PRICE.code==code,
                                                    jq.finance.SW1_DAILY_PRICE.date==startDate)
            return jq.finance.run_query(q)
        else:
            return pd.DateFrame()
    
    def swL1Stocks(self,industryCodes,date):
        """
        申万一级行业的股票代码
        :return [{code:xx,xx,xx},...]
        """
        
        if self.checkQueryCount():   
            ret=[]         
            for code in industryCodes:
                stocks={code:','.join(jq.get_industry_stocks(code, date=date))}
                #print(stocks)
                ret.append(stocks)
                
            ret=pd.DataFrame(ret)
            ret.fillna(method='bfill',inplace=True)
            ret=ret.iloc[[0]]
            ret['date']=date
            return ret
        else:
            return pd.DataFrame()    
        
    def swL1DailyValuation(self,code,startDate,endDate=None):    #finance.SW1_DAILY_VALUATION
        """
                    申万一级行业指数的历史日行情数据，每日18:00更新。
                    有问题，官网无此数据
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.SW1_DAILY_VALUATION).filter(
                                                    jq.finance.SW1_DAILY_VALUATION.code==code,
                                                    jq.finance.SW1_DAILY_VALUATION.date>=startDate,
                                                    jq.finance.SW1_DAILY_VALUATION.date<=endDate)
            else:
                q=jq.query(jq.finance.SW1_DAILY_VALUATION).filter(
                                                        jq.finance.SW1_DAILY_VALUATION.code==code,
                                                        jq.finance.SW1_DAILY_VALUATION.date==startDate)
            return jq.finance.run_query(q)
        else:
            return pd.DateFrame()
    
    def industryStocks(self): 
        #更新到2014-2-4后，超出1000万条的限制
        dates=pd.date_range(start='2013-5-16',end='2015-1-9')
        #dates=pd.date_range(start='2021-1-9',end='2021-1-10')
        swL1=IndustryType.objects.get(name="申万一级行业").industries_set.all()
        #df=pd.DataFrame(index=dates,columns=[(industry.code,industry.name) for industry in swL1])
        df=pd.DataFrame(index=dates,columns=[industry.code for industry in swL1])
        #df=pd.DataFrame(index=dates,columns=swL1)
        try:
            for index in df.index:
                print(index)
                for col in df.columns:
                    #print(df.loc[index,col])
                    #print(index,col)
                    df.loc[index,col]=','.join(jq.get_industry_stocks(col, date=index))
                
            #print(df)
        except Exception as e:
            print(e)
            df['date']=df.index
            df.reset_index(level=0,drop=True,inplace=True)  
            df.to_csv('./data/dailyPrice/industryInfo/swL1.csv',
                  encoding='gbk')
        
        df['date']=df.index
        df.reset_index(level=0,drop=True,inplace=True)  
        
        
        df.to_csv('./data/dailyPrice/industryInfo/swL1.csv',
                  encoding='gbk')
      
        '''df=pd.read_csv('./data/dailyPrice/industryInfo/swL1.csv',
                  encoding='gbk')
        print(tuple(df.columns))'''
    
    def exchangeTradeInfo(self,startDate,endDate=None):     #finance.STK_EXCHANGE_TRADE_INFO
        """
                    沪深两市股票交易的成交情况，包括市值、成交量，市盈率等情况。
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.STK_EXCHANGE_TRADE_INFO).filter(
                    jq.finance.STK_EXCHANGE_TRADE_INFO.date>=startDate,
                    jq.finance.STK_EXCHANGE_TRADE_INFO.date<=endDate)
            else:
                q=jq.query(jq.finance.STK_EXCHANGE_TRADE_INFO).filter(
                    jq.finance.STK_EXCHANGE_TRADE_INFO.date==startDate)
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()
    
    def topList(self,startDate,endDate=None):
        """
                    获取指定日期区间内的龙虎榜数据
        """
        if self.checkQueryCount():
            if endDate:
                df=jq.get_billboard_list(None, startDate, endDate)
            else:
                df=jq.get_billboard_list(None, end_date=startDate,count=1)
            return df
        else:
            return pd.DataFrame()
    
    def margin(self,startDate,endDate=None):
        """
        获取一只或者多只股票在一个时间段内的融资融券信息
        """
        if self.checkQueryCount():# and self.jqCodeList:
            if endDate:
                #df=jq.get_mtss(self.jqCodeList, startDate, endDate)
                df=jq.get_mtss(self.jqCodeList, startDate, endDate)
            else:
                #df=jq.get_mtss(self.jqCodeList,  end_date=startDate,  count=1)
                df=jq.get_mtss(self.jqCodeList,  end_date=startDate,  count=1)
            return df
        else:
            return pd.DataFrame()
    
    def marginTotal(self,startDate,endDate=None):           #finance.STK_MT_TOTAL
        """
                    记录上海交易所和深圳交易所的融资融券汇总数据
        """
        if self.checkQueryCount():
            if endDate: 
                q=jq.query(jq.finance.STK_MT_TOTAL).filter(
                    jq.finance.STK_MT_TOTAL.date>=startDate,
                    jq.finance.STK_MT_TOTAL.date<=endDate,)
            else:
                q=jq.query(jq.finance.STK_MT_TOTAL).filter(
                    jq.finance.STK_MT_TOTAL.date==startDate)
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()
                
