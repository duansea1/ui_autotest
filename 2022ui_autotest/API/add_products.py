# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: 段海洋
# @Time: 2022年8月月30日 19:09
# ---

"""查商品数据库、找到匹配商品、调加车商品接口加购功能"""

from commons.mysql_ops import *
import json,requests


database = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
            "port": 3306,"data": "zw_shop"}


# 查询销售中的商品--店铺16961
sql = "SELECT id from zw_goods where is_delete =2 and shop_id =16961 and on_sale=1 limit 200;"

sku_sql = "select goods_id, id from zw_sku where goods_id in (SELECT id from zw_goods where is_delete =2 and " \
          "shop_id =16961 and on_sale=1) and is_delete=2 and sku_stock>0 limit 1000;"


class kyidaShopcart:

    def query_skus(self, DB, SQL):
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def add_product_toUser(self, skuid, goodsid, token=None):
        """ 选择指定用户加车"""
        url = "https://api-test.shop.keyid.cn/miniapp/cart/add"
        header = {
            "ZW-APP-ID": "wx64f7637c4f2393e9",
            "ZW-SHOP-ID": "16961",
            "content-type": "application/json",
            "token": token,
            "sign": "602f6f4b7ccaba93915e22d3c9788fc5"
        }

        parms = {
            "skuId": str(skuid),
            "goodsId": str(goodsid),
            "quantity": 1
        }
        post_json = json.dumps(parms).encode("utf-8")
        res = requests.post(url=url, data=post_json, headers=header, verify=True)
        print(res.json())

    def run_add_products(self):
        """调此方法加车商品
        @:param DB :{"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0", "port": 3306,"data": "zw_shop"}
        @:param sql: "SELECT id from zw_goods where is_delete =2 and shop_id =16961 and on_sale=1 limit 200;"
        @:param skuid: 商品skuid
        @:param goodsid: sku对应的商品id
        @:param token:小程序C端用户登录的token
        """
        goods_result = self.query_skus(DB=database, SQL=sku_sql)
        if goods_result["code"] != 0:
            print("====链接数据库失败=====")
        else:
            good_skus = goods_result['data']
            print(good_skus)
            print("商品id：", good_skus[0][0])
            print("商品id->sku_id：", good_skus[0][1])
            for i in range(len(good_skus)):
                skuid = good_skus[i][1]
                goodsid = good_skus[i][0]
                print("已加车{2}个商品：加车商品{0},skuid:{1}".format(goodsid, skuid, i))
                # print(goodsid)
                token = "1a97f08363b9247c9bc93960d6d7e1d46f308219"
                self.add_product_toUser(skuid=skuid, goodsid=goodsid, token=token)


if __name__ == "__main__":
    cart = kyidaShopcart()
    cart.run_add_products()



