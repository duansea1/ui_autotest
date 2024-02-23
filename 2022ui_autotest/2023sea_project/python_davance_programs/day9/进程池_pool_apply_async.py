# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 17:43
# ---
from multiprocessing import Pool

def est(x, y, z=1):
    print("_--------------")
    return x + y

if __name__ == '__main__':
    pool = Pool(2)
    # apply(self, func, args=(), kwds={})
    """
    apply：调用函数，传递任意参数
    map：把一个可迭代对象，映射到函数
    """
    result = pool.apply(est, (2, 3), {'z': 2})  # 阻塞 主程序（主进程）
    print(result)
    # pool.apply_async(test, (2, )) # 不阻塞 主程序
