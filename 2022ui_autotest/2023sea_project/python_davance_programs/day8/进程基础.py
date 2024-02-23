# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-15 18:16
# ---
import os
import time
from multiprocessing import Process

def play_music():
    print('子进程p1', os.getpid())
    for i in range(5):
        print(f'play music...第{i+1}次')
        time.sleep(0.5)

def play_lol():
    print('子进程p2', os.getpid())
    for i in range(5):
        print(f'play lol...第{i+1}次')
        time.sleep(1)


if __name__ == '__main__':
    print('主进程', os.getpid())
    p1 = Process(target=play_music)
    p2 = Process(target=play_lol)
    # p1.daemon = True # 当为true时，主进程结束，会强制结束子进程
    # p2.daemon = True

    p1.start()

    p2.start()
    p1.is_alive()  # 返回true或者false
    print('join-------------开始执行')
    p1.join()  # 上面的代码任务没有运行完，不会运行下面的代码
