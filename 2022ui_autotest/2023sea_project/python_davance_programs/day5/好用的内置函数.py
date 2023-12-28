# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-06 21:38
# ---
from functools import reduce
# print(help(filter))
# filter(怎么过滤，要过滤的对象)
# map（如何映射， [要映射的对象1，要映射的对象2]） 对要映射的对象1，进行“映射操作”
# reduce()
def filter_test():
    def f(x):
        if x > 2:
            return True
    print(filter(None, [1,2,3]))
    return filter(f, [1,2,3])   # None 对Itertor不做任何操作

def map_test():
    # return map(lambda x: x+2, [1, 2, 3])   # 对[1,2, 3]中的每一个元素进行x+2的处理

    # return map()  # 把两个列表中的元素相加，生成新的列表
    nums1 = [1,2,3]
    nums2 = [1,2,3]
    result = []
    # for i, v in enumerate(nums1):  # 不使用map实现
    #     result.append(v +nums2[i])
    # 使用map实现

    # return list(map(lambda x, y: x+y, nums1, nums2)) # 两种方法实现两个列表相加
    return list(map(lambda nums1, nums2: nums1+nums2, nums1, nums2))


def reduce_test():
    # 累加功能 1~5的累计功能 [1,2,3,4,5] =>(((1+2) + 3) + 4)
    def f(x, y):
        result = x +y
        return result
    reduce(f, [1,3,1])
    print(reduce(f, [1, 2, 3, 4, 5]))

def zip_test():
    print(list(zip('ahhdjf', range(30), [13,2,3,4])))
    

if __name__ == "__main__":
    for vale in filter_test():
        print(vale)

    print('----------------')
    for value in map_test():
        print(value)
    print('---------------')
    print(map_test())
    zip_test()