# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : xxxx

from shop_manage import *

def add_products():
    """新增商品-客易达商城"""
    res = keyia_login("13166210872", "duan2324")
    if res['code'] != 0:
        raise "登录接口报错"
    else:
        token = res['data']['token']

    i = 0
    while i < 1:
        goodsname = "{0}{1}".format("批量+第{0}个商品".format(i), str(time.time())[-4:])
        skustock = str(time.time())[-1:]
        skuprice = str(time.time())[-3:]
        result = add_product(token, goodsname, skustock, skuprice)
        if result["code"] != 0:
            print("新增商品失败code码-：", str(result["code"])+str(result["msg"]))
        else:
            i = i + 1
            print("新增商品成功，第{0}个:\n"
                  "商品名称：{1}；\n"
                  "价格{2}".format(i, goodsname, skuprice))


if __name__ == "__main__":
    # pass
    add_products()
