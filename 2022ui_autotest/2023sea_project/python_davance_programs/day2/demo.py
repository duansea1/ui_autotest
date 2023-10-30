
# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-24 21:23
# ---

from python_davance_programs.day2.私有变量 import x, _y

print(x)
print(_y)


class A:
    def __init__(self):
        self.name = 'zhangjing'
        # self.age='24'

    def method(self):
        print("method print")

Instance = A()
print(getattr(Instance, 'name', 'not find'))
# 如果Instance 对象中有属性name则打印self.name的值，否则打印'not find'

print(getattr(A, 'age', 'not find age!!'))
# 如果Instance 对象中有属性age则打印self.age的值，否则打印'not find'

print(getattr(A(), 'method', 'default'))
