import zhpLiangHua.djangoShell

import pandas as pd
import numpy as np
import jqdatasdk as jq
from decimal import Decimal
from jqdatasdk import finance

from utils.common import jqdataAuth
from stock_hs_A.models import Industries,IndustryType,Securities,IncomeStatement,ReportSource,CompanyInfo,CapitalChange,ShareholderTop10

def getFinanceDataFromJqdata(stock,func,model):
    """
    从jqdata获取数据
    func:数据库表
    model:本地数据库表名
        上市公司概况  finance.STK_COMPANY_INFO   CompanyInfo
        上市公司股本变动信息 finance.STK_CAPITAL_CHANGE CapitalChange
        获取上市公司的十大股东数据    jqdata:finance.STK_SHAREHOLDER_TOP10 ShareholderTop10
    """
    #step1：从jqdata获取到该股票对应上市公司的df
    
    q=jq.query(func).filter(
        func.code==stock.code)
    df=finance.run_query(q)
    df.fillna(value=0,inplace=True)
    df.to_csv('./data/companyInfo/tmp.csv',encoding='gbk')
   
    
    #step2:更新本地数据
    #根据两个数据更细本地数据(securities,jqdataId) 
    '''
    未完成的工作，在表中增加jqdtaId字段，并且修改代码
    '''
    
    for row in df.itertuples():
        obj,isC=model.objects.get_or_create(securities=stock,jqdataId=getattr(row,'id'))
        print(obj.__dict__.keys())
        
        if isC:
            for attr in obj.__dict__.keys():
                if attr.startswith(('_','id','securities_id')):
                    continue
                setattr(obj,attr,getattr(row,attr))
            obj.save()
    
    
    return df

def updateAllCompanyInfo(func,model):
    """
    用法：上市公司概况  finance.STK_COMPANY_INFO   CompanyInfo
    """
    
    #step1:获取所有上市公司的代码（code)
    codeList=[obj.code for obj in Securities.objects.filter(securityType__name="stock")]
    print(codeList[0])
    
    #step2:从jqdata网站获取数据
    
    q=jq.query(func).filter(
        func.code.in_(codeList))
    df=finance.run_query(q)
    df.fillna(value=0.0,inplace=True)
    df.to_csv('./data/companyInfo/tmp.csv',encoding='gbk')
    #return
    
   
    #step3:将上市公司概况存入数据库
    """
    if 数据库中没有，则存入
    if 数据库中已经存在，比较
        if 没有更新，忽略
        if 有更新，更新，并且将更细记录写入日志数据表
    """
    for row in df.itertuples():        
        stock=Securities.objects.get(code=getattr(row,'code'))
        obj,isC=model.objects.get_or_create(securities=stock)
        print(stock.code)
        
        if not isC:
            #比较row和obj的相关数据，并且将更细记录写入日志数据库
            pass
        
        for attr in obj.__dict__:
            #print(type(getattr(obj,attr))==Decimal)
            if attr.startswith(('_','id','securities_id')):
                continue
        
            setattr(obj,attr,getattr(row,attr))
            obj.save()
        

def tmp():
    jqdataAuth()
    
    
    #step1:获取所有上市公司的代码（code)
    codeList=[obj.code for obj in Securities.objects.filter(securityType__name="stock")]
    #print(codeList[0])
    
    
    #step2:获取所有上市公司的概况
    q=jq.query(finance.STK_COMPANY_INFO).filter(
        finance.STK_COMPANY_INFO.code.in_(codeList))
    df=finance.run_query(q)
    print(df)
    
    #step3:将上市公司概况存入数据库
    """
    if 数据库中没有，则存入
    if 数据库中已经存在，比较
        if 没有更新，忽略
        if 有更新，更新，并且将更细记录写入日志数据表
    """
    for row in df.itertuples():
        
        security=Securities.objects.get(code=getattr(row,'code'))
        obj,isC=CompanyInfo.objects.get_or_create(securities=security)
        if 1:     
            obj.company_id=getattr(row,'company_id')    #公司ID
            obj.full_name=getattr(row,'full_name')    #公司名称
            obj.short_name=getattr(row,'short_name')   #公司简称
            obj.a_code=getattr(row,'a_code')    #A股股票代码
            obj.b_code=getattr(row,'b_code')    #B股股票代码
            obj.h_code=getattr(row,'h_code')    #H股股票代码
            obj.fullname_en=getattr(row,'fullname_en')    #英文名称
            obj.shortname_en=getattr(row,'shortname_en')    #英文简称
            obj.legal_representative=getattr(row,'legal_representative')    #法人代表
            obj.register_location=getattr(row,'register_location')    #注册地址
            obj.office_address=getattr(row,'office_address')    #办公地址
            obj.zipcode=getattr(row,'zipcode')    #邮政编码    varchar(10)    
            obj.register_capital=getattr(row,'register_capital')    #注册资金,单位：万元
            obj.currency_id=getattr(row,'currency_id')    #货币编码
            obj.currency=getattr(row,'currency')    #货币名称
            obj.establish_date=getattr(row,'establish_date')    #成立日期
            obj.website=getattr(row,'website')    #机构网址
            obj.email=getattr(row,'email')    #电子信箱
            obj.contact_number=getattr(row,'contact_number')    #联系电话
            obj.fax_number=getattr(row,'fax_number')    #联系传真
            obj.main_business=getattr(row,'main_business')    #主营业务    varchar(500)  
            obj.business_scope=getattr(row,'business_scope')    #经营范围    varchar(4000)  
            obj.description=getattr(row,'description')    #机构简介    varchar(4000)    
            obj.tax_number=getattr(row,'tax_number')    #税务登记号    varchar(50)    
            obj.license_number=getattr(row,'license_number')    #法人营业执照号    varchar(40)
            obj.pub_newspaper=getattr(row,'pub_newspaper')    #指定信息披露报刊   
            obj.pub_website=getattr(row,'pub_website')    #指定信息披露网站 
            obj.secretary=getattr(row,'secretary')    #董事会秘书    varchar(40)
            obj.secretary_number=getattr(row,'secretary_number')    #董秘联系电话    varchar(60)
            obj.secretary_fax=getattr(row,'secretary_fax')    #董秘联系传真    varchar(60)    
            obj.secretary_email=getattr(row,'secretary_email')    #董秘电子邮箱    varchar(80)  
            obj.security_representative=getattr(row,'security_representative')    #证券事务代表    varchar(40)   
            obj.province_id=getattr(row,'province_id')    #所属省份编码    varchar(12)   
            obj.province=getattr(row,'province')    #所属省份    varchar(60) 
            obj.city_id=getattr(row,'city_id')    #所属城市编码    varchar(12)       
            obj.city=getattr(row,'city')    #所属城市    varchar(60)
            obj.industry_id=getattr(row,'industry_id')    #行业编码    varchar(12)    证监会行业分类
            obj.industry_1=getattr(row,'industry_1')    #行业一级分类    varchar(60)    
            obj.industry_2=getattr(row,'industry_2')    #行业二级分类    varchar(60)
            obj.cpafirm=getattr(row,'cpafirm')    #会计师事务所    varchar(200)    
            obj.lawfirm=getattr(row,'lawfirm')    #律师事务所    varchar(200)    
            obj.ceo=getattr(row,'ceo')    #总经理    varchar(100)   
            obj.comments=getattr(row,'comments')    #备注    varchar(300)   
            obj.save() 
        else:
            pass
    
    

if __name__=="__main__":
    stock=Securities.objects.get(dsiplay_name="卫星石化")
    #print(stock)
    #updateCompanyInfo(stock)
    
    """
    上市公司概况  finance.STK_COMPANY_INFO   CompanyInfo
    上市公司股本变动信息 finance.STK_CAPITAL_CHANGE CapitalChange
    获取上市公司的十大股东数据    jqdata:finance.STK_SHAREHOLDER_TOP10 ShareholderTop10
    """
    
    """jqdataAuth()
    #updateAllCompanyInfo(finance.STK_COMPANY_INFO,CompanyInfo)
    #updateAllCompanyInfo(finance.STK_CAPITAL_CHANGE,CapitalChange)
    updateAllCompanyInfo(finance.STK_SHAREHOLDER_TOP10,ShareholderTop10)
    jq.logout()"""
    
    """jqdataAuth()
    df=getFinanceDataFromJqdata(stock,finance.STK_SHAREHOLDER_TOP10,ShareholderTop10)
    jq.logout()
    
    print(df)"""
    
    jqdataAuth()
    q=jq.query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code=='600276.XSHG').limit(10)
    df=finance.run_query(q)
    print(df)
    jq.logout()
    