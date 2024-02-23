# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-20 19:00
# ---
import time
# import gevent   # 可使用gevent.sleep()检测是否阻塞
from gevent import monkey
import gevent

monkey.patch_all()  # 进行非阻塞操作

def work1():
    for i in range(5):
        print("work1：听音乐---")
        time.sleep(1)


def work2():
    for i in range(5):
        print("work2：打游戏---")
        time.sleep(1)

def work3():
    for i in range(5):
        print("work3：发呆---")
        time.sleep(1)

def calc_time(func):
    """ 函数调用的执行时间"""
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"执行时间{(end - start_time):.2f}")
        return end - start_time
    return wrap

# @calc_time
def main():
    g1 = gevent.spawn(work1)  # 创建协程1对象
    g2 = gevent.spawn(work2)   # # 创建协程2
    g3 = gevent.spawn(work3)
    # g1.join()
    g2.join()
    print("所有任务执行完毕！！")

if __name__ == '__main__':
    main()
