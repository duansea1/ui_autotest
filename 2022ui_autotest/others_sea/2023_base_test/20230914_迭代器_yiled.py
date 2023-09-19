# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月14日 9:53
# ---
from collections.abc import Iterator,Iterable

# 可迭代对象：list是否具有可迭代能力
print(issubclass(list, Iterable))
print(issubclass(Iterator, Iterable))

# 生成器是可迭代的 -generator:生成器对象
g = (i*i for i in [1, 4, 0])
print(g)
print(next(g))  # 生成器使用next

# yield出现在函数中，运行到yield，返回的对象是生成器对象（generator object）
# 生成器对象一定也是迭代器对象
# yield is a keyword that is used like return, except the function will return a generator.

print("----------yiled-----")


def gfun():
    mylist = range(3)
    for i in mylist:
        yield i*i


g1 = gfun()
print(g1)

# def createGenerator():
#     mylist = range(3)
#     for i in mylist:
#         yield i*i
#         print(i*i)
#
# g = createGenerator()
# print(g)
# for gi  in g:
#     pass


# yield 使用案例
def frange(start, end, step):
    i = start
    while i < end:
        yield round(i, 3)
        i += step


for item in frange(10, 14, 0.8):
    print(item)
