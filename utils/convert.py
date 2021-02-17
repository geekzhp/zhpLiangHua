import os
import pandas as pd
from datetime import datetime,timedelta

from zhpLiangHua import dataPath as path
from utils.const import _const
from utils.file import readCsv

import utils.pandasSetting


class EXCHANGE(_const):
    XSHG = 'XSHG'   #上海证券交易所
    SSE = 'XSHG'    #上海证券交易所
    SH = 'XSHG'     #上海证券交易所
    XSHE = 'XSHE'   #深圳证券交易所
    SZ = 'XSHE'     #深圳证券交易所
    SZE = 'XSHE'    #深圳证券交易所

def jqcodeToXbxCode(jqCode):
    """
    sz000001
    """
    jqCodeSplit=jqCode.split('.')
    convert={'XSHE':'sz','XSHG':'sh'}
    return convert[jqCodeSplit[1]]+jqCodeSplit[0]
    

def gbkToUtf8(rootPath):  
    """
    将gbk编码的.csv文件转换成utf8编码的.csv文件
    """ 
    for file in os.listdir(rootPath):
        if file.endswith('.csv'):            
            filePath=os.path.join(rootPath,file)
            print(filePath)
            df=pd.read_csv(filePath, 
                           encoding='gbk',)
    
            df.to_csv(filePath,
                      float_format='%.15f',
                      index=False,)

def normalize_code(symbol, pre_close=None):
    """
         归一化证券代码
         2009年全国金融标准化技术委员会采标ISO 10383:2003 (Market Identification Code)为国家标准《证券和相关金融工具交易所和市场识别码》（GB/T23696-2009）
                    其中XSHG 代表 Shan(g)hai，XSHE 代表 Sh(e)nzhen。用来区别只使用6位代码的时候出现代码重名的问题。例如代码 000001，在上交所代表上证指数，在深交所则代表平安银行。                    
                    而按照此国家标准，代码全称 000001.XSHE 则代表深交所的平安银行，000001.XSHG 则代表上证指数。                    
                    为此常见的量化平台，例如聚宽提供了 API 函数 ，来进行常规的‘sh000001’，‘600519’等证券代码向ISO 10383:2003 (Market Identification Code)的归一化处理。

    :param code 如000001
    :return 证券代码的全称 如000001.XSHE
    """
    if (not isinstance(symbol, str)):
        return symbol
    
    #处理tushare转jqdata
    if (symbol.endswith('SH') and len(symbol)==9):
        ret_normalize_code = '{}.{}'.format(symbol[0:6], EXCHANGE.SH)
    elif(symbol.endswith('SZ') and len(symbol)==9):
        ret_normalize_code = '{}.{}'.format(symbol[0:6], EXCHANGE.SZ)
    elif (symbol.startswith('sz') and (len(symbol) == 8)):
        ret_normalize_code = '{}.{}'.format(symbol[2:8], EXCHANGE.SZ)
    elif (symbol.startswith('sh') and (len(symbol) == 8)):
        ret_normalize_code = '{}.{}'.format(symbol[2:8], EXCHANGE.SH)
    elif (symbol.startswith('00') and (len(symbol) == 6)):
        if ((pre_close is not None) and (pre_close > 2000)):
            # 推断是上证指数
            ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SH)
        else:
            ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SZ)
    elif ((symbol.startswith('399') or symbol.startswith('159') or \
        symbol.startswith('150')) and (len(symbol) == 6)):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SH)
    elif ((len(symbol) == 6) and (symbol.startswith('399') or \
        symbol.startswith('159') or symbol.startswith('150') or \
        symbol.startswith('16') or symbol.startswith('184801') or \
        symbol.startswith('201872'))):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SZ)
    elif ((len(symbol) == 6) and (symbol.startswith('50') or \
        symbol.startswith('51') or symbol.startswith('60') or \
        symbol.startswith('688') or symbol.startswith('900') or \
        (symbol == '751038'))):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SH)
    elif ((len(symbol) == 6) and (symbol[:3] in ['000', '001', '002', 
                                                 '200', '300'])):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SZ)
    else:
        print(symbol)
        ret_normalize_code = symbol

    return ret_normalize_code


def transferPeriodData(df,ruleType='M'):
    #print(df)
    """
    选股框架中，将日线数据转换为其他周期的数据
    :param df
    :param ruleType
    :return 聚合后的周期data
            ['date', 'code', 'name', 'paused', 'next_paused', 'next_open_high_limit',
           'next_one_high_limit', 'next_st', 'next_delist',
           'next_daily_pct_change','exchange_trad_days', 'trad_days',
           'ervery_day_pct_change']
           因子: 'total_mv' 'circ_mv':'last',
    """
       
    
    # 将交易日期设置为index
    df['last_date']=df['date']                  #为了记录周期最后的交易日期，而不是使用resample后的date
    df.set_index('date',inplace=True)
    
    periodDf=df.resample(rule=ruleType).agg({
            # 必须列
            'last_date': 'last',                #周期最后交易日
            'code': 'last',                     #股票代码
            'name': 'last',                     #股票名称
            'paused': 'last',                   #是否交易
            
            'next_day_paused': 'last',              #下日_是否交易
            'next_day_open_high_limit': 'last',     #下日_开盘涨停
            'next_day_one_high_limit': 'last',      #下日_一字涨停
            'next_day_st': 'last',                  #下日_是否ST
            'next_day_delist': 'last',              #下日_是否退市
            'next_day_pct_change': 'last',    #下日_开盘买入涨跌幅

            # 因子列
            'total_mv': 'last',                 #总市值
            'circ_mv':'last',                   #流通市值
        }
        )
    
    # 计算必须额外数据
    periodDf['exchange_trad_days']=df['code'].resample(ruleType).size()
    periodDf['trad_days']=periodDf['exchange_trad_days']-df['paused'].resample(ruleType).sum()
    periodDf=periodDf[periodDf['exchange_trad_days']>0] ## 有的时候整个周期不交易（例如春节、国庆假期），需要将这一周期删除
     
    # 计算其他因子(周期相关)
    periodDf['pct_change']=df['pct_change'].resample(rule=ruleType).apply(lambda x:(x+1.0).prod() - 1.0)    #周期涨跌幅
    periodDf['trunover']=df['money'].resample(rule=ruleType).sum()/periodDf['circ_mv']                      #周期换手率
    
    periodDf['ampitude_20_1']=df['ampitude_20_1'].resample(rule=ruleType).mean()                            #振幅1
    periodDf['ampitude_20_2']=df['ampitude_20_2'].resample(rule=ruleType).mean()                            #振幅2
     
    # 计算周期资金曲线
    periodDf['ervery_day_pct_change']=df['pct_change'].resample(ruleType).apply(lambda x:list(x))
     
    
    # 重新设定index
    periodDf.reset_index(inplace=True)
    periodDf['date']=periodDf['last_date']
    del periodDf['last_date']
   
    return periodDf
    


def periodConvert(dailyPrice,ruleType='1W'):
#   #方法1
    dailyPrice.set_index(['date'],inplace=True)
    # 将日线数据转换成周线数据
    # 1.进行转换，用一周中最后一个交易日的变量值，赋值给周线每个变量值
    # 2.周线的【涨跌额】等于一周中每日【涨跌额】相加
    # 3.周线的【涨跌幅】等于一周中每日【涨跌幅】相乘
    # 4.周线的【开盘价】等于一周中第一个交易日的【开盘价】
    # 5.周线的【最高价】等于一周中【最高价】的最大值
    # 6.周线的【最低价】等于一周中【最低价】的最小值
    # 7.周线的【成交量】等于一周中【成交量】相加
    # 8.周线的【成交额】等于一周中【成交额】相加         
    #periodDf=dailyPrice[['close']].resample(rule='1W').last()   #,label='left',closed='left'
    periodDf=dailyPrice.resample(rule=ruleType).last()
    periodDf['high']=dailyPrice['high'].resample(rule=ruleType).max()
    periodDf['low']=dailyPrice['low'].resample(rule=ruleType).min()
    periodDf['open']=dailyPrice['open'].resample(rule=ruleType).first()
    periodDf['volume']=dailyPrice['volume'].resample(rule=ruleType).sum()
    periodDf['money']=dailyPrice['money'].resample(rule=ruleType).sum()
    periodDf['tradDays']=dailyPrice['low'].resample(rule=ruleType).count()
    periodDf['pct_change']=dailyPrice['pct_change'].resample(rule=ruleType).apply(lambda x:(x+1.0).prod() - 1.0)
        
#     #方法2：有误
#     periodDf=dailyPrice.resample(rule='1W',on='date',base=0,label='right',closed='left').agg(
#             {
#             'open':'first',
#             'high':'max',
#             'low':'min',
#             'close':'last',
#             'volume':'sum',
#             'money':'sum',
#             'tradDays':'count'
#             }
#         )
#     
#     print(periodDf)
    
    #删除一周都没有交易数据的
    #print(periodDf[periodDf['volume']<0.001])
    periodDf=periodDf[periodDf['volume']>0.001]
    #print(periodDf[['open','close','high','low','volume','money','tradDays']])
    periodDf=periodDf[['code','open','close','high','low','volume','money','pct_change','tradDays']]
    return periodDf
    


def mergeWithIndexData(df,indexDf):
    indexDf=indexDf[indexDf['date']<=df.iloc[-1]['date']]
    
    df=pd.merge(left=df,
                right=indexDf,
                on='date',
                how='right',
                sort=True,
                indicator=True)
    
    
    # ===对开、高、收、低、前收盘价价格进行补全处理
    # 用前一天的收盘价，补全收盘价的空值
    df['close'].fillna(method='ffill',inplace=True)
    
    df['open'].fillna(value=df['close'],inplace=True)
    df['high'].fillna(value=df['close'],inplace=True)
    df['low'].fillna(value=df['close'],inplace=True)
    
    df['pre_close'].fillna(value=df['close'].shift(),inplace=True)
    
    df.loc[:,['pct_change','money','volume']]=df[['pct_change','money','volume']].fillna(value=0)
    
    # ===用前一天的数据，补全其余空值
    df.fillna(method='ffill', inplace=True)
    
    # ===去除上市之前的数据
    df = df[df['code'].notnull()]

    df.loc[df['_merge'] == 'right_only', 'paused'] = 1
    del df['_merge']

    df.reset_index(drop=True, inplace=True)
    return df

if __name__=="__main__":
    #concatDf()
    #df=work3()
    #print(df)
    #concatDf()
    jqcodeToXbxCode()
