# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月05日 9:26
# ---

# next函数执行到最后一位，取不到值时报StopIteration异常
my_list = [1, 2, 'tom']
my_inter = iter(my_list)

print(next(my_inter))
print(next(my_inter))
print(next(my_inter))
# print(next(my_inter))

# 生成器 generater
# 生成器是特殊的容器
g = (i*i for i in range(10))
# 使用
print(next(g))

"""
函数生成器：
在函数中使用yield 返回数据，并且终止代码继续执行
2、并且有yield的函数 当我们调用该函数的时候自动创建好一个生成器
3、通过next（）获取返回值，并且让程序继续执行。
4、也可以通过for循环遍历获取生成器
"""