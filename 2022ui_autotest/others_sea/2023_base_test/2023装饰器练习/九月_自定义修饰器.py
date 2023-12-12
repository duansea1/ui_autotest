# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月19日 17:59
# ---

#  1 、基本使用方式
def dec(a):
    print('参数a：', a)
    print('this method-修饰器函数')
    return a

@dec  # 使用修饰器
def funA():
    print("被修饰器函数-funA")
    pass

funA()  # 调用funA，但是会传给dec先执行后，最后执行funA函数
print("sea")

#  2、函数嵌套
print("**"*10 + '函数嵌套' + "*"*20)

def A(x): # 修饰器函数
    def B():
        print('B')
    B()
    return x

@A  # 使用修饰器
def C():  #被修饰器函数
    print("C")

C()  # 调用被修饰器函数

print("**"*10 + '3、闭包' + "*"*20)

def anmail(x):
    def bird():
        print('bird')
        return x()  # 无差别调用只能一层，这里是无法通过x调用, 直接调用被修饰的函数
    return bird

@anmail
def dog():
    print('dog')

dog()


print("**"*10 + '4、被修饰的函数有参数的形式' + "*"*20)
def anmail2(x2):  #  修饰器函数
    print('参数x：', x2)

    def bird2(aa, bb):  # 内嵌函数，接收被修饰函数传递的参数
        print('bird2')
        print("函数bird2的参数", aa, bb)
        return x2(aa, bb)  # 无差别调用只能一层，这里是无法通过x调用, 直接调用被修饰的函数
    return bird2

@anmail2
def dog2(n, nn):
    print('dog')

dog2('10', '20')

print("**"*10 + '5、有参数的修饰器，无参数的函数，使用内嵌函数收取参数' + "*"*20)

# 如果修饰器有参数，但被修饰器函数确没有参数的情况下，只能使用内嵌函数来收取参数
def fun(a=20):  # 修饰器函数
    print(a)

    def pig(cc):
        print('pig的参数', cc)
        return cc  #  可以无差别调用，因为是在第二层才棘手的funB,相当于第一层
    return pig

@fun(30)
def funB():   # 被修饰器函数
    print('xixiixi')

funB()