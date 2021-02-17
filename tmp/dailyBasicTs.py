import time
import pandas as pd
import tushare as ts

from datetime import datetime

pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数 
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.4f' % x) #不显示科学计数法

ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')

def getTradeCal(startDate='',endDate=''):
        pro=ts.pro_api()
        #SSE上交所,SZSE深交所,CFFEX 中金所,SHFE 上期所,CZCE 郑商所,DCE 大商所,INE 上能源
        df=pro.trade_cal(exchange='SSE',
                         is_open='1',
                         start_date=startDate,
                         end_date=endDate)
        return df

class UpdateDataTs():
    def __init__(self):
        self.pro=ts.pro_api()   
    
    def getStockBasic(self):
        for _ in range(3):
            try:
                """df=self.pro.stock_basic(exchange='', list_status='L',
                                        fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')"""
                df=self.pro.stock_basic(exchange='', list_status='L',)
                #上市状态： L上市 D退市 P暂停上市，默认L
            except Exception as e:
                print(e)
            else:
                return df
    
    def getDailyBasic(self,tsCode='',tradeDate='',startDate='',endDate=''):
        for _ in range(3):
            try:
                if tradeDate:
                    df=self.pro.daily_basic(
                            ts_code=tsCode,
                            trade_date=tradeDate, 
                            )
                else:
                    df=self.pro.daily_basic(
                            ts_code=tsCode,
                            start_date=startDate,
                            end_date=endDate,
                        )
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                return df
    
    def getDaily(self,tsCode='',tradeDate='',startDate='',endDate=''):
        for _ in range(3):
            try:
                if tradeDate:
                    df=self.pro.daily(ts_code=tsCode,trade_date=tradeDate)
                else:
                    df=self.pro.daily(ts_code=tsCode,start_date=startDate,end_date=endDate)
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                return df
        
if __name__=="__main__":
    upObj=UpdateDataTs()
#     dfDailyPrice=upObj.getDaily(tsCode='600230.SH,000001.SZ',tradeDate='20200107')
#     dfDailyBasic=upObj.getDailyBasic(tsCode='600230.SH,000001.SZ',tradeDate='20200107')
    #df=getTradeCal()
#     print(dfDailyPrice)
#     print(dfDailyBasic)
#     
#     dfDaily=pd.merge(dfDailyPrice,dfDailyBasic,on='ts_code')
#    print(dfDaily)
    stockList=upObj.getStockBasic()
    #print(stockList)
    
    for tsCode in stockList['ts_code']:
        print(tsCode)
        df=upObj.getDailyBasic(tsCode=tsCode)
        df.to_csv('./data/daily/dailyBasic/tushare/'+tsCode+'.csv',
                     encoding='gbk',
                     index=False,
                     float_format='%.15f',
                     )
        
