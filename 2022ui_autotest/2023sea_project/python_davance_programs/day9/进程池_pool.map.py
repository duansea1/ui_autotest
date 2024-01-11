# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 17:10
# ---
import time
from multiprocessing import Pool

def square(x):
    print("_____________________")
    result = x * x
    return result


if __name__ == '__main__':
    start = time.time()
    pool = Pool(5)
    result = pool.map(square, [1, 2, 3, 4, 5])   # []中的 分别取给square --map会阻塞主程序
    print(result)
    pool.close()
    end = time.time()
    print(f"总共用了{(end - start):.3f}时间")


