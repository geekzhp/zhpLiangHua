import time
import json
import pandas as pd
from urllib.request import urlopen

from utils.common import convertCode
from datetime import datetime

pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数 
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.4f' % x) #不显示科学计数法



def _getContentFromInternet(url,maxTryNum=10,sleepTime=5):
    """
    使用python自带的urlopen函数，从网页中抓取数据
    :param url:要抓取的网址
    :param maxTryNum:最多尝试抓取的次数
    :param sleepTime:超时时长
    
    :return 返回抓取到的内容
    """
    getSucess=False
    for i in range(maxTryNum):
        try:
            content=urlopen(url,timeout=10).read()
            getSucess=True
            break
        except Exception as e:
            print('抓取数据失败',e)
            time.sleep(sleepTime)
    
    if getSucess:
        return content
    else:
        raise ValueError('使用urlopen抓取网页数据不断报错，达到尝试的上限，停止程序，请尽快检查问题的所在')

def getRealTimeDataFromSinajs(codeList):
    """
    从新浪网，获取实时的行情数据，如果是更新日线行情，通常在下午5点之后更新当日数据
    相关信息:
        返回一个股票的数据：http://hq.sinajs.cn/list=sh600000,sz000002,sz300001，修改股票代码
        返回一串股票的数据：http://hq.sinajs.cn/list=sh600000,sz000002,sz300001
        正常网址：https://finance.sina.com.cn/realstock/company/sh600000/nc.shtml,
        
    :codeList 股票代码组成的列表，格式为:['sh600000', 'sz000002', 'sh600002', 'sz000003', 'sz300124', 'sh600276', 'sz002952']
    :return 返回股票的当日行情
        demo:其中paused,1:停牌，-1:退市
                        ode    open   close    high     low  pre_close        volume        money  paused
        date                                                                                                          
        2021-01-15 15:00:01  600000.XSHG    9.98    9.92   10.23    9.92       9.87  1.440726e+09  143067603.0       0
        2021-01-15 15:00:03  000002.XSHE   30.01   29.95   30.73   29.88      29.99  3.399073e+09  112337238.0       0
        2021-01-14 11:45:01  600002.XSHG    0.00    0.00    0.00    0.00       0.00  0.000000e+00          0.0      -1
        2021-01-14 11:45:01  000003.XSHE    0.00    0.00    0.00    0.00       0.00  0.000000e+00          0.0      -1
        2021-01-15 16:30:00  300124.XSHE   90.30   89.23   92.41   85.98      90.78  1.303148e+09   14630179.0       0
        2021-01-15 15:00:00  600276.XSHG  111.50  109.83  111.50  108.01     110.18  2.712380e+09   24707098.0       0
        2021-01-15 15:00:03  002952.XSHE   14.58   14.79   14.90   14.56      14.68  1.293188e+07     872925.0       0
        
    """
    url='http://hq.sinajs.cn/list='+','.join(codeList)
    #content=urlopen(url).read().decode('gbk').strip()
    content=_getContentFromInternet(url).decode('gbk').strip()
    
    dataLines=content.split('\n')
    dataLines=[data.replace('var hq_str_','').split(',') for data in dataLines]
    
    df=pd.DataFrame(dataLines,dtype='float64')
    df[0]=df[0].str.split('="')
    
    df['code']=df[0].str[0].str.strip().apply(convertCode)
    df['stockName']=df[0].str[-1].str.strip()
    df['date']=pd.to_datetime((df[30]+' '+df[31]).str.strip())
    
    renameDict = {1: 'open', 2: 'pre_close', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
               8: 'money', 9: 'volume', 32: 'status'}
    
    df.rename(columns=renameDict,inplace=True)
    
    #当日停牌的股票
    df['paused']=0
    pausedDf=df[(df['open']<0.00001) & (df['pre_close']>0.01)]
    if not pausedDf.empty:
        df.loc[pausedDf.index,'paused']=1
    
    #退市的股票 open close pre_close都为0
    existsDf=df[(df['open']<0.00001) & (df['pre_close']<0.00001)]
    if not existsDf.empty:
        df.loc[existsDf.index,'paused']=-1
                                
    df.set_index(['date',],inplace=True)
    return df[['code','open','close','high','low','pre_close','volume','money','paused']]

def isTodayTradingDay():
    """
    根据上证指数的数据，判断今日是否为交易日
    :return 如果今天是交易日，返回True，否则返回False
    """
    df=getRealTimeDataFromSinajs(codeList=['sh000001'])
    return df.index[0].date()==datetime.today()

def getAllStockDailyPriceToday():
    """
    http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up
    从新浪网址的上述的网址，逐页获取最近一个交易日所有股票的数据
    
    :return: 返回一个存储股票数据的DataFrame
    """
    #数据网址
    rawUrl = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s' \
              '&num=80&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=sort'
    pageNum=1
    
    allDf=pd.DataFrame()
    
    #获取上证指数最近的交易日
    df=getRealTimeDataFromSinajs(codeList=['sh000001'])
    shDate=df.index[0]
    print(shDate)
    
    while True:
        url=rawUrl % pageNum
        print('从新浪网抓取行情数据',pageNum)
        #print(url)
        content=_getContentFromInternet(url).decode('gbk').strip()
        df=pd.DataFrame(json.loads(content),dtype='float')
        
        if df.empty:
            print('从新浪网抓取全部A股行情数据结束')
            break
        
        df['symbol']=df['symbol'].str.strip().apply(convertCode)
        df['mktcap']=df['mktcap']*10000             #返回的数据，总市值单位为：万元
        df['nmc']=df['nmc']*10000                   #返回的数据，总市值单位为：万元
        df['changepercent']=df['changepercent']/100 #返回的数据，涨跌幅的单位为：%
        df['turnoverratio']=df['turnoverratio']/100 #返回的数据，换手率涨跌幅的单位为：%
        del df['code']
        
        renameDict={
            'symbol':'code',
            'trade':'close',
            'settlement':'pre_close',
            'changepercent':'change_pct',
            'volume':'volume',
            'amount':'money',
            'mktcap':'market_cap',              #总市值，单位：元
            'nmc':'circulating_market_cap',     #流通市值，单位：元
            'turnoverratio':'turnover_ratio',   #换手率
            'buy':'buy1',
            'sell':'sell1',
            'pb':'pb_ratio',                    #市净率
            }
        df.rename(columns=renameDict,inplace=True)
        #print(df)
        
        
        
        allDf=allDf.append(df,ignore_index=True)
        pageNum+=1
        
        time.sleep(1)
    
    if not allDf.empty:
        allDf['date']=shDate
        allDf['paused']=0
        
        #当日停牌的股票
        allDf['paused']=0
        pausedDf=allDf[(allDf['open']<0.00001) & (allDf['pre_close']>0.01)]
        if not pausedDf.empty:
            allDf.loc[pausedDf.index,'paused']=1
        
        #退市的股票 open close pre_close都为0
        existsDf=allDf[(allDf['open']<0.00001) & (allDf['pre_close']<0.00001)]
        if not existsDf.empty:
            allDf.loc[existsDf.index,'paused']=-1
    
    return allDf

    # 更新数据思路1：
    # 1. 使用get_today_data_from_sinajs()从新浪更新股票数据，将数据输出到预测者网的数据中
    # 2. 股票代码的list从预测者网数据的文件夹中提取
    # 3. 需要考察一下每天新增加的新股代码
    
    # 更新数据思路2：
    # 1. 使用get_all_today_stock_data_from_sina_marketcenter()，一下子获取所有股票数据，将数据输出到预测者网的数据中
    
    # 获取今天所有的股票数据
if __name__=="__main__":
    """
    每日更新股票的日行情数据
    更新数据思路1：
    1. 使用get_today_data_from_sinajs()从新浪更新股票数据，将数据输出到预测者网的数据中
    2. 股票代码的list从预测者网数据的文件夹中提取
    3. 需要考察一下每天新增加的新股代码
    
    更新数据思路2：
    1. 使用get_all_today_stock_data_from_sina_marketcenter()，一下子获取所有股票数据，将数据输出到预测者网的数据中
    这里采用了思路2
    """
#     stock_code_list = ['sh600000', 'sz000002', 'sh600002', 'sz000003', 'sz300124', 'sh600276', 'sz002952']
#     df=getRealTimeDataFromSinajs(stock_code_list)
#     print(df)

    #isTodayTradingDay()
  
#     if not isTodayTradingDay():
#         print('今天不是交易日，不需要更新数据，退出程序')
#         exit()
#      
#     if datetime.now().hour<16:
#         print('今日股票还未收盘，不需要更新数据，退出程序')
#         exit()
        
    df=getAllStockDailyPriceToday()
    df.to_csv('../data/dailyPrice/sina/'+(df.iloc[-1]['date'].date().strftime('%Y-%m-%d'))+'.csv',
              encoding='gbk',
              index=False,
              float_format='%.15f')
    
    

    #print(datetime.)
    

        
    