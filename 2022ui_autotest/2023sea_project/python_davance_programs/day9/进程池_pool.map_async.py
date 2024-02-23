# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 17:10
# --- TODO 含本文件
import time
from multiprocessing import Pool

def square(x):
    print("00000000000000")
    time.sleep(1)
    return x * x

def sums(args):
    """ 求和计算 """
    x, y = args
    return x + y


if __name__ == '__main__':
    start = time.time()
    # pool = Pool(2)
    # result = pool.map_async(square, [1, 2, 3, 4, 5])  # []中的 分别取给square --map会阻塞主程序
    # print(result.get())  # get是阻塞

    t1 = time.time()
    p = Pool(5)
    data = [(i, i + 1) for i in range(1, 4)]  # 扩展数据以匹配sums函数的参数
    print(data)
    res = p.map_async(sums, data)
    print(res.get())
    print("All tasks completed.")
