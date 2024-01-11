# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: 段海洋
# @Time: 2022年8月月31日 9:14
# ---

from mysql_ops import query_mysql


def excute_sql(DB, SQL):
    """数据库执行sql：update、
    delete from、
    select 、
    insert into"""
    result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
    return result
