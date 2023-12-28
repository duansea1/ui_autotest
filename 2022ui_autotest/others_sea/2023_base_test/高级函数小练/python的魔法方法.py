# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-12-15 9:17
# ---

# 8. `__enter__`方法和`__exit__`方法：定义上下文管理器。

class MyContext:
    def __enter__(self):
        print("Entering the context")
        print('执行enter方法')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")


with MyContext() as context:
    # 执行上下文中的操作

    print("Inside the context")

print('--------'*50)

# 9. `__call__`方法：使对象可调用。

class MyCallable:

    def __init__(self, func,a=1, b=2):
        print('初始化init操作')
        self.a = a
        self.b = b
        self.func = func

    def __call__(self, *args, **kwargs):
        print('__call__是对象可被调用')
        # return self.func(*args, **kwargs)

def sum(a=1,b=2):
    print('总和：', a + b)
    return str(a * b)


my_callable = MyCallable(func=sum(a=1,b=1))
# my_callable() # 输出 "Calling the object"
my_callable()
# print(my_callable)

import gc

print(gc.collect())