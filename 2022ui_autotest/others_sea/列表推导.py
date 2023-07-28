# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年11月月13日 16:19
# ---
"""
语法：[运算表达式 for in in 容器 简单表达式]
"""

lli = [i for i in range(1, 10)]
print(lli)
ll2 = [i*i for i in range(1, 111, 2) if i%2 == 1]
print(ll2)