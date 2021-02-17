import time
import pandas as pd
import jqdatasdk as jq

from datetime import datetime

pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数 
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.4f' % x) #不显示科学计数法
'''
Created on 2021年1月18日

@author: My
'''

class UpdataJq():
    def __init__(self,userName='18009020072',passwd='4187Xslc61'):
        jq.auth(userName,passwd)
        self.lastQueryCount=jq.get_query_count()
        print('剩余查询条数',self.lastQueryCount)
        
        if self.lastQueryCount['spare']<=1280:
            print('从jqdata查询数据的容量不足，退出')
    
    def checkQueryCount(self):
        if self.lastQueryCount['spare']<=1280:
            print('从jqdata查询数据的容量不足，退出')
            return False
        else:
            return True
        
    def logoutJq(self):
        jq.logout()
        
    def getTradeDays(self):
        if self.checkQueryCount():
            return jq.get_trade_days(start_date='2005-1-4')
        else:
            return None
    
    def getStockBasic(self):
        if self.checkQueryCount():
            stockList=jq.get_all_securities(['stock'])
            return stockList
        else:
            return []
        
    
        
    def getDailyBasic(self,jqCodeList,date):
        if self.checkQueryCount():
            q = jq.query(
                jq.valuation
            ).filter(
                jq.valuation.code.in_(jqCodeList)
            )
            df = jq.get_fundamentals(q,date)
                  
            return df
        else:
            return pd.DataFrame()
    
if __name__=="__main__":
    updataObj=UpdataJq()
    #stocks = list(jq.get_all_securities(['stock']).index)
#     df=updataObj.getDailyBasic(jqCode='000001.XSHE')
#     print(df)
    jqCodes=list(updataObj.getStockBasic().index)
    allTradeDays=updataObj.getTradeDays()
    for tradeDay in allTradeDays:
        print(tradeDay.strftime('%Y-%m-%d'))
        df=updataObj.getDailyBasic(jqCodes,tradeDay)
        if not df.empty:
            df.to_csv('./data/daily/dailyBasic/jqdata/'+tradeDay.strftime('%Y-%m-%d')+'.csv',
                      encoding='gbk',
                      index=False,
                      float_format='%.15f',)
        
    
    updataObj.logoutJq()
        