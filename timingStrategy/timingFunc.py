'''
Created on 2021年1月30日

@author: Administrator
'''

import numpy as np
import pandas as pd

def position(df):
    """
    将交易信号转换成仓位，以当日尾盘价作为收盘价计算
    根据交易信号，计算每天的仓位,默认为满仓操作，即0:空仓，1:满仓
    原理：
        产生交易信号signal=1时，通常来说，在第二个交易日已开盘价买入，但是，实际运行时，尽量选择另外一种方式，
        而是在产生信号的当天，以收盘价买入这只股票。
        实际情况是，在离收盘还有5分钟时，运行一下择时策略，则以14:55的价格作为当日的收盘价。如果产生交易信号，
        则买入。
        这是因为A股是T+1的，当天买了不能当天卖，因此，尽量在尾盘买入，那么当天发生各种事件，可以当天卖出。
        
        卖出同样，发出卖出信号时，在当天收盘尾盘时卖出。
    :param df
    :return:
    """
    
    #在产生signal的k线结束的时候，进行买入  
        
    df['signal'].fillna(method='ffill',inplace=True)    
    df['signal'].fillna(value=0,inplace=True)   # 将初始行数的signal补全为0
    
    
    df['pos']=df['signal'].shift()  #产生信号，尾盘买入，第二个交易日才有实际持有仓位;产生卖出信号，第二日尾盘卖出
    df['pos'].fillna(value=0,inplace=True)
           
       
    #（开盘时买入）开盘即涨跌停时不得买卖股票考虑进来,还未考虑ST股票
    #收盘时买入，需要考虑当天涨停时，无法买入；当天跌停时，无法卖出
    condCannotBuy=df['close']>=df['high_limit']
    df.loc[condCannotBuy.shift() & (df['signal'].shift()==1),'pos']=None   #上一个收盘价无法买入（涨停），应保持上一天的仓位值
        
    #condCannotSell=df['open_post']<df['close_post'].shift(1)*0.903
    condCannotSell=df['close']<=df['low_limit']
    df.loc[condCannotSell.shift() & (df['signal'].shift()==0),'pos']=None
    
    # position为空的日期，不能买卖。position只能和前一个交易日保持一致。
    df['pos'].fillna(method='ffill',inplace=True)
    #print(df[df['date']>pd.to_datetime('2015-05-01')])
    df.drop(['signal'],axis=1,inplace=True)
    return df

def calcuEquityCurveSimple(df):
    """
    计算资金曲线
    资金曲线时一个策略最终的结果，是评价一个策略最重要的标准
    
    计算资金曲线的简单方法
        首先计算资金曲线的每天涨幅
        当天空仓时，pos为0，资产涨幅为0
        当天满仓买入时，pos为1，资产涨幅为股票本身的涨跌幅
    
    存在的问题
        没有考虑交给券商的手续费，以及没有考虑交给国家的印花税
        没有考虑交易的滑点
        计算时，采用的当天的当涨跌幅（当日收盘价与前一日收盘价计算得出），实际情况是我们以当天的开盘价买入这只股票
        我们要求的是，当天收盘后产生交易信号，第二天开盘后以开盘价买入，这是逻辑上的错误
        以及没有考虑。。。
    """
    
    df['equityChange']=df['pct_change']*df['pos']
    df['equityCurve']=(df['equityChange']+1).cumprod()
    
    return df
    
def calcuEquityCurve_2017(df,initMoney=1000000,slippage=0.01,cRate=5.0/10000,tRate=1.0/1000):
    """
    逐行计算每日的资金曲线
    
    :param df['date','code','open','close','high','low','pct_change','pos']
    :param initMoney=1000000    #初始资金100万元
    :param slippage=0.01   #滑点，默认为0.01
    :param cRate=5.0/10000 #手续费，commission fees,默认为万分之5
    :param tRate=1.0/1000  #印花税，tax，默认未千分之一
    
    :return 
    """
    #计算实际的资金曲线（实际方法）
    df=df[['date','code','open','close','high','low','pct_change','pos']]
    df.reset_index(drop=True,inplace=True)
        
    #第一天的情况
    df.at[0,'holdNum']=0    #持有股票数量，此处也可以使用loc,相比at效率更高
    df.loc[0,'sotckValue']=0    #持仓股市市值
    df.at[0,'actualPos']=0  #每日的实际仓位
    df.at[0,'cash']=initMoney   #持有的现金
    df.at[0,'equity']=initMoney #总资产，即资金曲线=持仓股票市值+现金
    #print(df)
    
    for i in range(1,df.shape[0]):
        #前一天持有股票的数量
        #只能使用i-1,不能使用i+1等，用到了未来数据
        holdNum=df.at[i-1,'holdNum']
        
        #判断当天是否除权，若发生除权，需要调整holdNum
        #若当天通过收盘价计算出的涨跌幅，和当天实际涨跌幅不同，说明当天发生了除权
        if abs((df.at[i,'close']/df.at[i-1,'close']-1)-df.at[i,'pct_change'])>0.001:
            sotckValue=df.at[i-1,'sotckValue']
            #交易所会公布除权之后的价格
            lastPrice=df.at[i,'close']/(df.at[i,'pct_change']+1)    #昨天复权后的价格
            holdNum=sotckValue/lastPrice
            holdNum=int(holdNum)
              
    #         if i>1030:
    #             print(sotckValue,lastPrice,holdNum)
    #             print(df.iloc[1034:])
    #             exit()
        
        #判断是否需要调整仓位：那今天的仓位pos,和昨天的pos今天比较，看是否相同
        #需要调整仓位
        if df.at[i,'pos']!=df.at[i-1,'pos']:
            #对于需要调整仓位，需要买入多少股票
            #昨天的总资产*今天的仓位/今天的开盘价，得到需要持有的股票
            theoryNum=df.at[i-1,'equity']*df.at[i,'pos']/df.at[i,'open']
    #         print(type(theoryNum))  #<class 'numpy.float64'>
    #         print(theoryNum)
    #         exit()
            #对需要持有的股票数取整,如果向上取整，会出现钱不够的情况        
            #print(theoryNum)
            theoryNum=int(theoryNum) if theoryNum==theoryNum else 0
            
            #将theroyNum和昨天持有的股票相比，判断是加仓还是减仓
            
            if theoryNum>=holdNum:
                #加仓
                buyNum=theoryNum-holdNum
                #买股票只能整百（以手为单位），对buyNum向下取整百
                buyNum=int(buyNum/100)*100
                
                #计算买入股票花去的现金
                buyCash=(df.at[i,'open']+slippage)*buyNum
                #计算手续费
                commission=round(buyCash*cRate,2)
                
                #不足5元按5元收取
                if commission<5 and commission!=0:
                    commission=5
                df.at[i,'commission']=commission
                
                #计算当天收盘时持有的股票的数量和现金
                df.at[i,'holdNum']=holdNum+buyNum
                df.at[i,'cash']=df.at[i-1,'cash']-buyCash-commission
            else:
                #减仓
                sellNum=holdNum-theoryNum
                sellCash=sellNum*(df.at[i,'open']-slippage)
                commission=round(max(sellCash*cRate,5),2)
                df.at[i,'commission']=commission
                tax=round(sellCash*tRate,2)
                df.at[i,'tax']=tax
                
                #计算当天收盘时持有的股票的数量和现金
                df.at[i,'holdNum']=holdNum-sellNum
                df.at[i,'cash']=df.at[i-1,'cash']+sellCash-commission-tax
                
        else:
            #不需要调整仓位
            df.at[i,'holdNum']=holdNum
            df.at[i,'cash']=df.at[i-1,'cash']
            
        
        #以上计算的每天的holdNum和cash
        #计算当太难收盘时的各种资产数据
        df.at[i,'sotckValue']=df.at[i,'holdNum']*df.at[i,'close']    #股票市值
        df.at[i,'equity']=df.at[i,'cash']+df.at[i,'sotckValue']     #总资产
        df.at[i,'actualPos']=df.at[i,'sotckValue']/df.at[i,'equity']    #实际仓位，仓位的re-balance
    return df

def calcuEquityCurve(df,initMoney=1000000,slippage=0.01,cRate=2.5/10000,tRate=1.0/1000):
    """
    逐行计算每日的资金曲线
    
    :param df['date','code','open','close','high','low','pct_change','pos']
    :param initMoney=1000000    #初始资金100万元
    :param slippage=0.01   #滑点，默认为0.01,etf为0.001元
    :param cRate=2.5/10000 #手续费，commission fees,默认为万分之2.5
    :param tRate=1.0/1000  #印花税，tax，默认未千分之一
    
    :return 
    """
    #开仓条件（买入）
    cond1=df['pos']!=0
    cond2=df['pos']!=df['pos'].shift(1)
    openPosCond=cond1 & cond2   #当天pos=1，上一日pos_shift_1=0
    
    #平仓条件(卖出)
    cond1=df['pos']!=0
    cond2=df['pos']!=df['pos'].shift(-1)    
    #当天pos=1,第二天pos_shift_-1=0,这里并不是用到了未来数据，用当日尾盘的价格作为第二日收盘价计算出的pos，因此是有效的
    closePosCond=cond1 & cond2
    
    #对每次交易进行分组
    df.loc[openPosCond,'startTime']=df['date']
    df['startTime'].fillna(method='ffill',inplace=True)
    df.loc[df['pos']==0,'startTime']=pd.NaT
    
    #计算资金曲线
    #买入之后K线的变动
    df.loc[openPosCond,'stockNum']=initMoney*(1-cRate)/(df['pre_close']+slippage)
    df['stockNum']=np.floor(df['stockNum']/100)*100
    
    #买入股票后，剩余的钱，扣除了手续费
    #cash=initMoney-买股票花去的钱-买股票花去的钱*cRate(手续费）
    df['cash']=initMoney-df['stockNum']*(df['pre_close']+slippage)*(1+cRate)
    
    #收盘时，股票的净值
    df['stockValue']=df['stockNum']*df['close']
    
    #买入之后，现金不再发生变动
    df['cash'].fillna(method='ffill',inplace=True)
    df.loc[df['pos']==0,['cash']]=None
    
    #股票的净值StockValue随着涨跌幅波动
    #不能直接用df['stockNum']*df['close']计算，因为，发生配股、送股等行为时，stockNum会发生变化
    #StockValue的变化比例，与close_post(复权价)变化的比例时一样的，等比例变动
    groupNum=len(df.groupby('startTime'))
    if groupNum>1:
        t=df.groupby('startTime').apply(lambda x:x['close_post']/x.iloc[0]['close_post']*x.iloc[0]['stockValue'])
        t=t.reset_index(level=[0])
        df['stockValue']=t['close_post']
    elif groupNum==1:
        t=df.groupby('startTime')[['close_post','stockValue']].apply(lambda x:x['close_post']/x.iloc[0]['close_post']*x.iloc[0]['stockValue'])
        df['stockValue']=t.T.iloc[:,0]
    #print(t[:500])
    
    #df['stockNum']=df['stockValue']/df['close']
    
    
    #卖出之后K线的变动
    #股票数量的变动
    df.loc[closePosCond,'stockNum']=df['stockValue']/df['close']
    
    #现金变动
    df.loc[closePosCond,'cash']+=df.loc[closePosCond,'stockNum']*(df['close']-slippage)*(1-cRate-tRate)
    
    #股票价值变动
    df.loc[closePosCond,'stockValue']=0
    
    #账户净值
    df['netValue']=df['stockValue']+df['cash']
    
    #计算资金曲线
    df['equityChange']=df['netValue'].pct_change(fill_method=None)
    #补全,开仓日的收益率
    df.loc[openPosCond,'equityChange']=df.loc[openPosCond,'netValue']/initMoney-1
    #补全，未交易日的涨跌幅为0
    df['equityChange'].fillna(value=0,inplace=True)
    df['equityCurve']=(1+df['equityChange']).cumprod()
    
    df['equityCurveBase']=(1+df['pct_change']).cumprod()
    #删除无关数据
    df.drop(['startTime','stockNum','cash','stockValue','netValue'],axis=1,inplace=True)
    
    return df