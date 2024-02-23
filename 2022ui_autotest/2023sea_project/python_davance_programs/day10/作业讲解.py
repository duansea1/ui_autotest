# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-20 12:25
# ---
"""
1、简单描述同步、异步的区别？
-同步：同步是线性执行。前面的执行后，才会执行后边的
-异步：异步允许同时执行多个任务，互不影响。

2、一个列表中有100个url(假设每个请求地址0.5s)，请设计一个程序，获取列表中的url地址，使用4个线程去发送这100个请求计算出总耗时

"""

import time
from multiprocessing.pool import ThreadPool
import queue
import requests
import re

def calctime(func):
    """统计耗时时间"""
    def director(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time
    return director

def download(q: queue.Queue):
    while not q.empty():
        print(q.get())
        # re = requests.get(url=q.get())
        # print(re)
        q.task_done()  # 这个任务做完了

@calctime
def main():
    q = queue.Queue()   # 创建队列
    for i in range(1):         # 创建n个请求地址到队列里面
        q.put(f'http://www.gushi.com?page={i}')

    pool = ThreadPool(4)  # 创建执行的线程4个线程
    # apply_async是异步非阻塞式，不用等待当前进程执行完毕，随时跟进操作系统调度来进行进程切换，即多个进程并行执行，提高程序的执行效率。
    pool.apply_async(download, args=(q, ))
    q.join()
    print('finished')

if __name__ == '__main__':
    print(main())

