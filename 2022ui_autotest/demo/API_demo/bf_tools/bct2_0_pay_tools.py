# -*- coding: utf-8 -*-
# 说明：宝财通2.0支付工具类-测试环境删除账号工具
# @Author: duansea
# @Time: 2024-04-17 15:59
# ---
import logging

from redis import Redis
import time
from API_demo.commons.sqlrecords import excute_sql
from API_demo.baofu_method.juhe_pay_methods import Aggregatd_Payment
from API_demo.commons.time_tools import TimeTool
from API_demo.commons.bf_request import request_bct_del_account
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
    merchant_no = query_bct_merchant_no(openNo)
    T = TimeTool()
    with open('./bct2.0删除数据记录表.txt', "a") as f:
        f.write(f"\n删除时间：{T.current_time()}企业名称：{corp_name}，bct登录号：{merchant_no}，统一社会信用代码："
                f"{crop_code}\n")
    # logger = logging.basicConfig(filename='')
    if merchant_no:
        res = request_bct_del_account(merchant_no)
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
    """
    根据统一社会信用代码查询bct登录号
    """
    sql = Aggregatd_Payment().query_bct_openNo_sql(crop_code)
    # ic(sql)
    result = excute_sql(DB=SCRM_payhub, SQL=sql)
    # ic(result)
    if len(result['data']) > 0:
        return result['data'][0][0], result['data'][0][1]
    raise Exception("数据库没有查到openNo")

def query_bct_merchant_no(openNo):
    sql = Aggregatd_Payment().query_bct_merchant_no_sql(openNo)
    # ic('merchant_no:', sql)
    result = excute_sql(DB=SCRM_payhub, SQL=sql)
    ic(result)
    if len(result['data']) > 0:
        return result['data'][0][0]
    print("数据库没有查到merchant_no")
    return False

if __name__ == '__main__':
    pass
    # 删除宝财通2.0账号91500000MA5U7B0T99--富民银行
    # 913101153125976353--众玩网络
    # 91110109MA01KK2M45--北京交个朋友
    # CM690000000008090628   91320115608968458N-南京
    # 1792838487997681664-wang
    delete_zw_payhub_data_tool('320681199205188024')
