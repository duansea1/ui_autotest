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
    """删除商城用户"""
    for sql in delete_shop_user_sqls(open_kid):
        print('执行的sql：', sql)
        res = execute_sql(DB_MANDAO_SHOP, sql)
        print('执行结果：', res)


if __name__ == '__main__':
    # 删除商城的用户
    delete_shop_user(open_kid="OKIDBHGHsux9VqcA2xdTbYPFtcYSeP9c")
