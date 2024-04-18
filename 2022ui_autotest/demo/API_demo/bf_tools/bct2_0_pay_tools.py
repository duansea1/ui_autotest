# -*- coding: utf-8 -*-
# 说明：宝财通2.0支付工具类-测试环境删除账号工具
# @Author: duansea
# @Time: 2024-04-17 15:59
# ---
import logging

from redis import Redis
import time
from demo.API_demo.commons.sqlrecords import excute_sql
from demo.API_demo.baofu_method.juhe_pay_methods import Aggregatd_Payment
from demo.API_demo.commons.time_tools import TimeTool
from demo.API_demo.commons.bf_request import request_bct_del_account
from icecream import ic


SCRM_payhub = {"host": "10.254.110.27", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "zw_payhub"}

@TimeTool().snap_time
def delete_zw_payhub_data_tool(crop_code):
    """"
    正式：删除商户资料
    @query_corp_unified_social_credit_code_sql：统一社会信用代码
    """
    openNo, corp_name = query_bct_openNo(crop_code)
    ic(openNo)
    T = TimeTool()
    with open('./bct2.0删除数据记录表.txt', "a") as f:
        f.write(f"\n删除时间：{T.current_time()}企业名称：{corp_name}，登录号：{openNo}，统一社会信用代码："
                f"{crop_code}\n")
    # logger = logging.basicConfig(filename='')
    if openNo:
        res = request_bct_del_account(openNo)
        if res:
            print('宝财通2.那边返回信息', res)
        print("宝财通2.0登录号，删除完成！！！")
    # 删除商户相关的数据
    user_sqls = Aggregatd_Payment().delete_zw_payhub_data(openNo)
    n = 0
    for sql in user_sqls:
        n = n + 1
        result = excute_sql(DB=SCRM_payhub, SQL=sql)
        # ic(result)
        if result['code'] != 0:
            raise Exception('excue sqls is fail')
        print('数据执行结果:', ['第' + str(n) + '次', result, sql])

def query_bct_openNo(crop_code):
    sql = Aggregatd_Payment().query_bct_openNo_sql(crop_code)
    ic(sql)
    result = excute_sql(DB=SCRM_payhub, SQL=sql)
    ic(result)
    if len(result['data']) > 0:
        return result['data'][0][0], result['data'][0][1]
    print("数据库没有查到openNo")
    return False

if __name__ == '__main__':
    pass
    # 删除宝财通2.0账号91500000MA5U7B0T99--富民银行
    delete_zw_payhub_data_tool('91500000MA5U7B0T99')
