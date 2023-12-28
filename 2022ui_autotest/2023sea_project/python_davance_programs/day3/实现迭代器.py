# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-28 11:56
# ---

# 迭代器  __iter__（） __next__（）

# 如何判断某个对象是否是迭代器
# 方法一：使用isinstance
# 看对象有没有iter__ 和__next__

"""
# 迭代器协议：
1、迭代器类型必须实现__iter__和 __next__；；
2、__iter__方法必须返回self ;;
3、__next__必须返回下一个值，没有则抛出异常StopItertor
4、对迭代器进行for操作时，每次都会执行__next__
5、迭代器，只能迭代一次（循环一次）
6、for语句会忽略StopIteration异常
"""


class MyIter(object):
    def __init__(self, stop, start=0):
        self.stop = stop
        self.start = 1

    def __next__(self):
        """如果有下一个数，返回下一个数；如果没有则返回异常StopIteration"""
        print(f'开始执行{MyIter.__iter__}')
        if self.start >= self.stop - 1:
            raise StopIteration
        self.start += 1
        return self.start

    def __iter__(self):
        return self  # 必须返回self 才是可迭代对象

if __name__ == "__main__":
    obj = MyIter(1)
    # for i in obj:
    #     print(i)
    # print(obj.__next__())
    # print(obj.__next__())
    # print(obj.__next__())
    # print(obj.__next__())

    for i, value in enumerate(obj):
        print(i, value)
