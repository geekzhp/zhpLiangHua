'''
pandas显示的初始化操作

Created on 2021年1月23日

@author: Administrator
'''

import pandas as pd

pd.set_option('expand_frame_repr',False) #当列太多时，显示不换行
pd.set_option('display.max_columns', None) #显示所有的列
pd.set_option('precision', 15) #设置小数保留精度，浮点数的精度
pd.set_option('display.float_format',lambda x : '%.5f' % x) #不显示科学计数法