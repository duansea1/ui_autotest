# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月19日 19:11
# ---

class B:
    def __init__(self, name):
        self.name = name

    @staticmethod   # 加上staticmethod后，eat这个方法变成了一个普通函数，位置在类里面，但实际上相当于一个普通的函数，并不是类的方法了，所以需要传值，不然self就没有值而报错了
    def eat(self):  # 打印传递的值
        print(self)

"""
1. 这个函数是一个普通函数，只有这个类能用
2. 静态方法可以设置参数，也可以不需要参数了(self)
3. 该函数不能访问类的属性
"""
b = B("sea")
b.eat(1)
