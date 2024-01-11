# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-24 21:28
# ---
# python 自省：python运行时知道对象有哪些东西
class Person(object):
    name = "我们"
print(dir(Person))  # dir是自省的一种，查看有哪些属性
print(hasattr(Person, "name"))  # 作用查看对象，有没有某个属性bool

# 使用场景举例：  检查函数参数（类型检查isinstance等）
print(isinstance(Person, str))
"""
getattr()  # 获得某个对象的属性
setattr()  # 设置某个对象的属性

"""
print(hasattr(Person, "name"))
print(getattr(Person, "name"))
print(setattr(Person, "name", "kevin"))  # 设置属性
