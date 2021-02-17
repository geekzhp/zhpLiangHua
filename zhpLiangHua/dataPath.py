'''
Created on 2021年1月30日

@author: Administrator
'''

import os
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent


DATA=os.path.join(BASE_DIR,'updateData','data')

#K线
KLINE=os.path.join(DATA,'kline')
K_1M=os.path.join(KLINE,'stock','1m')
K_60M=os.path.join(KLINE,'stock','60m')

#日行情根文件夹
DAILY_PRICE=os.path.join(DATA,'dailyPrice')

#选股策略（日线）用到的基础数据

SELECT=os.path.join(DAILY_PRICE,'select')

#交易所资金流向
EXCHANGE_JQ=os.path.join(DAILY_PRICE,'exchange','jqdata')
#/zhpLiangHua/updateData/data/dailyPrice/stock/fundamental

#市场通
HSGT=os.path.join(DAILY_PRICE,'hsgt')
HSGT_HK_HOLD=os.path.join(HSGT,'hkHold')
HSGT_PRICE=os.path.join(HSGT,'moneyflow','price')
HSGT_RATE=os.path.join(HSGT,'moneyflow','rate')

#指数日行情
INDEX=os.path.join(DAILY_PRICE,'index')
INDEX_PRICE=os.path.join(INDEX,'price')

#融资融券
MARGIN=os.path.join(DAILY_PRICE,'margin')

#个股资金流向
MONEY_FLOW=os.path.join(DAILY_PRICE,'moneyflow')

#新浪抓取的行情数据（全A股）
SINA=os.path.join(DAILY_PRICE,'sina')

#个股日行情
STOCK=os.path.join(DAILY_PRICE,'stock')
STOCK_PRICE=os.path.join(STOCK,'price')
STOCK_FUNDAMENTAL=os.path.join(STOCK,'fundamental')
STOCK_FUNDAMENTAL_JQ=os.path.join(STOCK_FUNDAMENTAL,'jqdata')
STOCK_FUNDAMENTAL_TS=os.path.join(STOCK_FUNDAMENTAL,'tushare')
STOCK_SWL1=os.path.join(STOCK,'swL1')

#申万一级行业日行情
SWL1_PRICE=os.path.join(DAILY_PRICE,'swL1','price')
SWL1_VALUE=os.path.join(DAILY_PRICE,'swL1','valuation')
SWL1_STOCKS=os.path.join(STOCK,'swL1')

#龙虎榜
TOP_LIST=os.path.join(DAILY_PRICE,'topList')

#print(HSGT_RATE)