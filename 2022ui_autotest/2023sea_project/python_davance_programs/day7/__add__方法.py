# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-12 11:18
# ---

class Myclass(object):
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
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
