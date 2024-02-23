# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 18:31
# ---
import threading
import time

n = 20000
lock = threading.Lock()
def work():
    global n
    for i in range(10):
        # 上锁
        # lock.acquire()
        n -= 1
        print(f'第{20000-n}次执行')
        # 释放锁
        # lock.release()

if __name__ == '__main__':
    t1 = threading.Thread(target=work)     # 创建第一个进程
    t2 = threading.Thread(target=work)    # 创建第2个进程
    t1.start()
    # t2.start()
    t1.join()
    # t2.join()
    print(n)


