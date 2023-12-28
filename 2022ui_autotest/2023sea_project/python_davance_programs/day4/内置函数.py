# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-06 20:02
# ---
# map
# zip

"""
map() 和 zip() 是 Python 中的内置函数，它们在处理迭代器和序列时非常有用。下面是它们的使用场景举例。

map()的使用场景举例
map() 函数用于将一个函数应用于一个（或多个）序列的每个元素。这是一个使用 map() 的例子：

"""

def square(x):
    return x ** 2

# 创建一个数字列表
numbers = [1, 2, 3]

# 使用map计算列表中 每个元素的平方

squares = map(square, numbers)
print(list(squares))

"""
zip()的使用场景举例
zip() 函数用于将多个【可迭代的】对象（如列表、元组等）的元素一一对应起来，返回一个元组的迭代器。这是一个使用 zip() 的例子：
左右匹配相同的位数

"""

# 创建两个列表
names = ['Alice', 'Bob', 'Charlie', '12', '1']
ages = [25, 30, 35,12]

zipped = zip(names, ages)
print(zipped)
for name, age in zipped:
    print(f'姓名{name}：年龄{age}')

