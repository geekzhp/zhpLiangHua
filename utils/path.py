import os
import datetime

#try:
#     import QUANTAXIS as QA
#     from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION
#     from QUANTAXIS.QAData.QADataStruct import (
#         QA_DataStruct_Index_min, 
#         QA_DataStruct_Index_day, 
#         QA_DataStruct_Stock_day, 
#         QA_DataStruct_Stock_min,
#         QA_DataStruct_CryptoCurrency_day,
#         QA_DataStruct_CryptoCurrency_min,
#         )
#     from QUANTAXIS.QAIndicator.talib_numpy import *
#     from QUANTAXIS.QAUtil.QADate_Adv import (
#         QA_util_timestamp_to_str,
#         QA_util_datetime_to_Unix_timestamp,
#         QA_util_print_timestamp
#     )
#     from QUANTAXIS.QAUtil.QALogs import (
#         QA_util_log_info, 
#         QA_util_log_debug,
#         QA_util_log_expection)
#     from QUANTAXIS.QAFetch.QAhuobi import (
#         FIRST_PRIORITY,
#     )
# except:
#     print('PLEASE run "pip install QUANTAXIS" before call GolemQ.utils.path modules')
#     pass


"""创建本地文件夹
1. setting_path ==> 用于存放配置文件 setting.cfg
2. cache_path ==> 用于存放临时文件
3. log_path ==> 用于存放储存的log
4. download_path ==> 下载的数据/财务文件
5. strategy_path ==> 存放策略模板
6. bin_path ==> 存放一些交易的sdk/bin文件等
"""

basepath = os.getcwd()
path = os.path.expanduser('~')
user_path = '{}{}{}'.format(path, os.sep, '.GolemQ')
#cache_path = os.path.join(user_path, 'datastore', 'cache')


def mkdirs(dirname):
    if not (os.path.exists(os.path.join(basepath, dirname)) and \
        os.path.isdir(os.path.join(basepath, dirname))):
        print(u'文件夹',dirname,'不存在，重新建立')
        #os.mkdir(dirname)
        os.makedirs(os.path.join(basepath, dirname))
    return os.path.join(basepath, dirname)

