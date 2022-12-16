# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月04日 9:16
# ---
import sys

class Goods():
    def __init__(self, goodname, price, county):
        self.goodname = goodname
        self.price = price
        self.county = county

    def baseinfo(self):
        print("商品的基本信息:",self.goodname, self.price, self.county)

class Drugs(Goods):
    def __init__(self, activity, datetime, goodname, price, county):
        self.activity = activity
        self.datetime = datetime
        super().__init__(goodname, price, county=None)

    def drug_activity_info(self):
        print("药品的活动信息：", self.activity, self.datetime)
        # Goods.baseinfo()

drug = Drugs(activity="满减", datetime="1年",goodname='阿莫西林',price='199元', county='中国')
drug.drug_activity_info()
drug.baseinfo()
print(dir(Drugs), end="")


