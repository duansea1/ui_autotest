# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-12-29 16:40
# ---
from redis import Redis
import time

from demo.API_demo.commons import mysql_ops, time_tools

from demo.API_demo.baofu_method.shop_method import *

# 商城数据库
DBs = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
       "port": 3306, "data": "zw_shop"}
DB_MANDAO_SHOP = {"host": "10.254.110.27", "user": "scrm", "password": "scrm@135qwe",
       "port": 3306, "data": "zw_shop"}

DB_MANDAO_UCENTER = {"host": "10.254.110.27", "user": "scrm", "password": "scrm@135qwe",
       "port": 3306, "data": "ucenter"}


def execute_sql(DB, SQL):
    """
       传入DB数据，及sql执行sql
       :param DB: DB数据
       :param SQL: 需要执行的sql
       :return: sql执行的结果
       """
    result = mysql_ops.query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
    return result


def delete_shop_user(open_kid):
    """删除商城用户及会员

    TODO: ucenter 表需要删除相关的会员数据
    select * from zw_shop.zw_user where mobile = '15256818112';
    select * from zw_shop.zw_member where mobile = '15256818112';
    select * from zw_shop.zw_wx_user where wx_mobile = '15256818112';

    select * from ucenter.zw_kyd_member_v2 where mobile = '15256818112';
    select * from ucenter.zw_kyd_member_shop_v2 where mobile = '15256818112' and channel_id = 1;
    select * from ucenter.zw_kyd_member_shop_info_v2 where mobile = '15256818112' and channel_id = 1;
    """
    for sql in delete_shop_user_sqls(open_kid):
        print('执行的sql：', sql)
        res = execute_sql(DB_MANDAO_SHOP, sql)
        if res['code'] == 0:
            print(f"执行成功结果：{res}\n受影响的数据量：{res['rows']}")
            continue
        else:
            print('error----执行失败结果：', res)
            break

def delete_shop_user_scrm(moblie):
    """删除scrm端客易达店铺会员的关系"""
    for sql in delete_shop_to_scrm_user_sqls(moblie):
        print('执行的sql：', sql)
        res = execute_sql(DB_MANDAO_UCENTER, sql)
        if res['code'] == 0:
            print(f"执行成功结果：{res}\n受影响的数据量：{res['rows']}")
            continue
        else:
            print('error----执行失败结果：', res)
            break

def delete_shop_user_scrm_data(open_kid, moblie):
    # 删除客易达商城的用户会员and与scrm客户的关系
    delete_shop_user(open_kid=open_kid)
    delete_shop_user_scrm(moblie=moblie)


if __name__ == '__main__':
    # 删除商城的用户
    # delete_shop_user(open_kid="OKIDEYjqqVAb9PHVWrHU9iaHfQ7JmEqo")

    # 删除商城会员与scrm会员的关系
    # delete_shop_user_scrm(moblie='17681032991')

    # delete_shop_user_scrm_data(open_kid="OKIDEYjqqVAb9PHVWrHU9iaHfQ7JmEqo", moblie='17681032991')
    # delete_shop_user_scrm_data(open_kid="OKID3dwHRux4XvAjWCmpemk3ruiE3T2c", moblie='18321740710')

    #     OKIDEYjqqVAb9PHVWrHU9iaHfQ7JmEqo ---2991手机号
    # OKIDBHGHsux9VqcA2xdTbYPFtcYSeP9c-之前的2991关联的openid
    import os
    print(os.path)
