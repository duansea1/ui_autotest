"""
@Author    : duansea
@Date      : 2025/7/22 09:46
@Description: [文件功能的简要描述]
"""
from collections import namedtuple

Person = namedtuple('Person', ['name', 'age', 'gender'])

p1 = Person('duansea', 25,'male')
print(p1.name)
print(p1.age)
print(p1.gender)

# 自定义数据类型
class Person(namedtuple('Person', ['name', 'age', 'gender'])):
    __annotations__ = {'name': str, 'age': int, 'gender': str}