import pandas as pd

#当列太多时，显示不换行
pd.set_option('expand_frame_repr',False)
#显示所有的列
pd.set_option('display.max_columns', None)
#设置小数保留精度
pd.set_option('precision', 15)
#不显示科学计数法
pd.set_option('display.float_format',lambda x : '%.4f' % x)
'''
Created on 2021年1月14日

@author: My
'''

df=pd.read_csv('./data/巨潮/业绩预告.csv',encoding='gbk')
dfzz=(df[df['业绩类型']=='业绩大幅上升']).sort_values(by='净利润增长幅下限(%)',ascending=False)
dfzz.to_csv('./data/巨潮/业绩大幅增长.csv',encoding='gbk')
print(dfzz.dtypes)