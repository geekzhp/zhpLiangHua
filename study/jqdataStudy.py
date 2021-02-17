import jqdatasdk as jq

import pandas as pd
#from sqlalchemy.orm.session import query

jq.auth('18009020072','4187Xslc61')

#data=jq.get_all_securities(types=[], date=None)
#data=jq.get_all_securities(types=['index'])
#data=jq.get_margincash_stocks(None)
#print(data)

stock_code=jq.normalize_code(['600031'])
print(stock_code)
#gn=jq.get_concept(stock_code[0],'2020-12-23')
#print(gn)

#sw_l1=jq.get_industries(name='sw_l1',date=None)
#print(sw_l1)

#sw_l2=jq.get_industries(name='sw_l2',date=None)
#print(sw_l1)

#sw_l3=jq.get_industries(name='sw_l3',date=None)
#print(sw_l3)

#zjhhy=jq.get_industries(name='zjw')

#gfjg=jq.get_industry_stocks('801740')
#print(gfjg)

#d=jq.get_industry(stock_code)
#print(d)
#gfjg.to_csv('./data/国防军工_jqdata.csv',encoding='gbk')

#df=jq.finance.run_query(jq.query(jq.finance.SW1_DAILY_PRICE).filter(jq.finance.SW1_DAILY_PRICE.code=='801740').order_by(jq.finance.SW1_DAILY_PRICE.date.desc()))
#print(df)
#df.to_csv('./data/国防军工_指数行情_jqdata.csv',encoding='gbk')

#获取利润表数据
"""q=jq.query(jq.finance.STK_INCOME_STATEMENT).filter(
    jq.finance.STK_INCOME_STATEMENT.code=='601633.XSHG',
    jq.finance.STK_INCOME_STATEMENT.report_type==0
        )
df=jq.finance.run_query(q)
print(df)
df.to_csv('./data/合并利润表_长城汽车.csv',encoding='gbk')"""

#十大流通股东
"""q=jq.query(jq.finance.STK_SHAREHOLDER_FLOATING_TOP10).filter(
    jq.finance.STK_SHAREHOLDER_FLOATING_TOP10.code=='601633.XSHG')
df=jq.finance.run_query(q)
print(df)
df.to_csv('./data/十大流通股东_长城汽车.csv',encoding='gbk')"""

#股东股份质押
q=jq.query(jq.finance.STK_SHARES_PLEDGE).filter(
    jq.finance.STK_SHARES_PLEDGE.code=='601633.XSHG')
df=jq.finance.run_query(q)
print(df)
df.to_csv('./data/股东股份质押.csv',encoding='gbk')
jq.logout()