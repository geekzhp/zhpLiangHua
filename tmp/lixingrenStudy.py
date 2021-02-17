import requests
'''
Created on 2020年12月24日

@author: My
'''

"4b410394-5e11-4351-9c32-4f8bf3b7a12c"

lxrToken='4b410394-5e11-4351-9c32-4f8bf3b7a12c'
lxrFeiJinRongURL='https://open.lixinger.com/api/a/stock/fundamental/non_financial'

d={
    "token": lxrToken,
    "date": "2020-04-01",
    "stockCodes": [
        "000028",
        "600511"
    ],
    "metricsList": [
        "pe_ttm",
        "mc"
    ]
}

r=requests.post(lxrFeiJinRongURL,data=d)
print(r.text)