# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月21日 9:31
# 说明：装饰器函数练习举例
# ---
import time

print("**"*10 + '1、入门：直接执行func函数' + "*"*20)
def decorator(func):
    def wrapper(*args, **kw):
        return func()   # 使用return 和不用效果一样，因wrapper里没有需要执行的其他函数

    return wrapper


@decorator
def function():
    print("hello, decorator")


function()


print("**"*10 + '入门：日志打印器' + "*"*20)

def loggor(func):
    def wrapper(*args, **kwargs):
        print('准备开始执行：{} 函数了:'.format(func.__name__))
        # 函数真正执行的这行见下
        func(*args, **kwargs)
        print('执行完啦')
    return wrapper

# 假设我们的业务是计算两数之和
@loggor
def add(x, y):
    print('{} + {} = {}'.format(x, y, x+y))

add(200, 50)

print("**"*10 + '入门：时间计时器' + "*"*20)

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        # 函数执行的地方
        func(*args, **kwargs)
        t2 = time.time()
        cost_time = t2 - t1
        print("花费时间：{}秒".format(cost_time))
    return wrapper

@timer
def want_sleep(sleep_time):
    time.sleep(sleep_time)

want_sleep(0.2)


print("**"*10 + '进阶：带参数的函数装饰器' + "*"*20)

def say_hello(contry):
    def wrapper(func):
        def deco(*args, **kwargs):

            if contry == "china":
                print('你好!')
            elif contry == 'america':
                print('hello.')
            else:
                return
            # 真正执行函数的地方
            func(*args, **kwargs)
        return deco
    return wrapper

# 小明，中国人
@say_hello("china")
def xiaoming():
    pass

xiaoming()

print("**"*10 + '高阶：不带参数的类装饰器' + "*"*20)
""" 基于类装饰器的实现，必须实现__call__  和__init__ 两个内置函数。
__init__ ：接收被装饰函数   __call__ 实现装饰逻辑"""

class Logger(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("[INFO1]: the function {func}() is running...".format(func=self.func.__name__))
        return self.func(*args, **kwargs)


@loggor
def say(something):
    print("say {}!".format(something))

say("here we are!")


print("**"*10 + '高阶：带参数的类装饰器!!!' + "*"*20)
"""
上面不带参数的例子，你发现没有，只能打印INFO级别的日志，正常情况下，我们还需要打印DEBUG WARNING等级别的日志。 
这就需要给类装饰器传入参数，给这个函数指定级别了。
带参数和不带参数的类装饰器有很大的不同。
__init__ ：不再接收被装饰函数，而是接收传入参数。 __call__ ：接收被装饰函数，实现装饰逻辑。
"""
class Logger2(object):
    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func):  # 接收函数
        def wrapper(*args, **kwargs):
            print("[{level}]: the function {func}() is running...".format(level=self.level, func=func.__name__))
            func(*args, **kwargs)
        return wrapper   # 返回函数

@Logger2(level='WARNING')
def say2(anything):
    print("say {}!".format(anything))

say2('nice to you')
