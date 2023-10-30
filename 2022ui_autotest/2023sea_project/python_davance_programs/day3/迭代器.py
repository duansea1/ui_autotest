# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-28 11:40
# ---
from typing import Iterator,Iterable
# 如何判断某个对象是否是迭代器
# 方法一：使用isinstance
# 看对象有没有iter__ 和__next__
# 迭代器协议：1、迭代器类型必须实现__iter__和 __next__；；
# 2、__iter__方法必须返回self ;;3、__next__必须返回下一个值，没有则抛出异常StopItertor



l = [1,2,3]
obj = iter(range(1, 2))    # 把range 转换为Itertor类型S
# print(isinstance(l, list))
print(isinstance(obj, Iterator))
for attr in dir(obj):
    print(attr)
print("-------------------"*20)
for attr in dir(list):
    print(attr)




if __name__ == "__main__":
    pass
