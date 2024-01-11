# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月14日 9:53
# ---
from collections.abc import Iterator,Iterable



# 可迭代对象：list是否具有可迭代能力
print(issubclass(list, Iterable))
print(issubclass(Iterator, Iterable))

# 生成器是可迭代的 -generator:生成器对象
g = (i*i for i in [1, 4, 0])
print(g)
print(next(g))  # 生成器使用next

# yield出现在函数中，运行到yield，返回的对象是生成器对象（generator object）
# 生成器对象一定也是迭代器对象
# yield is a keyword that is used like return, except the function will return a generator.

print("----------yiled-----")


def gfun():
    mylist = range(3)
    for i in mylist:
        yield i*i


g1 = gfun()
print(g1)

# def createGenerator():
#     mylist = range(3)
#     for i in mylist:
#         yield i*i
#         print(i*i)
#
# g = createGenerator()
# print(g)
# for gi  in g:
#     pass


# yield 使用案例
def frange(start, end, step):
    i = start
    while i < end:
        yield round(i, 3)
        i += step


for item in frange(10, 14, 0.8):
    print(item)

print("*"*10 + "yield用法" + ""*10)

def yield_range(n):
    for i in range(n):
        yield i
        print('i=', i)
    print('do something')
    print('end')

def call(i):
    return i

for i in yield_range(10):
    print(i, ",")

print("*"*20 + "yield用法-浅入讲解" + "**"*20)


# !/usr/bin/python
# -*- coding: UTF-8 -*-

def fab(max):
    n = 0
    a, b = 0, 2
    while n < max:
        print(b)
        a, b = b, a + b  # 将右侧的值赋值到左边
        n = n + 1

fab(5)

# 第2个版本
print("*"*20 + "输出斐波那契數列前 N 个数第二版" + "**"*20)

def fab2(max):
    n = 0
    a, b = 0, 2
    L = []
    while n < max:
        L.append(b)
        a, b = b, a + b  # 将右侧的值赋值到左边
        n = n + 1
    return L

for m in fab2(5):
    print('第2版',m)


# !/usr/bin/python
# -*- coding: UTF-8 -*-
print("*"*20 + "输出斐波那契數列前 N 个数第3版" + "**"*20)
class Fab3(object):

    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):   # python3  迭代器规则发生了变化，而不是next.写成私有函数
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()


for n in Fab3(5):
    print(n)


# !/usr/bin/python
# -*- coding: UTF-8 -*-
print("*"*20 + "输出斐波那契數列前 N 个数第4版" + "**"*20)

def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b  # 使用 yield
        # print b
        a, b = b, a + b
        n = n + 1


for n in fab(5):
    print(n)

print("*"*20 + "yields使用：携程与并发" + "**"*20)
"""
这个程序的执行流程如下：
c = consumer() 创建一个生成器对象
producer(c) 开始执行，c.__next()__ 会启动生成器 consumer 直到代码运行到 j = yield i 处，此时 consumer 第一次执行完毕，返回
producer 函数继续向下执行，直到 c.send(i) 处，这里利用生成器的 send 方法，向 consumer 发送数据
consumer 函数被唤醒，从 j = yield i 处继续开始执行，并且接收到 producer 传来的数据赋值给 j，然后打印输出，直到再次执行到 yield 处，返回
producer 继续循环执行上面的过程，依次发送数据给 cosnumer，直到循环结束
最终 c.close() 关闭 consumer 生成器，程序退出
https://zhuanlan.zhihu.com/p/321302488
"""
def consumer():
    i = None
    while True:
        # 拿到producer 发来的消息
        j = yield i   # 4、此时consumer 第一次执行完毕，进行返回   《--6、从此处开始执行，接收到produce传来的数据赋值给j，然后打印输出
        print("consumer %s" % j)  # 7\打印数据

def producer(c):
    c.__next__()  # 3、c.__next()__ 会启动生成器
    for i in range(5):
        print("produce %s" % i)
        # 发数据给consumer
        c.send(i)   # 5、利用生成器的send方法，项consumer发送数据；consumer函数被唤醒
    c.close()

c = consumer()  # 1、创建一个生成器对象
producer(c)  # 2、开始执行
