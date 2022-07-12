import time
from time import sleep
def foo():
    print("hell0")


def foo1():
    t1 = time.time()
    print("hello")
    t2 = time.time()
    print('foo1:', t2 - t1)

# foo1()

def run_time(func):
    def warp():
        print('开始执行warp')
        t1 = time.time()
        rucan = func()  #执行函数,括号不能去掉
        sleep(1)
        t2 = time.time()
        print('时间差：', (t2 -t1))
        print('run_time执行完成')
        print(rucan)
        return rucan
    return warp()

# f = run_time(foo1)
# print(f)


#  修饰器，传参为修饰的函数，可以看上边的入参，不需要实例化打印
@run_time
def foo2():
    t1 = time.time()
    print("hello-开始执行foo2")
    t2 = time.time()
    print('foo2:', t2 - t1)



@run_time
def foo3():
    t1 = time.time()
    print("hello-开始执行foo3")
    t2 = time.time()
    print('foo3:', t2 - t1)
    return "foo3执行完成"

print("===========带参数+++++++++++")
def run_time_f(func):
    def warp(*args, **kwargs):
        print('开始执行warp_f')
        t1 = time.time()
        rucan = func(*args, **kwargs)  #执行函数,括号不能去掉
        sleep(1)
        t2 = time.time()
        print('时间差_c：', (t2 -t1))
        print('run_time_f执行完成')
        print(rucan)
        return rucan
    return warp

@run_time_f
def foo4(a, b, c):
    return (a, b, c)

print('foo4+++++++++:', foo4(1, 2, 3))

print("+++++++++++++++++++++++++++++++++++++++++++++++++")
def decorator_with_parm(name):
    def run_time5(func):  # func 为要修饰的对象
        def warp5(*args, **kwargs):
            print('-----------------------：', name)
            temp = func(*args, **kwargs)
            return temp
        return warp5
    return run_time5     # 有传参时，不能加（）

def run_time6(func):  # func 为要修饰的对象
    """修饰器，若多个参数，需要参数化 *args\**kwargs  return 出方法"""
    def warp5(*args, **kwargs):
        print('--------多个参数---------------：')
        temp = func(*args, **kwargs)
        return temp
    return warp5

@decorator_with_parm(name='foo5')
def foo5(a, b, c):
    print('打印foo5')
    return (a, b, c)

@run_time6
def foo6(a, b, c):
    print('打印foo5')
    return (a, b, c)

f5 = foo6(2, 3, 'qqqqq')
print(f5)