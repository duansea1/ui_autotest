# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 17:10
# ---
import time
from multiprocessing import Pool

def square(x):
    print("00000000000000")
    result = x * x
    time.sleep(1)

if __name__ == '__main__':
    start = time.time()
    pool = Pool(2)
    result = pool.map_async(square, [1, 2, 3, 4, 5])  # []中的 分别取给square --map会阻塞主程序
    print(result.get())  # get是阻塞


