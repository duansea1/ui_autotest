# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年4月月26日 9:36
# ---
from redis import Redis
import time
from commons.mysql_ops import *
from baofu_method.scrm_methods import Scrm_Lingshou
from commons.time_tools import TimeTool

DBs = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
       "port": 3306, "data": "zw_shop"}
SCRM_lingshou = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
SCRM_USER = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "ucenter"}
SCRM_scrm = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "scrm"}

class KydRedis():
    """操作客易达redis"""
    # 连接redis服务器 password:vhEA1jf4
    redis_connect = Redis(host='47.103.9.199', port=6379, db=3, password='vhEA1jf4', decode_responses=True)

    def get_Skey(self, key=None, type=None):
        '''获取指定key的value，对齐执行操作'''
        time.sleep(1)
        return self.redis_connect.get(key)

    def get_pipline(self, key):
        pipe = self.redis_connect.keys(pattern=key)
        del_res = self.redis_connect.delete()
        return pipe

    def del_pipline_keys(self, *args, **kwargs ):
        pipe = self.redis_connect
        re = pipe.zrem(*args, **kwargs)
        print(pipe.zrange('MEMBER_ORDER_TIME:237_320_472840800674680833', 0, 300))
        return re

    def delete_redis_key(self, key):
        """redis删除对应的key
        key='points_experience_rule:56-56'--测试环境：宝付店铺-对应scrm
        """
        result = self.get_Skey(key)
        if result != None:
            '''执行delete'''
            re = self.redis_connect.delete(key)
            return {'code': 0, 'msg': '删除成功' + key, 'data': [re]}
        else:
            return {'code': 1, 'msg': 'redis中没有找到指定key', 'data': []}

    def get_phone_sms_code(self, phone):
        """
        :param phone: 手机号 api_platform_sms_login_code_13166210872
        :return:
        """
        key = 'api_platform_sms_login_code_' + str(phone)
        return self.redis_connect.get(key)


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

    def delete_baofoo_account_pay(self, login_no, isd='1'):
        """说明：删除小程序下绑定的宝付支付"""
        sqls = []
        # #  1\zw_bht_account_bind_record--宝付企业个人个体账户绑定关系表
        # SELECT * from  zw_bht_account_bind_record WHERE login_no = '4II9Zah0GeD1sWJhdKOB';
        record_sql = ("update zw_bht_account_bind_record set is_deleted ="
                      + isd + " WHERE login_no ='" + login_no + "'")
        sqls.append(record_sql)
        # #  2|2\ '用户实名认证表'--zw_bht_pay_user_autonym
        user_autonym_sql = ("update zw_bht_pay_user_autonym set is_deleted ="
                            + isd + " WHERE login_no ='" + login_no + "'")
        sqls.append(user_autonym_sql)
        # 3、对公企业开户：zw_bht_corporation_account_open--删除对应表的数据
        zw_bht_corporation_account_open_sql = ("update zw_bht_corporation_account_open set is_delete ="
                                               + isd + " "  "WHERE login_no ='" + login_no + "'")
        sqls.append(zw_bht_corporation_account_open_sql)
        # 4、 宝户通账户绑定表-zw_bht_account_bind_record
        zw_bht_account_bind_record_sql = ("update zw_bht_account_bind_record set is_deleted ="
                                          + isd + " WHERE bind_login_no ='" + login_no + "'")
        sqls.append(zw_bht_account_bind_record_sql)
        # 5\个人 zw_bht_user_bank_account--用户绑定银行卡表
        # SELECT * from zw_bht_user_bank_account where is_delete =2 and  login_no='dnxjwqe90m2DpXyCMWVd';
        # seleCT * from zw_user_bank_account where is_delete =2 and login_no='dnxjwqe90m2DpXyCMWVd';
        zw_bht_user_bank_account_sql = ("update zw_bht_user_bank_account set is_delete ="
                                        + isd + " WHERE login_no ='" + login_no + "'")
        zw_user_bank_account_sql = ("update zw_user_bank_account set is_delete ="
                                    + isd + " WHERE login_no ='" + login_no + "'")
        sqls.append(zw_bht_user_bank_account_sql)
        sqls.append(zw_user_bank_account_sql)
        # 6\个人实名认证表
        zw_autonym_sql1 = "update zw_autonym set is_deleted =" + isd + " WHERE login_no ='" + login_no + "'"
        user_autonym_sql2 = ("update zw_bht_pay_user_autonym set is_deleted ="
                             + isd + " WHERE login_no ='" + login_no + "'")
        sqls.append(zw_autonym_sql1)
        sqls.append(user_autonym_sql2)
        # 7\ 用户绑定银行卡表select * from `zw_user_bank_account`where login_no = 'dnxjwqe90m2DpXyCMWVd' and  is_delete =2;
        sql = "update zw_user_bank_account set is_delete =" + isd + " WHERE login_no ='" + login_no + "'"
        sqls.append(sql)
        print('需要执行的sql', sqls)
        DBshop = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
                  "port": 3306, "data": "zw_shop"}
        for sql in sqls:
            result = self.query_sql(DB=DBshop, SQL=sql)
            print('执行结果：', [result, sql])

        #  https://sp.baofoo.com/support-admin/mer/follow/del/logino?logino=FMmOR7VB0RCrYe66at71&usertype=PERSON

    def update_lingshou_user_order(self, r_userid, external_order_id, external_user_id, line='1c8aa0614e8f195b'):
        """零售电商，修改用户和订单关联的线路用户id
        """
        sqls = []
        # 零售电商-零售用户外部用户关系表-zw_retail_external_user_rela--更换线路id
        # @parm::line-线路id(b748d239e773f12d-线路3)
        # @parm:r_userid-渠道用户id
        user_sql = ("update zw_retail_external_user_rela set third_app_id ='"
                    + line + "' WHERE retail_user_id ='" + r_userid + "'")
        sqls.append(user_sql)
        # 用户+订单+线路-zw_retail_external_user_order_rela::
        # @parm:e_userid-外部用户id
        user_order_sql = ("update zw_retail_external_user_order_rela set third_app_id ='"
                          + line + "' WHERE external_order_id ='"
                          + external_order_id + "'" + "and external_user_id='" + external_user_id + "'")
        sqls.append(user_order_sql)
        # 订单湖+线路-zw_retail_order_lake
        order_lake_sql = ("update zw_retail_order_lake set third_app_id ='"
                          + line + "' WHERE external_order_id ='"
                          + external_order_id + "'" + "and external_user_id='" + external_user_id + "'")
        sqls.append(order_lake_sql)
        # 订单日志+线路-zw_retail_order_lake_log
        order_lakelog_sql = ("update zw_retail_order_lake_log set third_app_id ='"
                             + line + "' WHERE external_order_id ='" + external_order_id + "'"
                             + "and external_user_id='" + external_user_id + "'")
        sqls.append(order_lakelog_sql)
        SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
        print('打印scrmsql', sqls)
        for sql in sqls:
            result = self.query_sql(DB=SCRM_DB, SQL=sql)
            print('执行结果：', [result, sql])

    def update_all_lingshou_user_order(self, old_line, line='1c8aa0614e8f195b'):
        '''零售电商，修改用户和订单关联的线路用户id'''
        sqls = []
        # 零售电商-零售用户外部用户关系表-zw_retail_external_user_rela--更换线路id
        # @parm::line-线路id(b748d239e773f12d-线路3)
        # @parm:r_userid-渠道用户id
        user_sql = ("update zw_retail_external_user_rela set third_app_id ='"
                    + line + "' WHERE third_app_id !='" + old_line + "'")
        sqls.append(user_sql)
        # 用户+订单+线路-zw_retail_external_user_order_rela::
        # @parm:e_userid-外部用户id
        user_order_sql = ("update zw_retail_external_user_order_rela set third_app_id ='"
                          + line + "' WHERE third_app_id !='" + old_line + "'")
        sqls.append(user_order_sql)
        # 订单湖+线路-zw_retail_order_lake
        order_lake_sql = ("update zw_retail_order_lake set third_app_id ='"
                          + line + "' WHERE third_app_id !='" + old_line + "'")
        sqls.append(order_lake_sql)
        # 订单日志+线路-zw_retail_order_lake_log
        # order_lakelog_sql = "update zw_retail_order_lake_log set third_app_id ='"+line+"'
        # WHERE external_order_id ='" + external_order_id + "'" + "and external_user_id='" + external_user_id + "'"
        # sqls.append(order_lakelog_sql)

        SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
        print('打印scrmsql', sqls)
        for sql in sqls:
            result = self.query_sql(DB=SCRM_DB, SQL=sql)
            print('执行结果：', [result, sql])

    @TimeTool().snap_time
    def delete_lingshou_data(self, retail_userid, orderid, goodsid='', chanel=2):
        """"
        正式功能：删除指定用户(含统计的销售数据)、指定的订单、指定的商品数据
        不支持批量删除用户、商品、订单和行为
        @retail_userid----零售用户id
        @orderid ----订单id
        @:goodsid -商品id
        @chanel --渠道：2-有赞  7-
        """
        sqls = []
        SL = Scrm_Lingshou()
        # 删除用户相关的数据
        usersql = SL.delete_lingshou_user(retail_userid=retail_userid, chanel=2)
        sqls.extend(usersql)
        # 删除订单相关的数据
        ordersql = SL.delete_lingshou_order(orderid=orderid)
        sqls.extend(ordersql)
        # 删除商品相关的数据
        productsql = SL.delete_lingshou_product(goodsid=orderid)
        sqls.extend(productsql)
        # todo 删除客户相关的数据：收件人信息 consignee表

        # print('打印scrmsql:', sqls)
        n = 0
        for sql in sqls:
            n = n + 1
            result = self.query_sql(DB=SCRM_lingshou, SQL=sql)
            print('执行结果:', ['第' + str(n) + '次', result, sql])

    @TimeTool().snap_time
    def delete_lingshou_shop_data(self, external_shop_id, retail_shop_id):
        """"
        正式功能：shop删除店铺维度的数据（商品、用户、行为、订单）
        @external_shop_id----外部店铺id
        @retail_shop_id ----零售店铺id--scrm系统的店铺id
        """
        sqls = []
        SL = Scrm_Lingshou()
        # 删除用户相关的数据
        usersql = SL.delete_lingshou_user_shop(external_shop_id, retail_shop_id)
        sqls.extend(usersql)
        # 删除订单相关的数据
        ordersql = SL.delete_lingshou_order_shop(external_shop_id, retail_shop_id)
        sqls.extend(ordersql)
        # 删除商品相关的数据
        productsql = SL.delete_lingshou_product_shop(external_shop_id, retail_shop_id)
        sqls.extend(productsql)
        # todo 删除客户相关的数据：收件人信息 consignee表

        # print('打印scrmsql:', sqls)
        n = 0
        for sql in sqls:
            n = n + 1
            result = self.query_sql(DB=SCRM_lingshou, SQL=sql)
            print('删除店铺维度的数据执行结果:', ['第' + str(n) + '次', result, sql])

    def delete_DouDian_user_orderinfo(self, retail_userid, external_user_id='', orderid='',  goodsid='',
                                      del_product=False, chanel='99'):
        '''删除某一个订单及用户数据--适用与抖店

        @:chaenl: 2--代表有赞，需要删除有赞用户表、标识表
        '''
        sqls = []
        # 1、删除解密订单
        sql1 = "delete from zw_retail_order_decode_todo where external_order_id='" + orderid + "'"
        sqls.append(sql1)
        # 2、零售订单索引表
        sql2 = "delete from zw_retail_order_index where external_order_id='" + orderid + "'"
        sqls.append(sql2)
        # 3、零售用户外部订单关系表-zw_retail_external_order_rela
        sql3 = "delete from zw_retail_external_order_rela where external_order_id='" + orderid + "'"
        sqls.append(sql3)
        # 4、零售订单表-zw_retail_order
        sql4 = "delete from zw_retail_order where external_order_id='" + orderid + "'"
        sqls.append(sql4)
        # 5、零售用户外部订单关系表-zw_retail_external_shop_order_rela
        sql5 = "delete from zw_retail_external_shop_order_rela where external_order_id='" + orderid + "'"
        sqls.append(sql5)
        # 6、零售外部用户订单关系表-zw_retail_external_user_order_rela
        sql6 = "delete from zw_retail_external_user_order_rela where external_order_id='" + orderid + "'"
        sqls.append(sql6)
        # 7、零售外部订单客户关系表-zw_retail_order_cust_rela
        sql7 = "delete from zw_retail_order_cust_rela where external_order_id='" + orderid + "'"
        sqls.append(sql7)
        # 8、订单解密表-zw_retail_order_decode
        sql8 = "delete from zw_retail_order_decode where external_order_id='" + orderid + "'"
        sqls.append(sql8)

        # 9、零售外部订单商品表-zw_retail_order_goods
        sql9 = "delete from zw_retail_order_goods where external_order_id='" + orderid + "'"
        sqls.append(sql9)
        # 10、订单湖-zw_retail_order_lake
        sql10 = "delete from zw_retail_order_lake where external_order_id='" + orderid + "'"
        sqls.append(sql10)
        # 11、售后表-zw_retail_order_refund
        sql11 = "delete from zw_retail_order_refund where external_order_id='" + orderid + "'"
        sqls.append(sql11)
        # 12、子订单表-zw_retail_sub_order
        sql12 = "delete from zw_retail_sub_order where external_order_id='" + orderid + "'"
        sqls.append(sql12)
        # 13、用户行为表-zw_retail_user_behaviour
        sql13 = ("delete from zw_retail_user_behaviour where external_order_id='"
                 + orderid + "'" + "or retail_user_id='" + retail_userid + "'")
        sqls.append(sql13)
        # # 14、订单关联商品表-zw_retail_user_behaviour_goods
        # sql14 = "delete from zw_retail_user_behaviour_goods where external_order_id='" + orderid + "'"
        # sqls.append(sql14)

        # 15、零售用户外部用户关系表-zw_retail_external_user_rela
        sql15 = "delete from zw_retail_external_user_rela where retail_user_id='" + retail_userid + "'"
        sqls.append(sql15)
        # 16、店铺用户表-zw_retail_shop_user
        sql16 = "delete from zw_retail_shop_user where retail_user_id='" + retail_userid + "'"
        sqls.append(sql16)
        # 17、店铺用户索引表-zw_retail_shop_user_index
        sql17 = "delete from zw_retail_shop_user_index where retail_user_id='" + retail_userid + "'"
        sqls.append(sql17)
        # 18、零售用户表-zw_retail_user
        sql18 = "delete from zw_retail_user where retail_user_id='" + retail_userid + "'"
        sqls.append(sql18)
        # chanel=2为有赞用户，需要删除
        external_user_id1 =external_user_id
        if chanel == 2:
            # 删除有赞用户
            sql19 = "delete from zw_retail_youzan_account where external_user_id='" + external_user_id1 + "'"
            sqls.append(sql19)
            sql20 = "delete from zw_retail_external_account_logo where external_user_id='" + external_user_id1 + "'"
            sqls.append(sql20)


        if del_product == True:
            """删除商品数据"""
            # 1、商品线路表
            sql_product1 = "delete from zw_retail_external_goods_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product1)
            # 2、商品表-zw_retail_goods
            sql_product2 = "delete from zw_retail_goods where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product2)
            # 3、商品-类目表-zw_retail_goods_category_rela
            sql_product3 = "delete from zw_retail_goods_category_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product3)
            # 4、商品索引表-zw_retail_goods_index
            sql_product4 = "delete from zw_retail_goods_index where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product4)
            # 5、商品湖表-zw_retail_goods_lake
            sql_product5 = "delete from zw_retail_goods_lake where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product5)
            # 6、商品sku表-zw_retail_goods_sku_rela
            sql_product6 = "delete from zw_retail_goods_sku_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product6)
            # 7、商品shop表-zw_retail_shop_goods_rela
            sql_product7 = "delete from zw_retail_shop_goods_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product7)
            # # 8、商品shop表-zw_retail_shop_goods_rela
            # sql_product8 = "delete from zw_retail_shop_goods_rela where external_goods_id='" + goodsid + "'"
            # sqls.append(sql_product8)

        SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
        print('打印scrmsql', sqls)
        n = 0
        for sql in sqls:
            n = n + 1
            result = self.query_sql(DB=SCRM_DB, SQL=sql)
            print('执行结果:', ['第'+str(n)+'次', result, sql])

    def del_bind_member_data(self, external_user_id, member_no="sea", is_del_redis=False):
        """
        正式功能：删除会员绑定的渠道用户的订单数据
        :return:
        """
        SL = Scrm_Lingshou()
        exce_sqls = SL.unbinding_retail_data(external_user_id)
        n = 0
        for sql in exce_sqls:
            n += 1
            result = self.query_sql(DB=SCRM_USER, SQL=sql)
            print('删除会员绑定的渠道用户的订单数据:', ['第{}次'.format(n), result, sql])

        # rdis = KydRedis()
        keyword = "MEMBER_ORDER_TIME:237_320_" + member_no

        # result1 = rdis.del_pipline_keys('MEMBER_ORDER_TIME:237_320_472840800674680833', 'E20230404112909059800037')
        # # result2 = rdis.del_pipline_keys('MEMBER_ORDER_TIME', keyword)
        # print('redis返回结果：', result1)

    def del_member_redis_data(self, external_user_id):
        """
        正式功能：删除渠道用户-订单赠送积分成长值的数据
        @:param channel_order_sn---外部订单id
        :return:
        """

        # 删除数据库-订单订单赠送积分记录-zw_retail_order_rule_snapshot
        del_order_snapshot = ("delete from zw_retail_order_rule_snapshot where channel_order_sn in ("
                              + "select external_order_id from zw_retail_order where external_user_id='"
                              + external_user_id + "')")
        self.query_sql(DB=SCRM_scrm, SQL=del_order_snapshot)

        print("开始执行删除redis数据")
        get_user_order = ("select external_order_id from zw_retail_order where state in (4, 5) and external_user_id='"
                          + external_user_id + "'")
        orderids = self.query_sql(DB=SCRM_scrm, SQL=get_user_order)
        print(orderids,get_user_order)
        keys = []
        if orderids['data']:
            # print('查询执行结果:', ['返回结果：', orderids['data'], get_user_order])
            for orderid in orderids['data']:
                # print(orderid[0])
                keys.append("member_order_bonus_points_237_320_dd_" + orderid[0])
        else:
            print("slect没有查询到订单")
            return {'mag': "slect没有查询到订单"}
        # redis -订单送积分和成长值的缓存
        # 列子：member_order_bonus_points_237_320_dd_5040769236360353387
        # key_order = "member_order_bonus_points_237_320_dd_" + external_order_id
        if len(keys) == 0:
            print("slect没有查询到订单2")
            return {'mag':"没有查询到订单"}
        rds = KydRedis()
        # rds.delete_redis_key(keys)
        for key in keys:
            rds.delete_redis_key(key)
        return {'mag': "执行成功"}

    @TimeTool().snap_time
    def delete_demo_data(self, external_shop_id, retail_shop_id):
        """"
        demo：shop删除店铺维度的数据（商品、用户、行为、订单）
        @external_shop_id----外部店铺id
        @retail_shop_id ----零售店铺id--scrm系统的店铺id
        """
        SL = Scrm_Lingshou()
        # 删除用户相关的数据
        usersql = SL.delete_demo(external_shop_id, retail_shop_id)
        n = 0
        for sql in usersql:
            print('usersql:', usersql)
            n = n + 1
            result = self.query_sql(DB=SCRM_lingshou, SQL=sql)
            if result['code'] != 0:
                raise Exception('excue sqls is fail')
            print('demo-删除店铺维度的数据执行结果:', ['第' + str(n) + '次', result, sql])



if __name__ == '__main__':
    pass
    # reds = KydRedis()
    # # re_value = reds.get_Skey(key='points_experience_rule:56-56')
    # # print('返回的value:', re_value)
    #
    # # 删除对应的key，在会员管理系统-可以正常开通全域积分规则
    # res = reds.delete_redis_key(key='points_experience_rule:56-56')
    # print(res)

    # 获取手机号的验证码
    # print(reds.get_phone_sms_code(13166210872))
    # ConvenientScript
    """删除测试环境-宝户通账户信息"""
    excue = ConvenientScript()
    # login_no ='641525329622059712513'  # 需要删除的个人login_no
    # excue.delete_baofoo_account_pay(login_no,isd='1')

    '''更新用户、订单的线路id'''
    # 线路1：1c8aa0614e8f195b
    # 线路2：91b5c082a6cf042b
    # 线路3：b748d239e773f12d

    # excue.update_lingshou_user_order(r_userid='Px7rnJLZgn1nTkJmS3GyM', external_order_id='1915204298471438899',
    #                                  external_user_id='AAFt0YHcABD0D2GIOazWc05p', line='1c8aa0614e8f195b')

    """ 更新线路用户的线路为旧线路"""
    # excue.update_all_lingshou_user_order(old_line='b748d239e773f12d', line='1c8aa0614e8f195b')

    """ 
    抖店多线路--删除订单及其用户\ 商品的数据 
    """
    # 6920397821379024382\axXXCkXQJGF4M2apKggjn
    # excue.delete_DouDian_user_orderinfo(orderid='6920397821379024382', retail_userid='r6L4R5SBFSwyye9RSL8Kt', goodsid='3629814263113221043' , del_product=False)

    """有赞多线路--删除订单、用户"""
    # excue.delete_DouDian_user_orderinfo(retail_userid='rwuqCMrbrRT5uwUsb0Kfr',
    #                                     external_user_id='UwFln6wj647483955892744192', del_product=False, chanel=2)
    # excue.delete_lingshou_data(retail_userid='Tep6XSuNvXKQJpRdFBwGW', orderid='E20230915151433094506179')
    """ 查询用户的sql"""
    # res = excue.delete_lingshou_user(retail_userid='mera0hW6b6pdm7kCntwTK')
    # print(res)

    """ ****删除店铺维度的数据--delete_lingshou_shop_data"""
    # excue.delete_lingshou_shop_data(external_shop_id='@112834142', retail_shop_id='@64dd89a15559e')

    # ###################### 解绑会员上的用户 ##########################
    # 会员id：472840800674680833
    # 抖店订单 5040769236360353387 -1@#v4yq65O+I7LyqeZ8vIn1+Ze9Oeu0TFVQ+q18aHbjC+cv3F77EeUstWZIQcno++YfdzWamgPDzA==
    # 有赞-E20230509111252059806179 账号：k3pJaQ2G1025769697422868480
    """
    测试数据：龙雨-有赞：1@#v4yq65O+I7LyqeZ8vIn1+Ze9Oeu0TFVQ+q18aHbjC+cv3F77EeUstWZIQcno++YfdzWamgPDzA==
    会员13166210872-客易达：订单-202305121336515520902277992449
    """
    dd_acount = "1@#v4yq65O+I7LyqeZ8vIn1+Ze9Oeu0TFVQ+q18aHbjC+cv3F77EeUstWZIQcno++YfdzWamgPDzA=="  # 抖店账号
    ddsea = '1@#KXjeB9V/2OlWvZ5mvHOfxSWTt03AUTCRwoZv2z2ObMVdSmYgL9OYDfQPf9+jdOULJvOs'  # 抖店
    kyd_acount = "OKIDEj9Z9UjyU3dyAWd7iNto49Q1U7mn"  # 客易达账号
    youzan_acount = "kLeEvABE1144742564428046336"  # 有赞账号
    youzan2_acount = 'Ragnc6he646331639273639936'
    tb_acount = 'AAH59TdrAOHupynQxEEtvIXq'  # 淘宝
    video_account = 'olycp5Ntybjon5-cijrYhR4zKZbU'  # 视频号小店
    self_acount = 'user2183'  # 自营店铺
    ks_acount = 'f181cab22dec9dd214bf57240b007c79'  # 快手小店
    # excue.del_bind_member_data(external_user_id='AAHZ9TdrAOHupynQxEEPzRzA', member_no="47284080067468083311", is_del_redis=True)

    # ##########################删除赠送积分的缓存和快照数据 ############################
    """说明：员工绑定订单后，若没有赠送积分和成长值，需要执行此操作，删除订单赠送成长值快照"""
    # excue.del_member_redis_data(external_user_id='1@#v4yq65O+I7LyqeZ8vIn1+Ze9Oeu0TFVQ+q18aHbjC+cv3F77EeUstWZIQcno++YfdzWamgPDzA==')

    # demo -yield 测试验证
    excue.delete_demo_data(external_shop_id='S12', retail_shop_id="M12")
