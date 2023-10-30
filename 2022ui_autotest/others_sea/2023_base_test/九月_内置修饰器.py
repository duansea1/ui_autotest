# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月19日 18:57
# ---

class A:
    def __init__(self):
        self.__age = 20   # 实例属性

    @property
    def age(self):  # 被修饰的方法
        return self.__age

    @age.getter
    def age(self):  # 被修饰的方法
        return self.__age

    @age.setter
    def age(self, newage):  # 被修饰的方法
        self.__age = newage


class B:
    __name = 'B的私有属性'   # 私有属性在内部可以调用，在函数外不能只能调用

    def __init__(self):
        __name = self.__name
        print(__name)


a = A()
# a.age = 200
print(a.age)

# b = B()
# print(b.__name)

