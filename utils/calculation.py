import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
'''
Created on 2021年1月10日

@author:zhp

计算相关的函数
junXian：计算双均线

'''


def pctChagne(df):
    df['pct_change']=(df['close']-df['pre_close'])/df['pre_close']
    return df

def priceLimit(df):
    """
    计算涨停价和跌停价
    """
    df.loc[df['date']<='2020-09-25','high_limit']=df['pre_close']*1.1
    df.loc[df['date']<='2020-09-25','low_limit']=df['pre_close']*0.9
    
    #对st进行修改
    df.loc[(df['date']<='2020-09-25') & (df['name'].str.contains('ST')),'high_limit']=df['pre_close']*1.05
    df.loc[(df['date']<='2020-09-25') & (df['name'].str.contains('ST')),'low_limit']=df['pre_close']*0.95
    
    df.loc[df['date']<='2020-09-25','high_limit'] = df['high_limit'].apply(lambda x: float(Decimal(x*100).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 100))
    df.loc[df['date']<='2020-09-25','low_limit'] = df['low_limit'].apply(lambda x: float(Decimal(x*100).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 100))
    
    return df

def junXian(df):
    """
    计算df的均线，包括MA20、MA60、MA120，以及EMA20、EMA60、EMA120
    计算乖离率，包括CS、SM、ML，单位为：%
    
    df:需要处理的df
    
    ret:在原df的基础上增加ma_20、ema_20、ma_60、ema_60、ma_120、ema_120、CS、SM、ML列
    """
    df['date']=pd.to_datetime(df['date'])
    df.sort_values(by='date',inplace=True)
     
    #将“涨跌幅 change_pct”数据去掉%号
    #df['change_pct']=df['change_pct']/100    
    #df['change_pct_2']=df['close'].pct_change()
    #print(df)
    
    #计算EMA20、EMA60、EMA120、MA20、MA60、MA120、MAV20
    df['ma_20']=df['close'].rolling(20).mean()
    df['ma_20'].fillna(value=df['close'].expanding().mean(),inplace=True)
    df['ema_20']=pd.DataFrame.ewm(df['close'],span=20).mean()
    
    
    df['ma_60']=df['close'].rolling(60).mean()
    df['ma_60'].fillna(value=df['close'].expanding().mean(),inplace=True)
    df['ema_60']=pd.DataFrame.ewm(df['close'],span=60).mean()
    
    df['ma_120']=df['close'].rolling(120).mean()
    df['ma_120'].fillna(value=df['close'].expanding().mean(),inplace=True)
    df['ema_120']=pd.DataFrame.ewm(df['close'],span=120).mean()
    
    df['mav_20']=df['volume'].rolling(20).mean()
    df['mav_20'].fillna(value=df['volume'].expanding().mean(),inplace=True)
    
    #计算CS、SM、ML
    df['CS']=(df['close']-df['ema_20'])/df['ema_20']*100
    df['SM']=(df['close']-df['ema_60'])/df['ema_60']*100
    df['ML']=(df['close']-df['ema_120'])/df['ema_120']*100
    #print(df)
        
    return df


def calAdjustPrice(df,adjType='post'):
    """
    计算复权价,确保提供的数据包含open、close、low、high、pct_change(非%,经过pre_close计算的复权后的涨跌幅)
    其中date为datatime类型
    复权价主要用于产生交易信号signal
    
    :param df
    :adjType 'pre':前复权 'post':后复权 None 不复权
    :return 默认返回后复权价格 open_post,close
    """
    if adjType in ['post','pre']:
        #整理数据
        df.sort_values(by='date',inplace=True)
        df.reset_index(drop=True,inplace=True)
        df.drop_duplicates(subset=['date'],keep='first',inplace=True)
        
        df['pct_change']=df['close']/df['pre_close']-1.0
                
        df['factor']=(1.0+df['pct_change']).cumprod()
        if adjType=='post':
            price1=df['close'].iloc[0]  #首日收盘价
            price2=df['factor'].iloc[0] #首日资金曲线
            df['close_post']=df['factor']*(price1/price2)
           
        elif adjType=='pre':
            price1=df['close'].iloc[-1]
            price2=df['factor'].iloc[-1]
            df['close_pre']=df['factor']*(price1/price2)
        else:
            pass
        
        df['open_'+adjType]=df['open']/df['close']*df['close_'+adjType]
        df['high_'+adjType]=df['high']/df['close']*df['close_'+adjType]
        df['low_'+adjType]=df['low']/df['close']*df['close_'+adjType]
        
        #del df['factor']
        df.drop(['factor'],axis=1,inplace=True)
    return df

def amplitude(df,period=20):
    """
    计算振幅
        公式1:过去20个交易日的最高价/过去20个交易日的最低价-1
        公式2:每个交易日的最高价/最低价-1,计算20个交易日的平均值
    :param df
    :param period 振幅的参考周期
    """
    df['ampitude_'+str(period)+'_1']=df['high'].rolling(period,min_periods=1).max()/df['low'].rolling(period,min_periods=1).min()-1.0
    df['ampitude_'+str(period)+'_2']=(df['high']/df['low']-1.0).rolling(period,min_periods=1).mean()
    
    return df