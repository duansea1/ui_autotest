# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-20 18:52
# ---
import time


def work1():
    for i in range(5):
        print("work1：听音乐---")
        time.sleep(1)
        yield

def work2():
    for i in range(5):
        print("work2：打游戏---")
        time.sleep(1)
        yield

def calc_time(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"执行时间{(end - start_time):.2f}")
        return end - start_time
    return wrap

# @calc_time
def main():
    g1 = work1()
    g2 = work2()
    while True:
        try:
            next(g1)
            next(g2)
        except StopIteration as e:
            print(e)
            break


if __name__ == '__main__':
    main()
