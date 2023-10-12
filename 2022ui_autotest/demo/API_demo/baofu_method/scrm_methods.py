# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月19日 9:34
# ---
from demo.API_demo.commons.mysql_ops import query_mysql

DBs = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
       "port": 3306, "data": "zw_shop"}
SCRM_lingshou = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com",
                 "user": "scrm", "password": "scrm@135qwe", "port": 3306, "data": "lingshou"}
SCRM_scrm = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "scrm", "password": "scrm@135qwe",
                   "port": 3306, "data": "scrm"}

class Scrm_Lingshou(object):
    """零售电商-删除用户、订单、商品数据"""

    # 数据库：
    def query_sql(self, DB, SQL):
        """数据库执行sql：update、
        delete from、
        select 、
        insert into"""
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def delete_lingshou_product(self, goodsid):
        """ s删除电商2.0-指定商品"""
        product_sqls = []
        # 1、商品线路表
        sql_product1 = "delete from zw_retail_external_goods_rela where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product1)
        # 2、商品表-zw_retail_goods
        sql_product2 = "delete from zw_retail_goods where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product2)
        # 3、商品-类目表-zw_retail_goods_category_rela
        sql_product3 = "delete from zw_retail_goods_category_rela where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product3)
        # 4、商品索引表-zw_retail_goods_index
        sql_product4 = "delete from zw_retail_goods_index where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product4)
        # 5、商品湖表-zw_retail_goods_lake
        sql_product5 = "delete from zw_retail_goods_lake where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product5)
        # 6、商品sku表-zw_retail_goods_sku_rela
        sql_product6 = "delete from zw_retail_goods_sku_rela where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product6)
        # 7、商品shop表-zw_retail_shop_goods_rela
        sql_product7 = "delete from zw_retail_shop_goods_rela where external_goods_id='" + goodsid + "'"
        product_sqls.append(sql_product7)
        # # 8、商品shop表-zw_retail_shop_goods_rela
        # sql_product8 = "delete from zw_retail_shop_goods_rela where external_goods_id='" + goodsid + "'"
        # sqls.append(sql_product8)
        return product_sqls

    def delete_lingshou_order(self, orderid):
        """
        s删除指定的订单数据
        :return:
        """
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
        # 20、zw_retail_order_consignee_address_rela-订单关联的地址
        sql20 = "delete from zw_retail_order_consignee_address_rela where external_order_id='" + orderid + "'"
        sqls.append(sql20)
        # 21、 删除订单相关的行为--zw_retail_user_behaviour
        sql21 = "delete from zw_retail_user_behaviour where external_order_id='" + orderid + "'"
        sqls.append(sql21)

        return sqls

    def delete_lingshou_user(self, retail_userid, chanel=2):
        """
        s删除零售电商-用户相关的数据
        chanel：2-删除订单、非2：不删除
        :return:sqls
        """
        sqls = []
        # 13、用户行为表-zw_retail_user_behaviour
        sql13 = "delete from zw_retail_user_behaviour where retail_user_id='" + retail_userid + "'"
        sqls.append(sql13)
        # # 14、订单关联商品表-zw_retail_user_behaviour_goods
        # sql14 = "delete from zw_retail_user_behaviour_goods where external_order_id='" + orderid + "'"
        # sqls.append(sql14)

        # 15、零售用户外部用户关系表-zw_retail_external_user_rela
        sql15 = "delete from zw_retail_external_user_rela where retail_user_id='" + retail_userid + "'"
        sqls.append(sql15)
        # done 删除查询第三方用户id-sql
        # select_user_sql = ("select external_user_id from zw_retail_external_user_rela
        # where retail_user_id='" + retail_userid + "'")
        # result = self.query_sql(DB=SCRM_lingshou, SQL=select_user_sql)
        # if result['data']:
        #     print('查询外部userid执行结果:', ['返回结果：', result['data'][0][0], select_user_sql])
        #     external_user_id = result['data'][0][0]
        # else:
        #     external_user_id = ''

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
        if chanel == 2:
            # 删除有赞用户-零售电商-有赞用户账号表zw_retail_youzan_account[有赞用户与线路的关系]
            sql19 = ("delete from zw_retail_youzan_account where external_user_id in ("
                     + "select external_user_id from zw_retail_external_user_rela where retail_user_id='"
                     + retail_userid + "')")
            sqls.append(sql19)
            # 20\零售电商2.0-外部用户与线路标识表-zw_retail_external_account_logo
            sql20 = ("delete from zw_retail_external_account_logo where external_user_id in ("
                     + "select external_user_id from zw_retail_external_user_rela where retail_user_id='"
                     + retail_userid + "')")
            sqls.append(sql20)
            # 删除有赞用户的销售统计数据
            sql21 = "delete from zw_dim_retail_user_stat_daily where retail_user_id='" + retail_userid + "'"
            sqls.append(sql21)

        return sqls

    def delete_lingshou_product_shop(self, external_shop_id, retail_shop_id):
        """ shop删除电商2.0-指定店铺的商品
        @:external_shop_id --外部店铺id
        @:retail_shop_id---零售店铺id

        """
        product_sqls = []
        # 1、商品线路表
        sql_product1 = "delete from zw_retail_external_goods_rela where external_shop_id='" + external_shop_id + "'"
        product_sqls.append(sql_product1)

        # 3、商品-类目表-zw_retail_goods_category_rela
        sql_product3 = ("delete from zw_retail_goods_category_rela where external_goods_id in ("
                        + "select external_goods_id from zw_retail_goods where external_shop_id='"
                        + external_shop_id + "')")
        product_sqls.append(sql_product3)
        # 4、商品索引表-zw_retail_goods_index
        sql_product4 = "delete from zw_retail_goods_index where retail_shop_id='" + retail_shop_id + "'"
        product_sqls.append(sql_product4)
        # 5、商品湖表-zw_retail_goods_lake
        sql_product5 = "delete from zw_retail_goods_lake where external_shop_id='" + external_shop_id + "'"
        product_sqls.append(sql_product5)
        # 6、商品sku表-zw_retail_goods_sku_rela
        sql_product6 = ("delete from zw_retail_goods_sku_rela where external_goods_id in ("
                        + "select external_goods_id from zw_retail_goods where external_shop_id='"
                        + external_shop_id + "')")
        product_sqls.append(sql_product6)
        # 7、商品shop表-zw_retail_shop_goods_rela
        sql_product7 = "delete from zw_retail_shop_goods_rela where retail_shop_id='" + retail_shop_id + "'"
        product_sqls.append(sql_product7)
        # 2、商品表-zw_retail_goods--最后删除商品表的数据
        sql_product2 = "delete from zw_retail_goods where external_shop_id='" + external_shop_id + "'"
        product_sqls.append(sql_product2)
        return product_sqls

    def delete_lingshou_order_shop(self, external_shop_id, retail_shop_id):
        """
        shop删除指定商家的订单数据
        :return:
        """
        sqls = []
        # 1、删除:待解密订单表
        sql1 = "delete from zw_retail_order_decode_todo where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql1)

        # 3、零售用户外部订单关系表-zw_retail_external_order_rela
        sql3 = ("delete from zw_retail_external_order_rela where external_order_id in ("
                + "select external_order_id from zw_retail_order_index where retail_shop_id='"
                + retail_shop_id + "')")
        sqls.append(sql3)
        # 4、零售订单表-zw_retail_order
        sql4 = "delete from zw_retail_order where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql4)
        # 5、零售用户外部订单关系表-zw_retail_external_shop_order_rela
        sql5 = "delete from zw_retail_external_shop_order_rela where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql5)
        # 6、零售外部用户订单关系表-zw_retail_external_user_order_rela
        sql6 = "delete from zw_retail_external_user_order_rela where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql6)
        # 7、零售外部订单客户关系表-zw_retail_order_cust_rela
        sql7 = ("delete from zw_retail_order_cust_rela where external_order_id in ("
                + "select external_order_id from zw_retail_order_index where retail_shop_id='"
                + retail_shop_id + "')")
        sqls.append(sql7)
        # 8、订单解密表-zw_retail_order_decode
        sql8 = ("delete from zw_retail_order_decode where external_order_id in ("
                + "select external_order_id from zw_retail_order_index where retail_shop_id='"
                + retail_shop_id + "')")
        sqls.append(sql8)
        # 8-1、订单解密表-记录表-zw_retail_order_decode_records
        sql81 = "delete from zw_retail_order_decode_records where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql81)
        # 8-2、订单-待解密表-zw_retail_order_decode_todo
        sql82 = "delete from zw_retail_order_decode_todo where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql82)

        # 9、零售外部订单商品表-zw_retail_order_goods
        sql9 = "delete from zw_retail_order_goods where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql9)
        # 9-1、零售外部订单商品sku表-zw_retail_order_goods_sku
        sql91 = "delete from zw_retail_order_goods_sku where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql91)
        # 10、订单湖-zw_retail_order_lake
        sql10 = "delete from zw_retail_order_lake where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql10)
        # 11、售后表-zw_retail_order_refund
        sql11 = ("delete from zw_retail_order_refund where external_order_id in ("
                 + "select external_order_id from zw_retail_order_index where retail_shop_id='"
                 + retail_shop_id + "')")
        sqls.append(sql11)
        # 12、子订单表-zw_retail_sub_order
        sql12 = "delete from zw_retail_sub_order where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql12)
        # 20、zw_retail_order_consignee_address_rela-订单关联的地址
        sql20 = "delete from zw_retail_order_consignee_address_rela where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql20)
        # 21、 删除订单相关的行为--zw_retail_user_behaviour
        sql21 = "delete from zw_retail_user_behaviour where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql21)
        # 2、零售订单索引表--需要最后删除，其他sql需要先查到数据
        sql2 = "delete from zw_retail_order_index where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql2)
        return sqls

    def delete_lingshou_user_shop(self, external_shop_id, retail_shop_id, chanel=2):
        """
        shop删除零售电商-用户相关的数据
        chanel：2-删除订单、非2：不删除
        :return:sqls
        """
        sqls = []

        # 15、零售用户外部用户关系表-zw_retail_external_user_rela
        sql15 = "delete from zw_retail_external_user_rela where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql15)
        # select_user_sql = "select external_user_id from zw_retail_external_user_rela where
        # retail_user_id='" + retail_userid + "'"
        # result = self.query_sql(DB=SCRM_lingshou, SQL=select_user_sql)
        # if result['data']:
        #     print('查询外部userid执行结果:', ['返回结果：', result['data'][0][0], select_user_sql])
        #     external_user_id = result['data'][0][0]
        # else:
        #     external_user_id = ''
        # 16、店铺用户表-zw_retail_shop_user
        sql16 = "delete from zw_retail_shop_user where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql16)

        # 17、零售用户表-zw_retail_user
        sql17 = ("delete from zw_retail_user where retail_user_id in ("
                 + "select retail_user_id from zw_retail_shop_user_index where retail_shop_id='"
                 + retail_shop_id + "')")
        sqls.append(sql17)
        # 18、店铺用户索引表-zw_retail_shop_user_index
        sql18 = "delete from zw_retail_shop_user_index where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql18)

        sql19 = "delete from zw_retail_youzan_account where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql19)
        # 20-zw_retail_external_account_logo零售电商2.0-外部用户与线路标识表
        sql20 = "delete from zw_retail_external_account_logo where external_shop_id='" + external_shop_id + "'"
        sqls.append(sql20)

        # 21、删除客户-收件人相关的数据zw_retail_consignee_index
        sql21 = "delete from zw_retail_consignee_index where retail_shop_id='" + retail_shop_id + "'"
        sqls.append(sql21)
        return sqls

    def unbinding_retail_data(self, external_user_id, *args):
        """解绑会员身上的渠道用户订单
        @:param external_user_id--渠道用户id-通过绑定关联到会员身上
        @:param member_no 会员编号
        :return: 解绑结果
        """
        sqls = []
        # 1、店铺会员索引表-zw_kyd_member_store_index（会员与渠道用户id的关联）
        sql_1 = "delete from ucenter.zw_kyd_member_store_index where external_user_id='" + external_user_id + "'"
        sqls.append(sql_1)
        # 2、zw_kyd_member_shop_info_v2-客易达-店铺会员信息表（会员与渠道用户id的关联）
        sql_2 = "delete from ucenter.zw_kyd_member_shop_info_v2 where external_user_id='" + external_user_id + "'"
        sqls.append(sql_2)
        # 3、zw_kyd_member_shop_v2-客易达-店铺会员表（会员与渠道用户id的关联）
        sql_3 = "delete from ucenter.zw_kyd_member_shop_v2 where external_user_id='" + external_user_id + "'"
        sqls.append(sql_3)
        # 4、zw_kyd_member_order_stat_details--会员订单统计明细表 # TODO 暂时不需要执行该表
        # TODO 需要删除订单快照表-此表记录该笔订单是否赠送积分和成长值--zw_retail_order_rule_snapshot 字段：channel_order_sn
        # sql_4 = ("delete from scrm.zw_retail_order_rule_snapshot where channel_order_sn in ("
        #         + "select external_order_id from zw_retail_order where external_user_id='"
        #         + external_user_id + "')")
        # sqls.append(sql_4)

        return sqls



    def get_external_order_ids(self, external_user_id):
        """
        获取该渠道用户的所有订单
        :param external_user_id: 渠道用户id
        :return:
        """
        get_user_order = ("select external_order_id from zw_retail_order where external_user_id='"
                          + external_user_id + "'")
        return get_user_order

    def delete_demo(self, external_shop_id, retail_shop_id):
        """ demo:删使用yield生成list，进行遍历删除
        @:external_shop_id --外部店铺id
        @:retail_shop_id---零售店铺id
        """
        # 1、商品线路表
        sql_product1 = "delete from zw_retail_external_goods_rela where external_shop_id='" + external_shop_id + "'"
        yield sql_product1

        # 3、商品-类目表-zw_retail_goods_category_rela
        sql_product3 = ("delete from zw_retail_goods_category_rela where external_goods_id in ("
                        + "select external_goods_id from zw_retail_goods where external_shop_id='"
                        + external_shop_id + "')")
        yield sql_product3
        # 4、商品索引表-zw_retail_goods_index
        sql_product4 = "delete from zw_retail_goods_index where retail_shop_id='" + retail_shop_id + "'"
        yield sql_product4
        # 5、商品湖表-zw_retail_goods_lake
        sql_product5 = "delete from zw_retail_goods_lake where external_shop_id='" + external_shop_id + "'"
        yield sql_product5