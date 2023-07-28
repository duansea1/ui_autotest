# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : xxxx

# getattr()
import sys

for i in sys.argv:
    print(i)

print(sys.path[0])




def decorator(func):
    def inner(*args, **kwargs):
        print('内函数执行前')
        func(*args, **kwargs)
        print('执行结束')
    return inner


@decorator
def show(name, age, sex):
    print(f'一只战斗机：{name},年龄{age},性别：{sex}')


# re = decorator(show)
# re('小米', '21', '女')

show('小米', '21', '女')



