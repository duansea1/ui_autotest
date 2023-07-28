# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : 新增商品
import json
import time
import requests
import random


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


def save_new_products(self, numberbase=2027):
	"""新增商品到指定店铺"""
	url = "https://api.shop.keyid.cn/tenant/goods/save"

	token = 'ca4162a86a0f2421f8764eb9436b4b114881d061'
	img_http = "https://img.shop.keyid.cn/shop-api/images/20230215"
	img1 = img_http + '/1tdYGC9YezxmsQIe.png'
	img2 = img_http + '/f1eeCrACUzOc0rez.png'
	img3 = img_http + '/jPgewWg5n1vfCg0c.png'
	img4 = img_http + '/ea5hBRAudDUwlFuW.png'
	img5 = img_http + "/ea5hBRAudDUwlFuW.png"
	img6 = img_http + "/o8iE9JRR8BXoGtxt.png"
	product_imgs = [img1, img2, img3, img4, img5, img6]
	img = random.choice(product_imgs)
	print('商品的主图片:', img)

	productName = "新商品" + str(numberbase)

	attributeValues = ['SS码', '明星款S', '时尚XL码']
	attributeValue = random.choice(attributeValues)
	skuPrices = [9.89, 9.56, 7.65, 55, 198, 128]
	skuPrice = random.choice(skuPrices)

	header = {
		"ZW-SHOP-ID": "31",
		"ZW-CORP-ID": "11",
		"ZW-TENANT-ID": "11",
		"content-type": "application/json",
		"ZW-PLATFORM-TOKEN": token
	}

	parms = {
		"shopId": 31,
		"specType": 2,
		"materialSrc": [{
			"materialSrc": img,
			"sort": 1,
			"isCover": 1
		}],
		"goodsName": productName,
		"goodsCategoryId": [{
			"categoryParentId": 229,
			"categorySonId": 232
		}],
		"enable": "1",
		"transportId": 29,
		"goodsDescription": "<p><img src=\"" + img + "\"><img src=\"https://img.shop.keyid.cn/shop-api/images/20230215/zbSl6LUMEHaRBQm1.png\"><img src=\"https://img.shop.keyid.cn/shop-api/images/20230215/JSbZQx2QyfTHwi4v.png\"><img src=\"https://img.shop.keyid.cn/shop-api/images/20230215/s2gBRwir1tvmD3vY.png\"><img src=\"https://img.shop.keyid.cn/shop-api/images/20230215/vyWEbFwKPr0CGSh2.png\"><img src=\"https://img.shop.keyid.cn/shop-api/images/20230215/LyIN6rrDBDlczNQI.png\"></p>",
		"onSale": 2,
		"skuInfo": [
			[{
				"attributeId": 0,
				"attributeName": "尺寸",
				"attributeValue": attributeValue,
				"skuSort": 1
			}, {
				"attributeId": 0,
				"attributeName": "尺寸",
				"attributeValue": "2XL",
				"skuSort": 1
			}, {
				"attributeId": 0,
				"attributeName": "尺寸",
				"attributeValue": "S码",
				"skuSort": 1
			}]
		],
		"skuStock": [10, 10, 10],
		"skuPrice": [skuPrice * 100, 1990, 1990],
		"skuImg": [img, img, img]
	}
	post_json = json.dumps(parms).encode("utf-8")
	res = requests.post(url=url, data=post_json, headers=header, verify=False)
	print(res.json())


def save_new_testproducts(self, numberbase=2027):
	"""新增商品到指定店铺"""
	url = "https://api-test.shop.keyid.cn/tenant/goods/save"

	token = '1c596507c8273f58d7bceff768794826a498b073'
	img_http = "https://img-shop-dev.keyid.cn/shop-api/images/20230213"
	# img1 = img_http + '/1tdYGC9YezxmsQIe.png'
	# img2 = img_http + '/f1eeCrACUzOc0rez.png'
	# img3 = img_http + '/jPgewWg5n1vfCg0c.png'
	# img4 = img_http + '/ea5hBRAudDUwlFuW.png'
	# img5 = img_http + "/ea5hBRAudDUwlFuW.png"
	# img6 = img_http + "/o8iE9JRR8BXoGtxt.png"
	# product_imgs = [img1, img2, img3, img4, img5, img6]
	# img = random.choice(product_imgs)
	img = "https://img-shop-dev.keyid.cn/shop-api/images/20230213/7RXnjPi45vOPY8Ev.jpg"
	print('商品的主图片:', img)

	productName = "新商品" + str(numberbase)

	attributeValues = ['SS码', '明星款S', '时尚XL码']
	attributeValue = random.choice(attributeValues)
	skuPrices = [9.89, 9.56, 7.65, 55, 198, 128]
	skuPrice = random.choice(skuPrices)

	header = {
		"ZW-SHOP-ID": "17063",
		"ZW-CORP-ID": "56",
		"ZW-TENANT-ID": "56",
		"content-type": "application/json",
		"ZW-PLATFORM-TOKEN": token
	}

	parms = {
		"shopId": 31,
		"specType": 2,
		"materialSrc": [{
			"materialSrc": img,
			"sort": 1,
			"isCover": 1
		}],
		"goodsName": productName,
		"goodsCategoryId": [{
			"categoryParentId": 553,
			"categorySonId": 554
		}],
		"enable": "1",
		"transportId": 185,
		"goodsDescription": "无说明",
		"onSale": 2,
		"skuInfo": [
			[{
				"attributeId": 0,
				"attributeName": "尺寸",
				"attributeValue": attributeValue,
				"skuSort": 1
			}, {
				"attributeId": 0,
				"attributeName": "尺寸",
				"attributeValue": "2XL",
				"skuSort": 1
			}, {
				"attributeId": 0,
				"attributeName": "尺寸",
				"attributeValue": "S码",
				"skuSort": 1
			}]
		],
		"skuStock": [10, 10, 10],
		"skuPrice": [skuPrice * 100, 1990, 1990],
		"skuImg": [img, img, img]
	}
	post_json = json.dumps(parms).encode("utf-8")
	res = requests.post(url=url, data=post_json, headers=header, verify=False)
	print(res.json())


def addProduct_of_youwantNum(self):
	"""新增商品"""
	n = 1
	numberbase = 1023
	while n < 3:  # 新增3个商品
		self.save_new_products(numberbase=numberbase)
		n = n + 1
		numberbase += 1


def add_catebage(self, num, index):
	"""新增分类"""
	url = "https://api-test.shop.keyid.cn/tenant/category/save"
	token = "1c596507c8273f58d7bceff768794826a498b073"
	header = {
		"ZW-SHOP-ID": "16961",
		"content-type": "application/json",
		"ZW-PLATFORM-TOKEN": token,
		"ZW-CORP-ID": "19",
		"ZW-TENANT-ID": "19"
	}

	parms = {
		"shopId": 16961,
		"categoryName": str(num) + "一级分类",
		"level": 1,
		"parentId": "",
		"cateSort": index,
		"isDefault": 2
	}
	post_json = json.dumps(parms).encode("utf-8")
	res = requests.post(url=url, data=post_json, headers=header, verify=False)
	print(res.json())



#======================新增商品====================

if __name__ == "__main__":

	# i = 0
	# while i < 1:
	# 	goodsName = "{0}{1}".format("第{0}个商品".format(i), str(time.time())[-4:])
	# 	result = add_product(goodsName)
	# 	if result["code"] != 0:
	# 		print("新增商品失败code码：", result["code"])
	# 		break
	# 	else:
	# 		i = i + 1
	# 		print("新增商品成功，第{0}个".format(i))

	# res = keyia_login("13166210872", "duan2324")
	# if res['code'] != 0:
	# 	raise "登录接口报错"
	# else:
	# 	token = res['data']['token']

	res = keyia_login("13166210872", "duan2324")
	if res['code'] != 0:
		raise "登录接口报错"
	else:
		token = res['data']['token']


	# 新增分类
	"""n = 20
	index = 24
	while n < 120:
		add_catebage(num=n, index=index)
		n = n + 1
		index += 1"""


