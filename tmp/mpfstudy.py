import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tushare as ts
import os


'''
Created on 2021年1月13日

@author: My
'''

ts.set_token('b869861b624139897d87db589b6782ca0313e0e9378b2dd73a4baff5')
pro=ts.pro_api()

#df=pro.stock_basic(fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
#df.to_csv('./data/stockList.csv',index=False)

df=pd.read_csv('./data/stockList.csv')
#print(df)
#print(df[df['name']=='三一重工']['ts_code'])  600031.SH
df=pro.daily(ts_code='000157.SZ')
print(df)
df.to_csv('./data/000157_daily.csv',index=False)

class DataFinanceDraw(object):
    """
            获取数据，并按照mpf需求的格式格式化，并绘图
    """
    def __inti__(self):
        self.data=pd.DataFrame()
    
    def _format_ts_mpf_data(self,data):
        """
                    格式化数据：从tushare数据格式化成mpf标准格式
        """
        data['Date']=pd.to_datetime(data['trade_date'],format='%Y%m%d')
        data.set_index(['Date'],inplace=True)
        del data['trade_date']
        
        data.rename(columns={'open':'Open','close':'Close','high':'High','low':'Low','vol':'Volume'},inplace=True)
        data.sort_index(inplace=True)
        return data
        
    def my_data(self,file_name='600031_daily.csv'):
        """
                    获取数据，并将数据格式化称mpf的标准格式
        """
        data=pd.read_csv(os.getcwd()+'\\data\\'+file_name)
        data=self._format_ts_mpf_data(data)
        self.data=data
        
        return data
    
    def compare_data(self,file_name='000157_daily.csv'):
        data=pd.read_csv(os.getcwd()+'\\data\\'+file_name)
        data=self._format_ts_mpf_data(data)
        return data
    
    def more_panel_draw(self):
        """
        make_addplot 绘制多个子图，这里以添加macd指标为例
        """
        data=self.data[-250:]
        #计算macd指标，可以选择第三方模块talib,该模块包含了常用的金融指标kdj、macd、boll等等
        exp12=data['Close'].ewm(span=12,adjust=False).mean()
        exp26=data['Close'].ewm(span=26,adjust=False).mean()
        macd=exp12-exp26
        signal=macd.ewm(span=9,adjust=False).mean()
        
        histogram=macd-signal        
        histogram[histogram<0]=None
        histogram_positive=histogram
        histogram=macd-signal
        histogram[histogram>=0]=None
        histogram_negative=histogram
        
        
        #添加macd子图
        """add_plot=[
            mpf.make_addplot(exp12,type='line',color='y'),
            mpf.make_addplot(exp26,type='line',color='r'),
            mpf.make_addplot(histogram,type='bar',width=0.7,color='dimgray',alpha=1,secondary_y=False,panel=2),
            mpf.make_addplot(macd,color='fuchsia',secondary_y=True,panel=2),
            mpf.make_addplot(signal,color='b',secondary_y=True,panel=2),
            ]"""
            
        #分色显示
        add_plot=[
            mpf.make_addplot(exp12,type='line',color='y'),
            mpf.make_addplot(exp26,type='line',color='r'),
            mpf.make_addplot(histogram_positive,type='bar',width=0.7,panel=2,color='b'),
            mpf.make_addplot(histogram_negative,type='bar',width=0.7,panel=2,color='fuchsia'),
            mpf.make_addplot(macd,color='fuchsia',secondary_y=True,panel=2),
            mpf.make_addplot(signal,color='b',secondary_y=True,panel=2),
            ]
        
        
        mpf.plot(data,type='candle',
                 addplot=add_plot,
                 volume=True,
                 figscale=1.5,
                 figratio=(5,5),
                 title='MACD',
                 ylabel='price',
                 ylabel_lower='volume',
                 main_panel=0,
                 volume_panel=1,
                 )
    
    def panel_draw(self):
        """
                    绘制多个子图
        """
        data=self.data.iloc[-250:]
        
        add_plot=[
            #mpf.make_addplot(self.compare_data()[-250:],type='candle',panel=2)
            mpf.make_addplot(self.compare_data()[-250:],type='candle',panel=1,mav=(5,20))
            ]
        
        mpf.plot(data,type='candle',
                 
                 main_panel=0,      #设置主图编码
                 volume_panel=2,    #设置成交量图编码
                 num_panels=4,      #设置panel的数量
                 panel_ratios=(1,1,0.3,0.2),    #设置各panel的比例
                 
                 mav=(5,20),
                 addplot=add_plot,
                 volume=True,
                 
                 figscale=1.5,
                 title='candle',
                 figratio=(5,5),
                 ylabel='price',
                 ylabel_lower='volume',
                 )
        
        plt.show()
        plt.close()
        
if __name__=="__main__":
    obj=DataFinanceDraw()
    print(obj.my_data())
    #obj.panel_draw()
    obj.more_panel_draw()
    
    