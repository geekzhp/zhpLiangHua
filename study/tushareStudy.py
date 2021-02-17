import tushare as ts
import pandas as pd
'''
Created on 2020年12月24日

@author: Administrator
'''

ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')

pro=ts.pro_api()
data=pro.stock_basic(exchange='',list_status='L',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date')
print(data)

data.to_csv('./data/stock_list.csv',encoding='gbk')