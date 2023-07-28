# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023��4����26�� 9:36
# ---
from redis import Redis
import time
from commons.mysql_ops import *

DBs = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
       "port": 3306, "data": "zw_shop"}


class KydRedis():
    """�������״�redis"""
    # ����redis������ password:vhEA1jf4
    redis_connect = Redis(host='47.103.9.199', port=6379, db=8, password='vhEA1jf4', decode_responses=True)

    def get_Skey(self, key=None, type=None):
        '''��ȡָ��key��value������ִ�в���'''
        time.sleep(1)
        return self.redis_connect.get(key)

    def delete_redis_key(self, key):
        """redisɾ����Ӧ��key
        key='points_experience_rule:56-56'--���Ի�������������-��Ӧscrm
        """
        result = self.get_Skey(key)
        if result != None:
            '''ִ��delete'''
            re = self.redis_connect.delete(key)
            return {'code': 0, 'msg': 'ɾ���ɹ�' + key, 'data': [re]}
        else:
            return {'code': 1, 'msg': 'redis��û���ҵ�ָ��key', 'data': []}

    def get_phone_sms_code(self, phone):
        """
        :param phone: �ֻ��� api_platform_sms_login_code_13166210872
        :return:
        """
        key = 'api_platform_sms_login_code_' + str(phone)
        return self.redis_connect.get(key)


class ConvenientScript(object):
    """��ݽű�����ɾ���˻���"""
    # �̳�
    DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
          "port": 3306, "data": "zw_shop"}
    # �⻧���˻���ϵ�� zw_bht_account_bind_record
    # ����֧��������zw_payment

    # SCRM-DB
    SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
               "port": 3306, "data": "lingshou"}

    # ���ݿ⣺
    def query_sql(self, DB, SQL):
        """���ݿ�ִ��sql��update��
        delete from��
        select ��
        insert into"""
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def scrm_sql(self, DB, SQL):
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def delete_baofoo_account_pay(self, login_no, isd='1'):
        """˵����ɾ��С�����°󶨵ı���֧��"""
        sqls = []
        # #  1\zw_bht_account_bind_record--������ҵ���˸����˻��󶨹�ϵ��
        # SELECT * from  zw_bht_account_bind_record WHERE login_no = '4II9Zah0GeD1sWJhdKOB';
        record_sql = "update zw_bht_account_bind_record set is_deleted =" + isd + " WHERE login_no ='" \
                     + login_no + "'"
        sqls.append(record_sql)
        # #  2|2\ '�û�ʵ����֤��'--zw_bht_pay_user_autonym
        user_autonym_sql = "update zw_bht_pay_user_autonym set is_deleted =" + isd + " WHERE login_no ='" \
                           + login_no + "'"
        sqls.append(user_autonym_sql)
        # 3���Թ���ҵ������zw_bht_corporation_account_open--ɾ����Ӧ�������
        zw_bht_corporation_account_open_sql = "update zw_bht_corporation_account_open set is_delete =" + isd + " " \
                                                                                                               "WHERE login_no ='" + login_no + "'"
        sqls.append(zw_bht_corporation_account_open_sql)
        # 4�� ����ͨ�˻��󶨱�-zw_bht_account_bind_record
        zw_bht_account_bind_record_sql = "update zw_bht_account_bind_record set is_deleted =" + isd + " WHERE " \
                                                                                                      "bind_login_no ='" + login_no + "'"
        sqls.append(zw_bht_account_bind_record_sql)
        # 5\���� zw_bht_user_bank_account--�û������п���
        # SELECT * from zw_bht_user_bank_account where is_delete =2 and  login_no='dnxjwqe90m2DpXyCMWVd';
        # seleCT * from zw_user_bank_account where is_delete =2 and login_no='dnxjwqe90m2DpXyCMWVd';
        zw_bht_user_bank_account_sql = "update zw_bht_user_bank_account set is_delete =" + isd + " WHERE login_no ='" \
                                       + login_no + "'"
        zw_user_bank_account_sql = "update zw_user_bank_account set is_delete =" + isd + " WHERE login_no ='" \
                                   + login_no + "'"
        sqls.append(zw_bht_user_bank_account_sql)
        sqls.append(zw_user_bank_account_sql)
        # 6\����ʵ����֤��
        zw_autonym_sql1 = "update zw_autonym set is_deleted =" + isd + " WHERE login_no ='" + login_no + "'"
        user_autonym_sql2 = "update zw_bht_pay_user_autonym set is_deleted =" + isd + " WHERE login_no ='" + login_no + "'"
        sqls.append(zw_autonym_sql1)
        sqls.append(user_autonym_sql2)
        # 7\ �û������п���select * from `zw_user_bank_account`where login_no = 'dnxjwqe90m2DpXyCMWVd' and  is_delete =2;
        sql = "update zw_user_bank_account set is_delete =" + isd + " WHERE login_no ='" + login_no + "'"
        sqls.append(sql)
        print('��Ҫִ�е�sql', sqls)
        DBshop = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
                  "port": 3306, "data": "zw_shop"}
        for sql in sqls:
            result = self.query_sql(DB=DBshop, SQL=sql)
            print('ִ�н����', [result, sql])

        #  https://sp.baofoo.com/support-admin/mer/follow/del/logino?logino=FMmOR7VB0RCrYe66at71&usertype=PERSON

    def update_lingshou_user_order(self, r_userid, external_order_id, external_user_id, line='1c8aa0614e8f195b'):
        '''���۵��̣��޸��û��Ͷ�����������·�û�id'''
        sqls = []
        # ���۵���-�����û��ⲿ�û���ϵ��-zw_retail_external_user_rela--������·id
        # @parm::line-��·id(b748d239e773f12d-��·3)
        # @parm:r_userid-�����û�id
        user_sql = "update zw_retail_external_user_rela set third_app_id ='" + line + "' WHERE retail_user_id ='" \
                   + r_userid + "'"
        sqls.append(user_sql)
        # �û�+����+��·-zw_retail_external_user_order_rela::
        # @parm:e_userid-�ⲿ�û�id
        user_order_sql = "update zw_retail_external_user_order_rela set third_app_id ='" + line + "' WHERE external_order_id ='" \
                         + external_order_id + "'" + "and external_user_id='" + external_user_id + "'"
        sqls.append(user_order_sql)
        # ������+��·-zw_retail_order_lake
        order_lake_sql = "update zw_retail_order_lake set third_app_id ='" + line + "' WHERE external_order_id ='" \
                         + external_order_id + "'" + "and external_user_id='" + external_user_id + "'"
        sqls.append(order_lake_sql)
        # ������־+��·-zw_retail_order_lake_log
        order_lakelog_sql = "update zw_retail_order_lake_log set third_app_id ='" + line + "' WHERE external_order_id ='" \
                            + external_order_id + "'" + "and external_user_id='" + external_user_id + "'"
        sqls.append(order_lakelog_sql)
        SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
        print('��ӡscrmsql', sqls)
        for sql in sqls:
            result = self.query_sql(DB=SCRM_DB, SQL=sql)
            print('ִ�н����', [result, sql])

    def update_all_lingshou_user_order(self, old_line, line='1c8aa0614e8f195b'):
        '''���۵��̣��޸��û��Ͷ�����������·�û�id'''
        sqls = []
        # ���۵���-�����û��ⲿ�û���ϵ��-zw_retail_external_user_rela--������·id
        # @parm::line-��·id(b748d239e773f12d-��·3)
        # @parm:r_userid-�����û�id
        user_sql = "update zw_retail_external_user_rela set third_app_id ='" + line + "' WHERE third_app_id !='" \
                   + old_line + "'"
        sqls.append(user_sql)
        # �û�+����+��·-zw_retail_external_user_order_rela::
        # @parm:e_userid-�ⲿ�û�id
        user_order_sql = "update zw_retail_external_user_order_rela set third_app_id ='" + line + "' WHERE third_app_id !='" \
                         + old_line + "'"
        sqls.append(user_order_sql)
        # ������+��·-zw_retail_order_lake
        order_lake_sql = "update zw_retail_order_lake set third_app_id ='" + line + "' WHERE third_app_id !='" \
                         + old_line + "'"
        sqls.append(order_lake_sql)
        # ������־+��·-zw_retail_order_lake_log
        # order_lakelog_sql = "update zw_retail_order_lake_log set third_app_id ='"+line+"' WHERE external_order_id ='" \
        #                      + external_order_id + "'" + "and external_user_id='" + external_user_id + "'"
        # sqls.append(order_lakelog_sql)

        SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
        print('��ӡscrmsql', sqls)
        for sql in sqls:
            result = self.query_sql(DB=SCRM_DB, SQL=sql)
            print('ִ�н����', [result, sql])

    def delete_YZ_user_orderinfo(self, orderid, retail_userid, goodsid, del_product=False):
        '''ɾ��ĳһ���������û�����'''
        sqls = []
        # 1��ɾ�����ܶ���
        sql1 = "delete from zw_retail_order_decode_todo where external_order_id='" + orderid + "'"
        sqls.append(sql1)
        # 2�����۶���������
        sql2 = "delete from zw_retail_order_index where external_order_id='" + orderid + "'"
        sqls.append(sql2)
        # 3�������û��ⲿ������ϵ��-zw_retail_external_order_rela
        sql3 = "delete from zw_retail_external_order_rela where external_order_id='" + orderid + "'"
        sqls.append(sql3)
        # 4�����۶�����-zw_retail_order
        sql4 = "delete from zw_retail_order where external_order_id='" + orderid + "'"
        sqls.append(sql4)
        # 5�������û��ⲿ������ϵ��-zw_retail_external_shop_order_rela
        sql5 = "delete from zw_retail_external_shop_order_rela where external_order_id='" + orderid + "'"
        sqls.append(sql5)
        # 6�������ⲿ�û�������ϵ��-zw_retail_external_user_order_rela
        sql6 = "delete from zw_retail_external_user_order_rela where external_order_id='" + orderid + "'"
        sqls.append(sql6)
        # 7�������ⲿ�����ͻ���ϵ��-zw_retail_order_cust_rela
        sql7 = "delete from zw_retail_order_cust_rela where external_order_id='" + orderid + "'"
        sqls.append(sql7)
        # 8���������ܱ�-zw_retail_order_decode
        sql8 = "delete from zw_retail_order_decode where external_order_id='" + orderid + "'"
        sqls.append(sql8)

        # 9�������ⲿ������Ʒ��-zw_retail_order_goods
        sql9 = "delete from zw_retail_order_goods where external_order_id='" + orderid + "'"
        sqls.append(sql9)
        # 10��������-zw_retail_order_lake
        sql10 = "delete from zw_retail_order_lake where external_order_id='" + orderid + "'"
        sqls.append(sql10)
        # 11���ۺ��-zw_retail_order_refund
        sql11 = "delete from zw_retail_order_refund where external_order_id='" + orderid + "'"
        sqls.append(sql11)
        # 12���Ӷ�����-zw_retail_sub_order
        sql12 = "delete from zw_retail_sub_order where external_order_id='" + orderid + "'"
        sqls.append(sql12)
        # 13���û���Ϊ��-zw_retail_user_behaviour
        sql13 = "delete from zw_retail_user_behaviour where external_order_id='" + orderid + "'" + "or retail_user_id='" \
                + retail_userid + "'"
        sqls.append(sql13)
        # # 14������������Ʒ��-zw_retail_user_behaviour_goods
        # sql14 = "delete from zw_retail_user_behaviour_goods where external_order_id='" + orderid + "'"
        # sqls.append(sql14)

        # 15�������û��ⲿ�û���ϵ��-zw_retail_external_user_rela
        sql15 = "delete from zw_retail_external_user_rela where retail_user_id='" + retail_userid + "'"
        sqls.append(sql15)
        # 16�������û���-zw_retail_shop_user
        sql16 = "delete from zw_retail_shop_user where retail_user_id='" + retail_userid + "'"
        sqls.append(sql16)
        # 17�������û�������-zw_retail_shop_user_index
        sql17 = "delete from zw_retail_shop_user_index where retail_user_id='" + retail_userid + "'"
        sqls.append(sql17)
        # 18�������û���-zw_retail_user
        sql18 = "delete from zw_retail_user where retail_user_id='" + retail_userid + "'"
        sqls.append(sql18)

        if del_product == True:
            """ɾ����Ʒ����"""
            # 1����Ʒ��·��
            sql_product1 = "delete from zw_retail_external_goods_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product1)
            # 2����Ʒ��-zw_retail_goods
            sql_product2 = "delete from zw_retail_goods where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product2)
            # 3����Ʒ-��Ŀ��-zw_retail_goods_category_rela
            sql_product3 = "delete from zw_retail_goods_category_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product3)
            # 4����Ʒ������-zw_retail_goods_index
            sql_product4 = "delete from zw_retail_goods_index where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product4)
            # 5����Ʒ����-zw_retail_goods_lake
            sql_product5 = "delete from zw_retail_goods_lake where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product5)
            # 6����Ʒsku��-zw_retail_goods_sku_rela
            sql_product6 = "delete from zw_retail_goods_sku_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product6)
            # 7����Ʒshop��-zw_retail_shop_goods_rela
            sql_product7 = "delete from zw_retail_shop_goods_rela where external_goods_id='" + goodsid + "'"
            sqls.append(sql_product7)
            # # 8����Ʒshop��-zw_retail_shop_goods_rela
            # sql_product8 = "delete from zw_retail_shop_goods_rela where external_goods_id='" + goodsid + "'"
            # sqls.append(sql_product8)




        SCRM_DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "lingshou"}
        print('��ӡscrmsql', sqls)
        n = 0
        for sql in sqls:
            n = n + 1
            result = self.query_sql(DB=SCRM_DB, SQL=sql)
            print('ִ�н����', ['��'+str(n)+'��',result, sql])


if __name__ == '__main__':
    pass
    # reds = KydRedis()
    # # re_value = reds.get_Skey(key='points_experience_rule:56-56')
    # # print('���ص�value:', re_value)
    #
    # # ɾ����Ӧ��key���ڻ�Ա����ϵͳ-����������ͨȫ����ֹ���
    # res = reds.delete_redis_key(key='points_experience_rule:56-56')
    # print(res)

    # ��ȡ�ֻ��ŵ���֤��
    # print(reds.get_phone_sms_code(13166210872))
    # ConvenientScript
    """ɾ�����Ի���-����ͨ�˻���Ϣ"""
    excue = ConvenientScript()
    # login_no ='641525329622059712513'  # ��Ҫɾ���ĸ���login_no
    # excue.delete_baofoo_account_pay(login_no,isd='1')

    '''�����û�����������·id'''
    # ��·1��1c8aa0614e8f195b
    # ��·2��91b5c082a6cf042b
    # ��·3��b748d239e773f12d

    # excue.update_lingshou_user_order(r_userid='Px7rnJLZgn1nTkJmS3GyM', external_order_id='1915204298471438899',
    #                                  external_user_id='AAFt0YHcABD0D2GIOazWc05p', line='1c8aa0614e8f195b')

    """ ������·�û�����·Ϊ����·"""
    # excue.update_all_lingshou_user_order(old_line='b748d239e773f12d', line='1c8aa0614e8f195b')

    """���޶���·--ɾ�����������û�\��Ʒ������"""
    # 6920397821379024382\axXXCkXQJGF4M2apKggjn
    excue.delete_YZ_user_orderinfo(orderid='6920397821379024382', retail_userid='r6L4R5SBFSwyye9RSL8Kt', goodsid='3629814263113221043' , del_product=False)
