# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-06 20:02
# ---
# nums = [1, 22, 4, 55]  # 输出大于5的元素到新列表
def new_nums(nums: list):
    new_list = []
    for num in nums:
        if num > 5:
            new_list.append(num)
    return new_list

print(new_nums(nums=[1, 22, 4, 55]))

def filter_nums2(list1: list, mark: int):

    return [num for num in list1 if num > mark]

print(filter_nums2([5.6,4,5,33],5))

def filter_nums(nums, mark):
    """
    :param nums:列表含有数字元素
    :param mark: 判断数字大小的给定值
    :return: 大于mark的list
    """
    return list(filter(lambda x: x <= 2, nums))
    # return list(filter(lambda x: x > mark, nums))


print(filter_nums(nums=[44, 1, 2], mark=5))
