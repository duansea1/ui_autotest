# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月14日 15:35
# ---

res = (i for i in range(10))
print(res)
x = 2
y =22
ad = lambda x, y: x+y
print(ad)
print(ad(2,3))
print(type(ad))

a = lambda x=2, y=2: None
print(a())
print(type(a))


def quare(x):
    return x*2
list = list(map(quare, [1,2,3,4]))
print("list:", list)

import os
l = [d for d in os.listdir(".")]
print(l)