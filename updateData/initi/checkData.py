# -*- coding: utf-8 -*-
import zhpLiangHua.djangoShell

import os
import time
import numpy as np
import pandas as pd
import tushare as ts
from datetime import datetime

import zhpLiangHua.dataPath as path
from utils.path import mkdirs
from utils.file import readCsv,saveCsv
from utils.convert import normalize_code,jqcodeToXbxCode
from zhpLiangHua.dataPath import STOCK_FUNDAMENTAL_JQ,STOCK_PRICE
from stock_hs_A.models import TradeDay


class CheckData():
    
    def __init__(self):
        pass
    
    def checkIndex(self):
        """
        检查指数行情数据，确保与交易日的数据相吻合
        """
        #获取数据库的交易日数据
        tradDaysSet=set([obj.date for obj in TradeDay.objects.filter(exchagne__tsCode='SSE',isOpen=True)])    
            
        indexDates=readCsv(os.path.join(path.INDEX_PRICE,'000001.XSHG.csv'))['date'].dt.date
        
        if not indexDates.is_unique:
            print('上证指数行情日期不唯一，请检查')
        else:
            if not set(indexDates)==tradDaysSet:
                print('上证指数行情日期与数据库交易日期不一致，请检查,不一致的日期数据:{}'.format(tradDaysSet^set(indexDates)))
            else:
                print('上证指数行情数据检查完毕：合格')
                
        
        #print(tradDaysSet-indexDatesSet)
        
    
    def checkDailyPrice(self):
        """
        检查个股的日行情确保：
        1）日期唯一
        2）日期与上证指数相吻合
        """
        indexDF=readCsv(os.path.join(path.INDEX_PRICE,'000001.XSHG.csv'))
        
        for csvFile in os.listdir(path.STOCK_PRICE):
            print(os.path.join(path.STOCK_PRICE,csvFile))
            df=readCsv(os.path.join(path.STOCK_PRICE,csvFile))
            
            startDt=max(df.iloc[0]['date'].date(),datetime(2001,1,4).date())
            endDt=df.iloc[-1]['date'].date()
            
            print(startDt)
            
#             tradDaysSet=set([obj.date for obj in TradeDay.objects.filter(exchagne__tsCode='SSE',
#                                                                          date__range=(startDt,endDt),
#                                                                          isOpen=True)])    
            
            set(df.loc[df['date']>=datetime(2001,1,4).date()]['date'].dt.date) ^ set(indexDF.loc[(indexDF['date']>=startDt) & (indexDF['date']<=endDt)]['date'].dt.date)
            break
        
    def checkPctChange(self):
            code='600627.XSHG'
            df=readCsv(os.path.join(path.STOCK_PRICE,code+'.csv'))
            print(df[(df['date']>'2008-10-01') & (df['date']<='2008-11-30')])
            #print(df[df['pct_change']==-0.004136893569010924])
        
if __name__=="__main__":
    checkObj=CheckData()
    
    checkObj.checkPctChange()
    #checkObj.checkDailyPrice()
    