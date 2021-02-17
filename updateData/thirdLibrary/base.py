'''
数据接口的初始化
    BaseJq:初始化jqdata
    BaseTs:初始化Tushare
    
Created on 2021年1月18日

@author: My
'''


import pandas as pd
import jqdatasdk as jq
import tushare as ts


class BaseJq():
    """
    从jqdata获取数据的基础类，完成基础设置
    """
    def __init__(self,userName='18009020072',passwd='4187Xslc61',jqCodeList=None): #
        """
        :username
            18009020072  
            18090679978
            
        :jqCodeList 需要获取采集数据的股票代码列表，格式为jqdata
        
        :lastQueryCount 剩余的查询条数，返回字典格式，{'total': 10000000, 'spare': 0}
        
        :return 如果查询剩余条数不足，返回，并且写入log、微信提示
        
        未完成：
            日志功能
            微信提示
        """
        jq.auth(userName,passwd)
        self.lastQueryCount=jq.get_query_count()
        
        print('剩余查询条数',self.lastQueryCount)
        
        self.jqCodeList=jqCodeList
        
        if self.lastQueryCount['spare']<=1280:
            print('从jqdata查询数据的容量不足，退出')
            return None
        
    def logoutJq(self):
        """
        通常情况下，与类的初始化搭配使用，释放资源
        """
        print('从jqdata查询数据剩余条数',self.lastQueryCount)
        jq.logout()
        
    def setCodeList(self,jqCodeList):
        """
        设置A股个股的jqCodeList，格式为List
        """
        self.jqCodeList=jqCodeList
    
    def checkQueryCount(self):
        """
        查询剩余条数
        :return 剩余条数不足，返回False，否则True
        """
        if self.lastQueryCount['spare']<=1280:
            print('从jqdata查询数据的容量不足，退出')
            return False
        else:
            return True
        
    
    
    def getTradeDays(self):
        """
        获取交易日历，jqdata的数据从2005-1-4开始更新
        """
        if self.checkQueryCount():
            return jq.get_trade_days(start_date='2005-1-4')
        else:
            return []
        
    def getStockList(self):
        """
        从jqdata网站，获取股票列表
        :return 含有股票列表信息的DataFrame
        """
        if self.checkQueryCount():
            stockList=jq.get_all_securities(['stock'])
            return stockList
        else:
            return pd.DataFrame()
    
    def getIndustyList(self,industryTypeStr='sw_l1'):
        """
        :return 返回行业列表的DataFrame，默认申万一级行业列表
        """
        if self.checkQueryCount():
            return jq.get_industries(name=industryTypeStr, date=None)
        else:
            return pd.DataFrame()
        
class BaseTs():
    def __init__(self):
        ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')
        self.tsPro=ts.pro_api()

if __name__=="__main__":
    obj=BaseJq()
    swL1Df=obj.getIndustyList()
    print(swL1Df)
    obj.logoutJq()