# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-29 10:17
# ---
# 意义：快速方便的创建一个迭代器
# yield的关键字，来实现快速创建迭代器
# 手动实现平方
L = []
for i in range(1,4):
    L.append(i*i)

class Squares(object):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.start > self.stop:
            raise StopIteration
        current = self.start * self.start
        self.start += 1
        return current

def squares(start, stop):
    for i in range(start, stop+1):
        yield i*i

# 第三种 推导式
squares3 = (i*i for i in range(1,4))
# print(squares3)

if __name__ == "__main__":
    # S = Squares(1, 3)
    S = squares(1, 3)
    print(enumerate(S))    # 返回的是迭代器 generator
    # 知识点：enumerate 是 Python 中的一个内置函数，它可以将可迭代对象\n
    # （如列表、元组或字符串）组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
    for i, value in enumerate(S, start=2):
        print(i, value)

