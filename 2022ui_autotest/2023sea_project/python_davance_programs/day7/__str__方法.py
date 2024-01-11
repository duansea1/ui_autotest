# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-12 11:04
# ---
"""
__str__ 是一个特殊的方法，用于返回对象的“字符串表示”。当您尝试打印一个对象或将其转换为字符串时，Python会自动调用这个方法。
"""
print(hasattr(list, '__str__'))  # True

class Mylist(list):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):    # print 对象时，输出的样子。返回的一定是字符串
        return "list:" + str(self[0]) + self.name + self.age

nums = Mylist([1, 2, 3])
print(nums)

