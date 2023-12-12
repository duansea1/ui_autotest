# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月12日 16:20
# ---

def warp(obj):
    obj.name = 'sea'
    return obj

# @warp   # 等价于 foo = wrap(foo)
# def foo1():
#     print('hello,decorator')

@warp
class Bar(object):
    def __init__(self):
        pass
print(Bar().name)  # ==>sea


print("**"*10 + '模拟对象的装饰器' + "*"*20)

def outer(func):
    def inner(id=2):
        func
        print('id:',id)
    return inner

@outer
def foo11():
    print('hello foo')

foo11()

print("**"*10 + '类方法装饰器' + "*"*20)


def outer1(func):  # 类装饰器
    def inner(arg):
        print('执行函数前：:', arg)
        func(arg)
        print('执行函数后：:', arg)
    return inner

class Zoo(object):
    def __init__(self):
        pass

    @outer1
    def zoo(self):
        print('欢迎进入动物园')

zoo = Zoo()
# print(zoo.zoo.__name__)
zoo.zoo()

print("**"*10 + '带参数的装饰器' + "*"*20)


url_mapping = {}
def route(url):
    def decorator(func):  # 函数装饰器
        url_mapping[url] = func
        return func
    return decorator

@route("/home")
def home():
    print('函数的名称', home.__name__)

@route("/page")
def page():
    print('函数的名称', page.__name__)

home()
print(url_mapping)