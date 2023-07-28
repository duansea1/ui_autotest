# -*- coding: utf-8 -*-
# ---
# @Software: call魔法函数的作用就是类的实例
# 可以继续像函数一样调用，像函数一样调用对象的时候就会走到类的call魔法函数了
# @Author: duansea
# @Time: 2022年9月月05日 20:52
# ---
class Test(object):
    def __init__(self, a, b=10):
        self.a = a
        self.b = b

    def __call__(self,c,d=20):
        print("a+b:", self.a+self.b)
        print(self.a+c)
        print(self.b+d)


test = Test(1,2)
test(100, 200)

print("=============分割线====================")

class Test2(object):
    def __init__(self, a, b=10):
        self.a=a
        self.b=b

    def __call__(self,func):
        def wrapper(*args,**kwargs):
            print("before func {func}".format(func=func.__name__))
            results=func(*args,**kwargs)
            print("after func {func}".format(func=func.__name__))
            return results
        return wrapper

@Test2(11, 22)
def print_sum(v1,v2):
    print("in print_sum()...")
    print(v1+v2)

print_sum(20,200)

print("=============分割线====================")
#   setattr的使用
class Test3(object):
    pass

t=Test3()
setattr(t,"str_a","设置settar")

print(t.str_a)

print("=============分割线====================")


import pluggy


hookspec = pluggy.HookspecMarker("myproject")


@hookspec
def test4():
    pass


@pluggy.HookspecMarker("myproject2")
def test5():
    pass


print("test()函数使用钩子：", test4.myproject_spec)
print(test5.myproject2_spec)

# -----------------------------------
# ©著作权归作者所有：来自51CTO博客作者redrose2100的原创作品，请联系作者获取转载授权，否则将追究法律责任
# Pytest核心原理之Pluggy插件源码解读（1）HookspecMarker类和HookimplMarker类分析
# https://blog.51cto.com/u_11160105/5515193