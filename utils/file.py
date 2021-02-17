'''
Created on 2021年1月24日

@author: Administrator
'''
import pandas as pd

def readCsv(path):
    df=pd.read_csv(path,
                   parse_dates=['date'] #day date
                   )
    return df

def saveCsv(df,path,isAppend=False):
    if isAppend:
        df.to_csv(path,
                  header=None,
                  mode='a',
                  index=False,
                  float_format='%.15f',                  
                      )
    else:
        df.to_csv(path,
                  index=False,
                  float_format='%.15f',
                      )