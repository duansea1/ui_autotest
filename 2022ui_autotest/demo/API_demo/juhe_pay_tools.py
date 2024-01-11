# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-24 17:59
# ---
import logging

from redis import Redis
import time
from commons.sqlrecords import excute_sql
from baofu_method.juhe_pay_methods import Aggregatd_Payment
from commons.time_tools import TimeTool
from commons.bf_request import request_bf_del_account

SCRM_payhub = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "payhub"}

@TimeTool().snap_time
def delete_payhub_data_tool(corp_unified_social_credit_code):
    """"
    正式：删除商户资料
    @corp_unified_social_credit_code：统一社会代码
    """
    openNo = query_openNo(corp_unified_social_credit_code)
    T = TimeTool()
    with open('聚合开户删除数据记录表.txt', "a") as f:
        f.write("\n" + str(T.current_time()) + str(openNo) + ":对应的统一社会代码 "
                + str(corp_unified_social_credit_code) + "\t")
    # logger = logging.basicConfig(filename='')
    if openNo:
        res = request_bf_del_account(loginNo=openNo, usertype='MERCHANT')
        if res:
            print('宝付那边返回信息', res)
        print("宝付登录号，删除完成！！！")
    # 删除商户相关的数据
    usersql = Aggregatd_Payment().delete_payhub_data(corp_unified_social_credit_code)
    n = 0
    for sql in usersql:
        # print('usersql:', usersql)
        n = n + 1
        result = excute_sql(DB=SCRM_payhub, SQL=sql)
        if result['code'] != 0:
            raise Exception('excue sqls is fail')
        print('数据执行结果:', ['第' + str(n) + '次', result, sql])

def query_openNo(corp_unified_social_credit_code):
    sql = Aggregatd_Payment().query_openNO_sql(corp_unified_social_credit_code)
    result = excute_sql(DB=SCRM_payhub, SQL=sql)
    if len(result['data']) > 0:
        return result['data'][0][0]
    print("数据库没有查到openNo")
    return False


if __name__ == '__main__':
    pass
    # 删除宝付账户和数据库的数据
    delete_payhub_data_tool('913101180625739120')
    # query_openNo('1')
