# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : 新增商品
import json
import time
import requests


def add_product(token, goodsname, skustock, skuprice, shopid=19):
	"""新增商品"""
	url_add_product = "http://api-test.shop.keyid.cn/tenant/goods/save"
	token = token
	header = {
			"Host":	"api-test.shop.keyid.cn",
			"Accept": "application/json, text/plain, */*",
			"Content-Type": "application/json",
			"ZW-PLATFORM-TOKEN": token,
			"Accept-Language": "zh-CN,zh;q=0.9",
			"ZW-TENANT-ID": str(shopid),
			"Connection": "keep-alive"
	}
	for n in range(0, 3):
		if n != 1:
			g = 1
		else:
			g = n+1

	parm = {
		"shopId": 16961,
		"materialSrc": [{
			"materialSrc": "https://img-shop-dev.keyid.cn/shop-api/images/20220808/UraroXjYHA5SGp4k.jpg",
			"sort": 1,
			"isCover": n
		},
			{
				"materialSrc": "https://img-shop-dev.keyid.cn/shop-api/images/20220808/6nlNFpwiUBgLhdyz.jpg",
				"sort": 2,
				"isCover": g
			}
		],
		"goodsName": goodsname,
		"goodsCategoryId": [{
			"categoryParentId": 202,
			"categorySonId": 363
		}, {
			"categoryParentId": 112,
			"categorySonId": 182
		}],
		"enable": "1",
		"transportId": 65,
		"goodsDescription": "",
		"onSale": 1,
		"skuInfo": [
			[{
				"attributeId": 3,
				"attributeValue": "批量商品红色",
				"thumb": "https://img-shop-dev.keyid.cn/shop-api/images/20220808/6nlNFpwiUBgLhdyz.jpg",
				"skuSort": 1
			}]
		],
		"skuStock": [skustock],
		"skuPrice": [skuprice]
	}

	print(header)
	post_json = json.dumps(parm).encode("utf-8")
	# 序列化和反序列化
	#json.loads(json.dumps(post_json.json()).replace(r'.', '/'))
	res = requests.post(url=url_add_product, headers=header, data=post_json, verify=True)

	print(res.json())
	print("res.text", res.text)
	print("res.content:", res.content)
	print("res.cookies:", res.cookies)
	print("res.headers:", res.headers)
	print("res.reason:", res.reason)
	print("res.encoding:", res.encoding)
	return res.json()


def keyia_login(mobile, password, *args):
	"商家后台登录"
	url = "http://api-test.shop.keyid.cn/platform/auth/login"
	header = {
		"Host": "api-test.shop.keyid.cn",
		"Accept": "application/json, text/plain, */*",
		"Content-Type": "application/json",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Connection": "keep-alive"
	}

	parms = {
		"mobile": mobile,
		"password": password
	}
	post_json = json.dumps(parms).encode("utf-8")
	res = requests.post(url=url, json=parms, headers=header, verify=True)

	print(res.json())
	return res.json()



#======================新增商品====================

if __name__ == "__main__":

	i = 0
	while i < 1:
		goodsName = "{0}{1}".format("第{0}个商品".format(i), str(time.time())[-4:])
		result = add_product(goodsName)
		if result["code"] != 0:
			print("新增商品失败code码：", result["code"])
			break
		else:
			i = i + 1
			print("新增商品成功，第{0}个".format(i))

	# res = keyia_login("13166210872", "duan2324")
	# if res['code'] != 0:
	# 	raise "登录接口报错"
	# else:
	# 	token = res['data']['token']

