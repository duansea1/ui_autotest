# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年8月月25日 9:36
# ---
from redis import Redis
import time
from commons.mysql_ops import *

DBs = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
       "port": 3306, "data": "zw_shop"}
SCRM_lingshou = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}

SCRM_scrm = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "scrm"}


class ConvenientScript(object):
    """便捷脚本：如删除账户、"""
    # 商城
    DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
          "port": 3306, "data": "zw_shop"}
    # 租户绑定账户关系表 zw_bht_account_bind_record
    # 宝付支付渠道表zw_payment

    # SCRM-DB
    SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
               "port": 3306, "data": "lingshou"}

    # 数据库：
    def query_sql(self, DB, SQL):
        """数据库执行sql：update、
        delete from、
        select 、
        insert into"""
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def scrm_sql(self, DB, SQL):
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def insert_many_data(self,exc_sql, DB):
        """
        :param sql: insert语句
        :return: 返回结果
        """
        return self.scrm_sql(DB, SQL=exc_sql)

    def exce_insert_sql(self):
        """"
        """
        product_id = 20000
        taoword = '第2波测试淘口令'
        strategy_id = 166666666
        while product_id < 20000:
            insert_sql = "INSERT INTO `scrm`.`zw_tb_promotion_record`(`tenant_id`, `corp_id`, `shop_id`, `group_id`, " \
                         "`retail_product_id`, `type`, `way`, `tao_pass_word`, `strategy_id`, " \
                         "`is_deleted`, `created_at`, `created_uid`, `updated_at`, `deleted_at`) " \
                         "VALUES ( 237, 320, 351, " \
                         "1166," + str(product_id) + ", 1, 2, '" + str(taoword) + "'," + str(strategy_id) + \
                         ", 2, '2023-08-23 10:29:58'," + str(product_id) +",'2023-08-25 15:22:28', NULL);"
            print(insert_sql)
            self.scrm_sql(DB=SCRM_scrm, SQL=insert_sql)
            taoword = '测试淘口令' + str(product_id)
            product_id += 1
            strategy_id += 1


if __name__ == '__main__':
    pass
    """删除测试环境-宝户通账户信息"""
    excue = ConvenientScript()
    excue.exce_insert_sql()

