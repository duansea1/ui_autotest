# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-12 11:18
# ---

class Myclass(object):
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        """
        在Python中，__add__是一个特殊的方法，也称为魔术方法或双下方法。
        当你在一个对象上使用加法运算符（+）时，Python会自动调用这个对象的__add__方法。
        """
        # self：第一个对象
        # other 第2个对象
        return self.value + other.value

if __name__ == "__main__":

    m1 = Myclass(1)
    m2 = Myclass(2)
    print(m1 + m2)
    print(m1.__add__(m2))
    m3 = object.__new__(Myclass)      # 创建对象
    m3.__init__(333)     # 初始化参数
    print(m3.value)
