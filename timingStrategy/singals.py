'''
Created on 2021年1月30日

@author: Administrator

'''

def signalMaParaList(maShort=range(10,200,10),maLong=range(10,300,10)):
    """
    产生简单移动平均线策略的参数范围
    :param ma_short:
    :param ma_long:
    :return:
    """
    paraList=[]
    for short in maShort:
        for long in maLong:
            if short>=long:
                continue
            else:
                paraList.append((short,long))
    return paraList

def signalMa(df,para):   #计算交易信号，产生signal(只有产生信号这部分代码需要自己写，其它部分都是可以复用的）
    """
    均线策略：
    当短期均线由下向上穿过长期均线的时候，第二天以开盘价全仓买入并在之后一直持有股票。
    当短期均线由上向下穿过长期均线的时候，第二天以开盘价卖出全部股票并在之后一直空仓，直到下一次买入。

    :param df:
    :param ma_short: 短期均线
    :param ma_long: 长期均线
    :return:
    """
    #双均线策略
    # for maShort in [5,10,15,20,25]:
    #     for maLong in [10,15,20,25,30]:
    #         if maShort<maLong:
    #             continue
    maShort,maLong=para
    
    df['maShort']=df['close_post'].rolling(maShort,min_periods=1).mean()
    df['maLong']=df['close_post'].rolling(maLong,min_periods=1).mean()
    
    #买入信号，做多信号
    cond1=(df['maShort']>df['maLong'])
    cond2=(df['maShort'].shift(1)<=df['maLong'].shift(1))
    df.loc[cond1 & cond2,'signal']=1    #1:做多
    
    #卖出信号，平仓信号
    cond1=(df['maShort']<df['maLong'])
    cond2=(df['maShort'].shift(1)>=df['maLong'].shift(1))
    df.loc[cond1 & cond2,'signal']=0    #0:平仓
    
    df.drop(['maShort','maLong','open_post','high_post','low_post'],axis=1,inplace=True)
    
    return df