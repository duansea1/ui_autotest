# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-24 21:14
# ---

def stest_private_and_protected_public():
    # public 共有的
    # private 私有的
    # protected 受保护的 不被其他文件导入
    pass
x = 10
_y = 20


class A():
    def __init__(self):
        self.__z = 2  # 私有
    def __some_method(self):
        print(self)

a = A()
# print(a.__z)
if __name__ == "__main__":
    stest_private_and_protected_public()


