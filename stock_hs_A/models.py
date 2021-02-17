from django.db import models


# Create your models here.
class Exchange(models.Model):
    """
    交易所
            交易市场    代码后缀    示例代码    证券简称
        上海证券交易所    .XSHG    '600519.XSHG'    贵州茅台
        深圳证券交易所    .XSHE    '000001.XSHE'    平安银行
        中金所    .CCFX    'IC9999.CCFX'    中证500主力合约
        大商所    .XDCE    'A9999.XDCE'    豆一主力合约
        上期所    .XSGE    'AU9999.XSGE'    黄金主力合约
        郑商所    .XZCE    'CY8888.XZCE'    棉纱期货指数
        上海国际能源期货交易所    .XINE    'SC9999.XINE'    原油主力合约
    """
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=10)
    tsCode=models.CharField(max_length=10,null=True,default=None)
    
class TradeDay(models.Model):
    """
    交易日历
    """
    exchagne=models.ForeignKey(Exchange,on_delete=models.CASCADE)
    date=models.DateField()
    isOpen=models.BooleanField(default=True)
    isUpdate=models.BooleanField(default=False)
    
    class Meta:
        ordering=['exchagne','date']

class IndustryType(models.Model):
    name=models.CharField(max_length=50)
    short=models.CharField(max_length=20)

class Industries(models.Model):
    code=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=50,null=True,default=None)
    industryType=models.ForeignKey(IndustryType, on_delete=models.CASCADE,null=True)
    start_date=models.DateField(null=True)

class Index(models.Model):
    """
    指数
    """
    code=models.CharField(max_length=20,unique=True)
    display_name=models.CharField(max_length=50,null=True)
    name=models.CharField(max_length=50,null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)

class SecurityType(models.Model):
    """
    type: 类型 : stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权)
    """
    name=models.CharField(max_length=20)
    des=models.CharField(max_length=50,null=True,default=None)
    
class Securities(models.Model):
    """
            交易市场               代码后缀    示例代码            证券简称
        上海证券交易所              .XSHG    '600519.XSHG'      贵州茅台
        深圳证券交易所              .XSHE    '000001.XSHE'      平安银行
        中金所                    .CCFX    'IC9999.CCFX'      中证500主力合约
        大商所                    .XDCE    'A9999.XDCE'       豆一主力合约
        上期所                    .XSGE    'AU9999.XSGE'      黄金主力合约
        郑商所                    .XZCE    'CY8888.XZCE'      棉纱期货指数
        上海国际能源期货交易所        .XINE    'SC9999.XINE'      原油主力合约
    """
    code=models.CharField(max_length=20,unique=True)
    display_name=models.CharField(max_length=50,null=True)
    name=models.CharField(max_length=50,null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    securityType=models.ForeignKey(SecurityType,on_delete=models.CASCADE,related_name='mainType',null=True)
    securityType2=models.ForeignKey(SecurityType,on_delete=models.CASCADE,null=True,related_name='secondType',default=None)
    
    
#财务报表

class ReportSource(models.Model):
    """
    报表来源：
                编码    名称
            321001    招募说明书
            321002    上市公告书
            321003    定期报告
            321004    预披露公告
            321005    换股报告书
            321099    其他
    """
    code=models.CharField(max_length=20)
    name=models.CharField(max_length=50)


class IncomeStatement(models.Model):
    """
    合并利润表
    """
    security=models.ForeignKey(Securities,on_delete=models.CASCADE)
    reportSource=models.ForeignKey(ReportSource,on_delete=models.CASCADE)
    
    pub_date=models.DateField()    #公告日期
    start_date=models.DateField()    #开始日期
    end_date=models.DateField()    #截止日期
    report_date=models.DateField()    #报告期
    
    total_operating_revenue=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业总收入
    operating_revenue=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业收入
    
    total_operating_cost=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业总成本
    operating_cost=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业成本
    operating_tax_surcharges=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业税金及附加
    sale_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #销售费用
    administration_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #管理费用
    exploration_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #堪探费用
    financial_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #财务费用
    asset_impairment_loss=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #资产减值损失
    fair_value_variable_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #公允价值变动净收益
    investment_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #投资收益
    invest_income_associates=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #对联营企业和合营企业的投资收益
    exchange_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #汇兑收益
    other_items_influenced_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #影响营业利润的其他科目
    
    operating_profit=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业利润
    subsidy_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #补贴收入
    non_operating_revenue=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业外收入
    non_operating_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #营业外支出
    disposal_loss_non_current_liability=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #非流动资产处置净损失
    other_items_influenced_profit=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #影响利润总额的其他科目
    
    total_profit=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #利润总额    
    income_tax=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #所得税 
    other_items_influenced_net_profit=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #影响净利润的其他科目
    
    net_profit=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #净利润
    np_parent_company_owners=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #归属于母公司所有者的净利润
    minority_profit=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #少数股东损益
    
    eps=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #每股收益
    basic_eps=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #基本每股收益
    diluted_eps=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #稀释每股收益
    other_composite_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #其他综合收益
    total_composite_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #综合收益总额
    ci_parent_company_owners=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #归属于母公司所有者的综合收益总额
    ci_minority_owners=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #归属于少数股东的综合收益总额
    interest_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #利息收入
    premiums_earned=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #已赚保费
    commission_income=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #手续费及佣金收入    
    interest_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #利息支出
    commission_expense=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #手续费及佣金支出
    refunded_premiums=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #退保金
    net_pay_insurance_claims=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #赔付支出净额
    withdraw_insurance_contract_reserve=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #提取保险合同准备金净额
    policy_dividend_payout=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #保单红利支出
    reinsurance_cost=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #分保费用
    non_current_asset_disposed=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #非流动资产处置利得
    other_earnings=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #其他收益
    

#上市公司概况
class CompanyInfo(models.Model):
    """
    上市公司概况
    """
    securities=models.ForeignKey(Securities,on_delete=models.CASCADE)
    
    company_id=models.IntegerField(null=True,default=0)    #公司ID
    full_name=models.CharField(max_length=100,null=True,default=None)    #公司名称
    short_name=models.CharField(max_length=40,null=True,default=None)    #公司简称
    a_code=models.CharField(max_length=12,null=True,default=None)    #A股股票代码
    b_code=models.CharField(max_length=12,null=True,default=None)    #B股股票代码
    h_code=models.CharField(max_length=12,null=True,default=None)    #H股股票代码
    fullname_en=models.CharField(max_length=100,null=True,default=None)    #英文名称
    shortname_en=models.CharField(max_length=40,null=True,default=None)    #英文简称
    legal_representative=models.CharField(max_length=40,null=True,default=None)    #法人代表
    register_location=models.CharField(max_length=100,null=True,default=None)    #注册地址
    office_address=models.CharField(max_length=150,null=True,default=None)    #办公地址
    zipcode=models.CharField(max_length=10,null=True,default=None)    #邮政编码    varchar(10)    
    register_capital=models.DecimalField(max_digits=20,decimal_places=4,default=0)    #注册资金,单位：万元
    currency_id=models.IntegerField(null=True,default=None)    #货币编码
    currency=models.CharField(max_length=32,null=True,default=None)    #货币名称
    establish_date=models.DateField(null=True,default=None)    #成立日期
    website=models.CharField(max_length=80,null=True,default=None)    #机构网址
    email=models.CharField(max_length=80,null=True,default=None)    #电子信箱
    contact_number=models.CharField(max_length=60,null=True,default=None)    #联系电话
    fax_number=models.CharField(max_length=60,null=True,default=None)    #联系传真
    main_business=models.CharField(max_length=500,null=True,default=None)    #主营业务    varchar(500)  
    business_scope=models.CharField(max_length=4000,null=True,default=None)    #经营范围    varchar(4000)  
    description=models.CharField(max_length=4000,null=True,default=None)    #机构简介    varchar(4000)    
    tax_number=models.CharField(max_length=50,null=True,default=None)    #税务登记号    varchar(50)    
    license_number=models.CharField(max_length=40,null=True,default=None)    #法人营业执照号    varchar(40)
    pub_newspaper=models.CharField(max_length=120,null=True,default=None)    #指定信息披露报刊   
    pub_website=models.CharField(max_length=120,null=True,default=None)    #指定信息披露网站 
    secretary=models.CharField(max_length=40,null=True,default=None)    #董事会秘书    varchar(40)
    secretary_number=models.CharField(max_length=60,null=True,default=None)    #董秘联系电话    varchar(60)
    secretary_fax=models.CharField(max_length=60,null=True,default=None)    #董秘联系传真    varchar(60)    
    secretary_email=models.CharField(max_length=80,null=True,default=None)    #董秘电子邮箱    varchar(80)  
    security_representative=models.CharField(max_length=40,null=True,default=None)    #证券事务代表    varchar(40)   
    province_id=models.CharField(max_length=12,null=True,default=None)    #所属省份编码    varchar(12)   
    province=models.CharField(max_length=60,null=True,default=None)    #所属省份    varchar(60) 
    city_id=models.CharField(max_length=12,null=True,default=None)    #所属城市编码    varchar(12)       
    city=models.CharField(max_length=60,null=True,default=None)    #所属城市    varchar(60)
    industry_id=models.CharField(max_length=12,null=True,default=None)    #行业编码    varchar(12)    证监会行业分类
    industry_1=models.CharField(max_length=60,null=True,default=None)    #行业一级分类    varchar(60)    
    industry_2=models.CharField(max_length=60,null=True,default=None)    #行业二级分类    varchar(60)
    cpafirm=models.CharField(max_length=200,null=True,default=None)    #会计师事务所    varchar(200)    
    lawfirm=models.CharField(max_length=200,null=True,default=None)    #律师事务所    varchar(200)    
    ceo=models.CharField(max_length=100,null=True,default=None)    #总经理    varchar(100)   
    comments=models.CharField(max_length=500,null=True,default=None)    #备注    varchar(300)     


#上市公司的股东和股本信息
class CapitalChange(models.Model):
    """
    获取上市公司股本变动信息
    jqData:finance.STK_CAPITAL_CHANGE
    
    说明：数据比较老，是2017年的数据
    """
    securities=models.ForeignKey(Securities,on_delete=models.CASCADE)
    
    company_id=models.IntegerField(null=True,default=0)    #公司ID
    company_name=models.CharField(max_length=100,null=True,default=None)    #公司名称    varchar(100)    
    #code=models.CharField(max_length=12,null=True,default=None)    #股票代码    varchar(12)    
    change_date=models.DateField(null=True,default=None)    #变动日期    date    
    pub_date=models.DateField(null=True,default=None)    #公告日期    date    
    change_reason_id=models.IntegerField(null=True,default=0)    #变动原因编码    int    
    change_reason=models.CharField(max_length=120,null=True,default=None)    #变动原因    varchar(120)    
    share_total=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #总股本    decimal(20,4)    未流通股份+已流通股份，单位：万股
    share_non_trade=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #未流通股份    decimal(20,4)    发起人股份 + 募集法人股份 + 内部职工股 + 优先股+转配股+其他未流通股+配售法人股+已发行未上市股份
    share_start=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #发起人股份    decimal(20,4)    国家持股 +国有法人持股+境内法人持股 + 境外法人持股 + 自然人持股
    share_nation=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #国家持股    decimal(20,4)    
    share_nation_legal=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #国有法人持股    decimal(20,4)    
    share_instate_legal=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #境内法人持股    decimal(20,4)    
    share_outstate_legal=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #境外法人持股    decimal(20,4)    
    share_natural=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #自然人持股    decimal(20,4)    
    share_raised=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #募集法人股    decimal(20,4)    
    share_inside=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #内部职工股    decimal(20,4)    
    share_convert=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #转配股    decimal(20,4)    
    share_perferred=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #优先股    decimal(20,4)    
    share_other_nontrade=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他未流通股    decimal(20,4)    
    share_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #流通受限股份    decimal(20,4)    
    share_legal_issue=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #配售法人股    decimal(20,4)    战略投资配售股份+证券投资基金配售股份+一般法人配售股份
    share_strategic_investor=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #战略投资者持股    decimal(20,4)    
    share_fund=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    # 证券投资基金持股    decimal(20,4)    
    share_normal_legal=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #一般法人持股    decimal(20,4)    
    share_other_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他流通受限股份    decimal(20,4)    
    share_nation_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #国家持股（受限）    decimal(20,4)    
    share_nation_legal_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #国有法人持股（受限）    decimal(20,4)    
    other_instate_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他内资持股（受限）    decimal(20,4)    
    legal_of_other_instate_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他内资持股（受限）中的境内法人持股    decimal(20,4)    
    natural_of_other_instate_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    # 其他内资持股（受限）中的境内自然人持股    decimal(20,4)    
    outstate_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #外资持股（受限）    decimal(20,4)    
    legal_of_outstate_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #外资持股（受限）中的境外法人持股    decimal(20,4)    
    natural_of_outstate_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #外资持股（受限）境外自然人持股    decimal(20,4)    
    share_trade_total=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #已流通股份（自由流通股）    decimal(20,4)    人民币普通股 + 境内上市外资股（B股）+ 境外上市外资股（H股）+高管股+ 其他流通股
    share_rmb=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #人民币普通股    decimal(20,4)    
    share_b=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #境内上市外资股（B股）    decimal(20,4)    
    share_b_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #限售B股    decimal（20,4）    
    share_h=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    # 境外上市外资股（H股）    decimal(20,4)    
    share_h_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #限售H股    decimal(20,4)    
    share_management=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    # 高管股    decimal(20,4)    
    share_management_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #限售高管股    decimal(20,4)    
    share_other_trade=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他流通股    decimal(20,4)    
    control_shareholder_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #控股股东、实际控制人(受限)    decimal(20,4)    
    core_employee_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #核心员工(受限)    decimal(20,4)    
    individual_fund_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    # 个人或基金(受限)    decimal(20,4)    
    other_legal_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他法人(受限)    decimal(20,4)    
    other_limited=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #其他(受限)    decimal(20,4)    
    
    
class ShareholderTop10(models.Model):
    """
    获取上市公司的十大股东数据
    jqdata:finance.STK_SHAREHOLDER_TOP10
    """
    securities=models.ForeignKey(Securities,on_delete=models.CASCADE)
    
    company_id=models.IntegerField(null=True,default=0)    #公司ID   
    company_name=models.CharField(max_length=100,null=True,default=None)    #公司名称    varchar(100)        
    end_date=models.DateField(null=True,default=None)    #截止日期    date    公告中统计的十大股东截止到某一日期的更新情况。
    pub_date=models.DateField(null=True,default=None)    #公告日期    date    公告中会提到十大股东的更新情况。
    change_reason_id=models.IntegerField(null=True,default=0)    #变动原因编码    int    
    change_reason=models.CharField(max_length=120,null=True,default=None)    #变动原因    varchar(120)    
    shareholder_rank=models.IntegerField(null=True,default=0)    # 股东名次    int    
    shareholder_name=models.CharField(max_length=200,null=True,default=None)    #股东名称    varchar(200)    
    shareholder_name_en=models.CharField(max_length=200,null=True,default=None)    #股东名称（英文）    varchar(200)    
    
    shareholder_id=models.IntegerField(null=True,default=0)    #股东ID    int    
    shareholder_class_id=models.IntegerField(null=True,default=0)    #股东类别编码    int    
    shareholder_class=models.CharField(max_length=120,null=True,default=None)    #股东类别    varchar(150)    包括:券商、社保基金、证券投资基金、保险公司、QFII、其它机构、个人等
    share_number=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #持股数量    decimal(10,4)    股
    share_ratio=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #持股比例    decimal(10,4)    %
    sharesnature_id=models.IntegerField(null=True,default=0)    #股份性质编码    int    
    sharesnature=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #股份性质    varchar(120)    包括:国家股、法人股、个人股外资股、流通A股、流通B股、职工股、发起人股、转配股等
    share_pledge_freeze=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #股份质押冻结数量    decimal(10,4)    如果股份质押数量和股份冻结数量任意一个字段有值，则等于后两者之和
    
    share_pledge=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #股份质押数量    decimal(10,4)    
    share_freeze=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #股份冻结数量    decimal(10,4)    
    
class ShareholderFloatingTop10(models.Model):
    """
    获取上市公司十大流通股东
    jqdata:finance.STK_SHAREHOLDER_FLOATING_TOP10
    """
    securities=models.ForeignKey(Securities,on_delete=models.CASCADE)
    
    company_id=models.IntegerField(null=True,default=0)    #公司ID   
    company_name=models.CharField(max_length=100,null=True,default=None)    #公司名称    varchar(100)        

    end_date=models.DateField(null=True,default=None)    #截止日期    date    公告中统计的十大股东截止到某一日期的更新情况。
    pub_date=models.DateField(null=True,default=None)    #公告日期    date    公告中会提到十大股东的更新情况。
    
    change_reason_id=models.IntegerField(null=True,default=0)    #变动原因编码    int    
    change_reason=models.CharField(max_length=120,null=True,default=None)    #变动原因    varchar(120)    
    shareholder_rank=models.IntegerField(null=True,default=0)    # 股东名次    int    
    shareholder_name=models.CharField(max_length=200,null=True,default=None)    #股东名称    varchar(200)    
    shareholder_name_en=models.CharField(max_length=200,null=True,default=None)    #股东名称（英文）    varchar(200)  
    shareholder_class_id=models.IntegerField(null=True,default=0)    #股东类别编码    int    
    shareholder_class=models.CharField(max_length=120,null=True,default=None)    #股东类别    varchar(150)    包括:券商、社保基金、证券投资基金、保险公司、QFII、其它机构、个人等
    share_number=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #持股数量    decimal(10,4)    股
    share_ratio=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #持股比例    decimal(10,4)    %
    sharesnature_id=models.IntegerField(null=True,default=0)    #股份性质编码    int    
    sharesnature=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #股份性质    varchar(120)    包括:国家股、法人股、个人股外资股、流通A股、流通B股、职工股、发起人股、转配股等 
    
class HolderNum(models.Model):
    """
    上市公司的股东数
    jqdata:finance.STK_HOLDER_NUM
    """
    securities=models.ForeignKey(Securities,on_delete=models.CASCADE)
    end_date=models.DateField(null=True,default=None)    #截止日期    date    公告中统计的十大股东截止到某一日期的更新情况。
    pub_date=models.DateField(null=True,default=None)    #公告日期    date    公告中会提到十大股东的更新情况。
    
    share_holders=models.IntegerField(null=True,default=0)    #股东总户数    int    
    a_share_holders=models.IntegerField(null=True,default=0)    #A股股东总户数    int    
    b_share_holders=models.IntegerField(null=True,default=0)    #B股股东总户数    int    
    h_share_holders=models.IntegerField(null=True,default=0)    #H股股东总户数    int
    
class SharelodersShareChange(models.Model):
    """
    上市公司大股东的增减持情况
    jqdata:finance.STK_SHAREHOLDERS_SHARE_CHANGE
    """
    securities=models.ForeignKey(Securities,on_delete=models.CASCADE)
    
    company_id=models.IntegerField(null=True,default=0)    #公司ID   
    company_name=models.CharField(max_length=100,null=True,default=None)    #公司名称    varchar(100)        

    end_date=models.DateField(null=True,default=None)    #截止日期    date    公告中统计的十大股东截止到某一日期的更新情况。
    pub_date=models.DateField(null=True,default=None)    #公告日期    date    公告中会提到十大股东的更新情况。
    
    type=models.IntegerField(null=True,default=0)    #增（减）持类型    int    0--增持;1--减持
    
    shareholder_id=models.IntegerField(null=True,default=0)    #股东ID    int      
    shareholder_name=models.CharField(max_length=200,null=True,default=None)    #股东名称    varchar(200)   
    change_number=models.IntegerField(null=True,default=0)    #变动数量    int    股
    change_ratio=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #变动数量占总股本比例    decimal(10,4)    录入变动数量后，系统自动计算变动比例，持股比例可以用持股数量除以股本情况表中的总股本
    price_ceiling=models.CharField(max_length=200,null=True,default=None)    #增（减）持价格上限    varchar(100)    公告里面一般会给一个增持或者减持的价格区间，上限就是增持价格或减持价格的最高价。如果公告中只披露了平均价，那price_ceiling即为成交均价
    after_change_ratio=models.DecimalField(max_digits=20,decimal_places=4,default=0,null=True)    #变动后占比    decimal(10,4)    %，变动后持股数量占总股本比例