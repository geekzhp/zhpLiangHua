'''
Created on 2021年1月21日

@author: Administrator
'''
import zhpLiangHua.djangoShell


from stock_hs_A.models import Securities

def jqdataToDb(df,model):
    """
    用于jqdata的finance表直接更新到项目的model表
    经检验适用于：    
        finance.STK_COMPANY_INFO    上市公司基本信息
    """
    df.fillna(value=0.0,inplace=True)
    
    for row in df.itertuples():        
        stock=Securities.objects.get(code=getattr(row,'code'))
        obj,_=model.objects.get_or_create(securities=stock)
        #print(stock.code)
       
        for attr in obj.__dict__.keys():
            if attr.startswith(('_','id','securities_id')):
                continue
        
            setattr(obj,attr,getattr(row,attr))
            obj.save()

if __name__=="__main__":
    from stock_hs_A.models import IncomeStatement
    objs=IncomeStatement.objects.filter(security_id=1)
    for obj in objs:
        print('{}:{}'.format(obj.pub_date,obj.report_date))