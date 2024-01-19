# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-14 12:01
# ---
"""
multiprocessing.Queue :管道 序列化
Redis rabitMQ    kafka
MQ （message Queue）
"""
import time
from multiprocessing import Process, Queue

def work01(q: Queue):
    """
    :param q: 要处理的任务
    :return:
    """
    print('work01中的参数q的id：', id(q))
    while q.empty():
        print(f"work01开始处理{q.get()}")

def work02(q: Queue):
    """
    :param q: 要做的所有任务
    :return:#
    """
    print('work02中的参数q的id：', id(q))
    while q.empty():
        print(f"work02开始处理{q.get()}")

if __name__ == "__main__":
    # q = ['a', 'b', 'c']  # 执行时，不会共享q --使用list work1\2会做重复工作
    # 使用Queue,work1\2,共同完成q中的任务，q会被work1、work2共用。
    q = Queue()
    q.put('a')
    q.put('b')
    q.put('c')
    p1 = Process(target=work01, args=(q,))    # 子进程q1
    p2 = Process(target=work02, args=(q,))    # 子进程q2
    p1.start()
    # p2.start()
    time.sleep(0.1)
    print("执行结束")
