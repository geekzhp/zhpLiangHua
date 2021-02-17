'''
Created on 2021年1月30日

@author: Administrator

择时框架的主程序
'''
import zhpLiangHua.djangoShell

import os
import pandas as pd

from utils.file import readCsv
from utils.calculation import calAdjustPrice,priceLimit

from stock_hs_A.models import Securities
from zhpLiangHua.dataPath import STOCK_PRICE
from timingStrategy.singals import signalMa,signalMaParaList
from timingStrategy import timingFunc
#from updateData.thirdLibrary.dailyUpdateJq import DailyQuotesUpdateJq

import utils.pandasSetting

pd.set_option('display.max_rows', 500)  # 最多显示数据的行数



#df=df[(df['date']>='2005-01-01') & (df['date']<='2019-04-09')]
# df.reset_index(drop=True,inplace=True)
#print(df)

def demo(df):
    if df.shape[0]<250:
        print('上市不足一年，不运行择时策略')
        exit()
    
        
    #计算复权价
    df=calAdjustPrice(df)
    
    #计算涨跌停价
    df=priceLimit(df)
    
    #第二模块：产生交易信号
    para=(10,90)
    df=signalMa(df,para=para)
    
    
    #第三模块：根据交易信号计算每天的仓位
    df=timingFunc.position(df)
    #print(df[df['pos']==1.0])
    
    #截取上市一年后的数据，股票刚上市，会疯涨一段时间，对后面的回测有一定的影响，不是正常的交易区间
    df=df.iloc[250-1:]
    #截取2007年之后的数据，2007年后经历了一轮牛市，经历两轮牛市；2007年股权分值改革，A股进入全流通时代，选择2007年之后的数据回测也是行规
    df=df[df['date']>=pd.to_datetime('2007-01-01')]
    
    
    #第四个模块：计算资金曲线
    df=timingFunc.calcuEquityCurve(df)
    
    equityCurve=df.iloc[-1]['equityCurve']
    equityCurveBase=df.iloc[-1]['equityCurveBase']
    
    print('双均线择时策略，参数:{},回测时间(start:{},end:{})运行后的最终收益为:{},股票原收益为:{}'.format(
        para,df.iloc[0]['date'],df.iloc[-1]['date'],equityCurve,equityCurveBase))

def choosePara(df):
    #计算复权价
    df=calAdjustPrice(df)
    
    #计算涨跌停价
    df=priceLimit(df)
    
    paraList=signalMaParaList(maShort=range(10,200,10),maLong=range(10,300,10))
    
    rtn=pd.DataFrame()
    for para in paraList:
        tmpDf=signalMa(df.copy(),para=para)
        tmpDf=timingFunc.position(tmpDf)
        tmpDf=tmpDf.iloc[250-1:]
        tmpDf=tmpDf[tmpDf['date']>=pd.to_datetime('2007-01-01')]
        tmpDf=timingFunc.calcuEquityCurve(tmpDf, initMoney=1000000,slippage=0.01,cRate=2.5/10000,tRate=1.0/1000)
        
        equityCurve=tmpDf.iloc[-1]['equityCurve']
        equityCurveBase=tmpDf.iloc[-1]['equityCurveBase']
        print(para,'策略最终收益',equityCurve)
        
        rtn.loc[str(para),'equityCurve']=equityCurve
        rtn.loc[str(para),'equityCurveBase']=equityCurveBase
    
    print(rtn.sort_values(by='equityCurve',ascending=False))
    
if __name__=="__main__":
    #第一模块:准备数据
    #obj=Securities.objects.get(display_name='万科A')  #万科A 特锐德
    
    #df=readCsv(os.path.join(STOCK_PRICE,obj.code+'.csv'))
    df=pd.read_csv('./data/sz000002_k.csv',encoding='gbk',skiprows=1,parse_dates=['交易日期'])
    df.rename(columns={'股票代码':'code','股票名称':'name','交易日期':'date','开盘价':'open','最高价':'high','最低价':'low','收盘价':'close','前收盘价':'pre_close','成交量':'volume','成交额':'money'},inplace=True)
    #对数据进行清洗和整理，防止出错
    df.sort_values(by=['date'],inplace=True)
    df.drop_duplicates(subset=['date'], keep='first', inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    #demo(df)
    choosePara(df)
