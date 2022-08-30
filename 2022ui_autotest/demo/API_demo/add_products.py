# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: 段海洋
# @Time: 2022年8月月30日 19:09
# ---

from commons.mysql_ops import *
import json,requests


database = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0", "port": 3306,"data": "zw_shop"}


# 查询销售中的商品--店铺16961
sql = "SELECT id from zw_goods where is_delete =2 and shop_id =16961 and on_sale=1 limit 200;"

sku_sql = "select goods_id, id from zw_sku where goods_id in (SELECT id from zw_goods where is_delete =2 and " \
          "shop_id =16961 and on_sale=1) and is_delete=2 and sku_stock>0 limit 1000;"


class kyidaShopcart:

    def query_skus(self, DB, SQL):
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        return result

    def add_product_toUser(self, skuid, goodsid):
        """ 选择指定用户加车"""
        url = "https://api-test.shop.keyid.cn/miniapp/cart/add"
        header = {
            "ZW-APP-ID": "wx64f7637c4f2393e9",
            "ZW-SHOP-ID": "16961",
            "content-type": "application/json",
            "token": "cb7765b36aa9a34dcae75d772f0c46ee322e6578",
            "sign": "27355c77d9ec16cacb821ac3a14625a7"
        }

        parms = {
            "skuId": str(skuid),
            "goodsId": str(goodsid),
            "quantity": 1
        }
        post_json = json.dumps(parms).encode("utf-8")
        res = requests.post(url=url, data=post_json, headers=header, verify=True)
        print(res.json())


if __name__ == "__main__":
    cart = kyidaShopcart()
    goods_result = cart.query_skus(DB=database, SQL=sku_sql)
    if goods_result["code"] != 0:
        print("====链接数据库失败=====")
    else:
        good_skus = goods_result['data']
        print(good_skus)
        print("商品id：", good_skus[0][0])
        print("商品id->sku_id：", good_skus[0][1])
        for i in range(3):
            skuid = good_skus[i][1]
            goodsid = good_skus[i][0]
            print("加车商品{0},skuid:{1}".format(goodsid, skuid))
            # print(goodsid)
            cart.add_product_toUser(skuid=skuid, goodsid=goodsid)
        # n = 0
        # while n < 3:
        #     for i in good_skus:
        #         skuid = i[0][1]
        #         goodsid = i[0][0]
        #         cart.add_product_toUser(skuid=skuid, goodsid=goodsid)
        #     n+=1



