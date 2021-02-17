import time
import pandas as pd
import jqdatasdk as jq
import tushare as ts

from study.baseJq import BaseTs
from datetime import datetime

pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.4f' % x) #不显示科学计数法


class MacroEconomy(BaseTs):
    def __init__(self):
        super().__init__()
        
    def gdp(self):
        df=self.pro.cn_gdp()
        df.to_csv('./data/macroEconomy/gdp.csv',
                  index=False)
        return df
    
    def cpi(self):
        df=self.pro.cn_cpi()
        df.to_csv('./data/macroEconomy/cpi.csv',
                  index=False)
        return df
    
    def ppi(self):
        df=self.pro.cn_ppi()
        df.to_csv('./data/macroEconomy/ppi.csv',
                  index=False)
        return df
    
    def m(self):
        df=self.pro.cn_m()
        df.to_csv('./data/macroEconomy/m.csv',
                  index=False)
        return df
    
    def rate(self):
        dfGz=self.pro.gz_index()
        dfGz.to_csv('./data/macroEconomy/rates/gz_index.csv',
                  index=False)
        
        dfWz=self.pro.wz_index()
        dfWz.to_csv('./data/macroEconomy/rates/wz_index.csv',
                  index=False)
        
        #return df

if __name__=="__main__":
    objEco=MacroEconomy()
    df=objEco.rate()
    print(df)