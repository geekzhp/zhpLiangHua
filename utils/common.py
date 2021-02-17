import re
import jqdatasdk as jq

def jqdataAuth():
    auth=True
    try:
        jq.auth('18009020072','4187Xslc61')
    except Exception as e:
        print('登陆失败')
        auth=False
    return auth

def convertCode(codeStr):
    """
    将股票代码，转换为jqdata的code格式
    XSHG:上海证券交易所的后缀
        6**：上海A股
        9**：上海B股
        5**：上海基金
    XSHE：深圳交易所后缀
    
    问题：不适合上交所、深交所以外的金融产品代码转换
    """
    
    #codeStr='sh600000'
    codeStr=codeStr.strip()
    code=''
    for s in codeStr:
        if s.isdecimal():
            code=code+s
    
    code=code.zfill(6)+'.XSHE' if len(code)<6 and len(code)>0 else code
    if len(code)==6:
        code=code+'.XSHG' if code[0:1]=='6' or s[0:1]=='9' or s[0:1]=='5' else code+'.XSHE'
            
    
    return code
    

if __name__=="__main__":
    convertCode('40000011')