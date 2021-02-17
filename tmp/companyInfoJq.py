import pandas as pd
from datetime import datetime

import jqdatasdk as jq
from study.baseJq import BaseJq
'''
Created on 2021年1月22日

@author: My
'''

pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.4f' % x) #不显示科学计数法

class CompanyInfo(BaseJq):
    def __init__(self,jqCodeList=None):
        super().__init__()
    
    def companyInfo(self):
        pass
    
    def holderTop10(self,startDate,endDate=None):
        """
                   上市公司前十大股东的持股情况，包括持股数量，所持股份性质，变动原因等。
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.STK_SHAREHOLDER_TOP10).filter(
                    jq.finance.STK_SHAREHOLDER_TOP10.code.in_(self.jqCodeList),
                    jq.finance.STK_SHAREHOLDER_TOP10.pub_date>=startDate,
                    jq.finance.STK_SHAREHOLDER_TOP10.pub_date<=endDate,)
            else:
                q=jq.query(jq.finance.STK_SHAREHOLDER_TOP10).filter(
                    jq.finance.STK_SHAREHOLDER_TOP10.code.in_(self.jqCodeList),
                    jq.finance.STK_SHAREHOLDER_TOP10.pub_date>=startDate,
                    jq.finance.STK_SHAREHOLDER_TOP10.pub_date<=datetime.today())
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()
    
    def floatingHodlderTop10(self,startDate,endDate=None):
        """
                   获取上市公司前十大流通股东的持股情况，包括持股数量，所持股份性质，变动原因等。
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.STK_SHAREHOLDER_FLOATING_TOP10).filter(
                    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.code.in_(self.jqCodeList),
                    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.pub_date>=startDate,
                    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.pub_date<=endDate,)
            else:
                q=jq.query(jq.finance.STK_SHAREHOLDER_TOP10).filter(
                    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.code.in_(self.jqCodeList),
                    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.pub_date>=startDate,
                    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.pub_date<=datetime.today())
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()
    
    def sharePlege(self):
        pass
    
    def holderNum(self,startDate,endDate=None):
        """
                   获取上市公司全部股东户数，A股股东、B股股东、H股股东的持股户数
        """
        if self.checkQueryCount():
            if endDate:
                q=jq.query(jq.finance.STK_HOLDER_NUM).filter(
                    jq.finance.STK_HOLDER_NUM.code.in_(self.jqCodeList),
                    jq.finance.STK_HOLDER_NUM.pub_date>=startDate,
                    jq.finance.STK_HOLDER_NUM.pub_date<=endDate,)
            else:
                q=jq.query(jq.finance.STK_HOLDER_NUM).filter(
                    jq.finance.STK_HOLDER_NUM.code.in_(self.jqCodeList),
                    jq.finance.STK_HOLDER_NUM.pub_date>=startDate,
                    jq.finance.STK_HOLDER_NUM.pub_date<=datetime.today())
            return jq.finance.run_query(q)
        else:
            return pd.DataFrame()

if __name__=="__main__":
    comObj=CompanyInfo(['600276.XSHG'],)
    df=comObj.holderTop10(startDate='1990-12-19')
    print(df)