'''
Created on 2021年1月24日

@author: Administrator

择时进行，更新每季度数据
'''

import zhpLiangHua.djangoShell

import os
from datetime import datetime,timedelta

from updateData.thirdLibrary.basic import UpdataBasic
from stock_hs_A.models import TradeDay,Securities,SecurityType
#from updateData.thirdLibrary.dailyUpdateJq import DailyQuotesUpdateJq

"""
基础数据：
    指数列表
    申万、证监会行业列表
"""

def indexList(updateObj):   #更新指数列表
    """
    更新股票列表
    """
    updateObj.indexList()
    updateObj.industry()

    

if __name__=="__main__":
    
    #更新基础数据
    updateObj=UpdataBasic() 
    
    
    updateObj.logoutJq()