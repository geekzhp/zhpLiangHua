'''
Created on 2020年12月28日

@author: zhp

用于更新基础数据：
    股票列表
    行业列表
    沪深成分股
    上市公司基本信息
    
'''

import zhpLiangHua.djangoShell

import pandas as pd
import jqdatasdk as jq

from datetime import datetime

from updateData.thirdLibrary.base import BaseJq,BaseTs
from utils.jqdataToDb import jqdataToDb
from utils.convert import normalize_code

from stock_hs_A.models import (Exchange,
                               TradeDay,
                               Industries,
                               Securities,
                               SecurityType,
                               CompanyInfo,
                               Index,
                               )

class UpdataBasic(BaseJq,BaseTs):
    """
    更新基础数据：
    交易日历
    股票列表
    
    """
    
    def __init__(self):
        BaseJq.__init__(self)
        BaseTs.__init__(self)
    
    def tradeDay(self,startDate):
        """
        通过tushare接口，更新交易日历
            交易所    SSE上交所,
                    SZSE深交所,
                    CFFEX 中金所,
                    SHFE 上期所,
                    CZCE 郑商所,
                    DCE 大商所,
                    INE 上能源
                    
        :DB TradeDay
        """
        for tsExchange in ['SSE','SZSE','CFFEX','SHFE','CZCE','DCE','INE']:
            df = self.tsPro.trade_cal(exchange=tsExchange, 
                                      start_date=startDate,
                                      end_date=datetime.today().strftime('%Y%m%d'))
            df['cal_date']=pd.to_datetime(df['cal_date'])
            
            #print(len(df))
            for row in df.itertuples():
                tdObj,_=TradeDay.objects.get_or_create(
                    exchagne=Exchange.objects.get(tsCode=tsExchange),
                    date=getattr(row,'cal_date'),                
                    )
                tdObj.isOpen=getattr(row,'is_open')
                tdObj.save()
            
        #return df
    
    def stockByTs(self):
        df=self.tsPro.stock_basic(exchange='', list_status='D',fields='ts_code,name,list_status,list_date,delist_date')
        for row in df.itertuples():            
            obj,isC=Securities.objects.get_or_create(
                code=normalize_code(getattr(row,'ts_code'))
                )
            if isC:
                obj.display_name=getattr(row,'name')
                obj.name=getattr(row,'name')
                obj.start_date=datetime.strptime(getattr(row,'list_date'),'%Y%m%d')
                obj.end_date=datetime.strptime(getattr(row,'delist_date'),'%Y%m%d') if getattr(row,'delist_date')  else datetime.date(2200,1,1)
                obj.securityType_id=1
                obj.save()
        return df
            
    
    def stockByJq(self,typeList=['stock',]):
        """
        更新股票列表
        type: 类型 : stock(股票)
                    index(指数)
                    etf(ETF基金)
                    fja（分级A）
                    fjb（分级B）
                    fjm（分级母基金）
                    mmf（场内交易的货币基金）
                    open_fund（开放式基金）
                    bond_fund（债券基金）
                    stock_fund（股票型基金）
                    QDII_fund（QDII 基金）
                    money_market_fund（场外交易的货币基金）
                    mixture_fund（混合型基金）
                    options(期权)
                    
        :DB SecurityType、CompanyInfo
        未完成：
            更新股票列表后，财务报表、股东数据等数据的更新
        """
        
        
        securitiesDf=jq.get_all_securities(typeList)
        #print(len(securitiesDf))
                
        for row in securitiesDf.itertuples():
            obj,isCreate=Securities.objects.get_or_create(
                code=row[0]            
            )
            #print(row[1],row[5])
            obj.display_name=row[1]
            obj.name=row[2]
            obj.start_date=row[3]
            obj.end_date=row[4]
           
            obj.securityType=SecurityType.objects.get_or_create(name=row[5])[0]
            obj.save()
            
            if isCreate and typeList==['stock',]:
                print('new company:{}'.format(obj.display_name))
                
                #更新上市公司概况  
                q=jq.query(jq.finance.STK_COMPANY_INFO).filter(
                            jq.finance.STK_COMPANY_INFO.code==obj.code)
                df=jq.finance.run_query(q)
                jqdataToDb(df,CompanyInfo)                
                
                #更新财务报表
                pass
        
        #更新QDII基金
        if typeList==['QDII_fund',]:
            self._secondSecurityType()
            
        return securitiesDf
    
    def _secondSecurityType(self):
        """
        open_fund（开放式基金） 第一分类
        QDII_fund（QDII 基金） 第二分类        
        """
        df=jq.get_all_securities(types=['QDII_fund'])
         
        for code in df.index:
            sObj=Securities.objects.get(code=code)
            sObj.securityType2=SecurityType.objects.get(name='QDII_fund')
            sObj.save()
    
    
    def indexList(self):
        """
        上交所、深交所的各类指数
        """
        if self.checkQueryCount():
            df=jq.get_all_securities(types=['index'],date=None)
            
            for row in df.itertuples():
                #print(row)
                obj,_=Index.objects.get_or_create(code=getattr(row,'Index'))
#                 Pandas(Index='000001.XSHG', display_name='上证指数', name='SZZS', start_date=Timestamp('1991-07-15 00:00:00'), end_date=Timestamp('2200-01-01 00:00:00'), type='index')
#                 Pandas(Index='000002.XSHG', display_name='A股指数', name='AGZS', start_date=Timestamp('1992-02-21 00:00:00'), end_date=Timestamp('2200-01-01 00:00:00'), type='index')
                for attr in obj.__dict__.keys():
                    if attr in ('_state','id','code'):
                        continue
                    setattr(obj,attr,getattr(row,attr))
                obj.save()
        else:
            return pd.DataFrame()
        
    def industry(self):
        '''
        废弃，不再使用
        功能：更新行业分类
                "sw_l1": 申万一级行业
                "sw_l2": 申万二级行业
                "sw_l3": 申万三级行业
                "jq_l1": 聚宽一级行业
                "jq_l2": 聚宽二级行业
                "zjw": 证监会行业
        '''    
        swL1New=jq.get_industries('sw_l1')
        codesSwL1New=set(swL1New.index) 
        
        swL2New=jq.get_industries('sw_l2')
        codesSwL2New=set(swL2New.index)  
        
        swL3New=jq.get_industries('sw_l3')
        codesSwL3New=set(swL3New.index)  
      
        zjwNew=jq.get_industries('zjw')
        codesZjwNew=set(zjwNew.index)
       
        
        swL1=Industries.objects.filter(industryType__name="申万一级行业")    
        codesSwL1=set([obj.code for obj in swL1])
        for code in codesSwL1New-codesSwL1:
            Industries.objects.create(
                code=code,
                name=swL1New.loc[code,'name'],
                industryType_id=1,
                start_date=swL1New.loc[code,'start_date']
                )
        
        swL2=Industries.objects.filter(industryType__name="申万二级行业")    
        codesSwL2=set([obj.code for obj in swL2])
        for code in codesSwL2New-codesSwL2:
            Industries.objects.create(
                code=code,
                name=swL2New.loc[code,'name'],
                industryType_id=2,
                start_date=swL2New.loc[code,'start_date']
                )
        
        swL3=Industries.objects.filter(industryType__name="申万三级行业")    
        codesSwL3=set([obj.code for obj in swL3])
        for code in codesSwL3New-codesSwL3:
            Industries.objects.create(
                code=code,
                name=swL3New.loc[code,'name'],
                industryType_id=3,
                start_date=swL3New.loc[code,'start_date']
                )
         
        zjw=Industries.objects.filter(industryType__name="证监会行业")    
        codesZjw=set([obj.code for obj in zjw])
        for code in codesZjwNew-codesZjw:
            Industries.objects.create(
                code=code,
                name=zjwNew.loc[code,'name'],
                industryType_id=4,
                start_date=zjwNew.loc[code,'start_date']
                )    

    

def tuiShiStock():
    tsStock=Securities.objects.filter(end_date__lt=datetime.today())
    for obj in tsStock.values():
        print(obj)


    
if __name__=="__main__":
    obj=UpdataBasic()
    #df=obj.tradeDay('INE')
    #df=obj.stock()
    #df=obj.indexList()
    df=obj.stockByTs()
    print(df)
    
    obj.logoutJq()
    