import zhpLiangHua.djangoShell

import pandas as pd
import jqdatasdk as jq
from jqdatasdk import finance

from updateData.common import jqdataAuth
from stock_hs_A.models import Industries,IndustryType,Securities,IncomeStatement,ReportSource

def updateIncomeStatement(stockObj):
    if not jqdataAuth():
        print('jqdata连接失败')
        return 
    
    #stockObj=Securities.objects.get(dsiplay_name='长城汽车')
    print(stockObj.code)
    
    q=jq.query(finance.STK_INCOME_STATEMENT).filter(
        finance.STK_INCOME_STATEMENT.code==stockObj.code,
        finance.STK_INCOME_STATEMENT.report_type==0,)
    df=finance.run_query(q)
    jq.logout()
    
    df.fillna(value=0.0,inplace=True)
    incomeStatementNewSet=set([(getattr(row,'pub_date'),getattr(row,'report_date')) for row in df.itertuples()])
    
    incomeStatementSet=set([(obj.pub_date,obj.report_date) for obj in IncomeStatement.objects.filter(security=stockObj)])
    
    for (pub_date,report_date) in incomeStatementNewSet-incomeStatementSet:
        row=df[(df['pub_date']==pub_date) & (df['report_date']==report_date)]
    #for row in df.itertuples():        
        
        #print(type(row.iloc[0]['exploration_expense']))
        
        IncomeStatement.objects.create(
            security=stockObj,
            reportSource=ReportSource.objects.get(code=str(row.iloc[0]['source_id'])),          
                   
            pub_date=row.iloc[0]['pub_date'],    #公告日期
            start_date=row.iloc[0]['start_date'] ,   #开始日期
            end_date=row.iloc[0]['end_date'],    #截止日期
            report_date=row.iloc[0]['report_date'],   #报告期
             
            total_operating_revenue=row.iloc[0]['total_operating_revenue'],     #营业总收入
            operating_revenue=row.iloc[0]['operating_revenue'],    #营业收入           
            total_operating_cost=row.iloc[0]['total_operating_cost'],    #营业总成本
            operating_cost=row.iloc[0]['operating_cost'],    #营业成本
            operating_tax_surcharges=row.iloc[0]['operating_tax_surcharges'],    #营业税金及附加
            sale_expense=row.iloc[0]['sale_expense'],    #销售费用
            administration_expense=row.iloc[0]['administration_expense'],    #管理费用            
            exploration_expense=row.iloc[0]['exploration_expense'],    #堪探费用            
            financial_expense=row.iloc[0]['financial_expense'],   #财务费用             
            asset_impairment_loss=row.iloc[0]['asset_impairment_loss'],   #资产减值损失
            fair_value_variable_income=row.iloc[0]['fair_value_variable_income'],   #公允价值变动净收益
            investment_income=row.iloc[0]['investment_income'],    #投资收益
            invest_income_associates=row.iloc[0]['invest_income_associates'],    #对联营企业和合营企业的投资收益
            exchange_income=row.iloc[0]['exchange_income'],    #汇兑收益
            other_items_influenced_income=row.iloc[0]['other_items_influenced_income'],    #影响营业利润的其他科目
            
            operating_profit=row.iloc[0]['operating_profit'],    #营业利润
            subsidy_income=row.iloc[0]['subsidy_income'],    #补贴收入
            non_operating_revenue=row.iloc[0]['non_operating_revenue'],    #营业外收入
            non_operating_expense=row.iloc[0]['non_operating_expense'],   #营业外支出
            disposal_loss_non_current_liability=row.iloc[0]['disposal_loss_non_current_liability'],    #非流动资产处置净损失
            other_items_influenced_profit=row.iloc[0]['other_items_influenced_profit'],    #影响利润总额的其他科目
            
            total_profit=row.iloc[0]['total_profit'],    #利润总额    
            income_tax=row.iloc[0]['income_tax'],    #所得税 
            other_items_influenced_net_profit=row.iloc[0]['other_items_influenced_net_profit'],    #影响净利润的其他科目
            
            net_profit=row.iloc[0]['net_profit'],    #净利润
            np_parent_company_owners=row.iloc[0]['np_parent_company_owners'],    #归属于母公司所有者的净利润
            minority_profit=row.iloc[0]['minority_profit'],    #少数股东损益
            
            eps=row.iloc[0]['eps'],    #每股收益
            basic_eps=row.iloc[0]['basic_eps'],    #基本每股收益
            diluted_eps=row.iloc[0]['diluted_eps'],    #稀释每股收益
            other_composite_income=row.iloc[0]['other_composite_income'],    #其他综合收益
            total_composite_income=row.iloc[0]['total_composite_income'],    #综合收益总额
            ci_parent_company_owners=row.iloc[0]['ci_parent_company_owners'],    #归属于母公司所有者的综合收益总额
            ci_minority_owners=row.iloc[0]['ci_minority_owners'],    #归属于少数股东的综合收益总额
            interest_income=row.iloc[0]['interest_income'],    #利息收入
            premiums_earned=row.iloc[0]['premiums_earned'],    #已赚保费
            commission_income=row.iloc[0]['commission_income'],    #手续费及佣金收入    
            interest_expense=row.iloc[0]['interest_expense'],    #利息支出
            commission_expense=row.iloc[0]['commission_expense'],    #手续费及佣金支出
            refunded_premiums=row.iloc[0]['refunded_premiums'],    #退保金
            net_pay_insurance_claims=row.iloc[0]['net_pay_insurance_claims'],    #赔付支出净额
            withdraw_insurance_contract_reserve=row.iloc[0]['withdraw_insurance_contract_reserve'],    #提取保险合同准备金净额
            policy_dividend_payout=row.iloc[0]['policy_dividend_payout'],    #保单红利支出
            reinsurance_cost=row.iloc[0]['reinsurance_cost'],    #分保费用
            non_current_asset_disposed=row.iloc[0]['non_current_asset_disposed'],    #非流动资产处置利得
            other_earnings=row.iloc[0]['other_earnings'],    #其他收益
            )
            
        
    #df.to_csv('./data/financialReport/income_长城汽车.csv',encoding='gbk')
    
def tmp():
    stockObjs=Securities.objects.filter(securityType__name='stock')
    for stockObj in stockObjs:
        print(stockObj.dsiplay_name)
        updateIncomeStatement(stockObj)
        
if __name__=="__main__":
    #updateIncomeStatement()
    tmp()
    