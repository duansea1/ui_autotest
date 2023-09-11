# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年8月月15日 9:27
# ---

class Solution(object):
    def twoSum(self, nums, target):
        """
        给定一个列表，一个特定数，找到列表中两数相加==特殊数，的两个数字所在的位置。
        :param nums: list[]
        :param target: int
        :return: list[int]
        """
        print('开始执行')
        for i in range(len(nums)):
            # 计算需要找到的下一个目标数字
            res = target - nums[i]
            # 遍历剩下的元素，查找是否存在该数字
            if res in nums[i + 1:]:
                # 若存在，返回答案。这里由于是两数之和，采用.index获取索引位置
                # 获取目标元素在nums[i+1:]--因列表中的元素之和唯一，为
                local_index = [i, nums[i + 1:].index(res) + i + 1]
                return local_index


if __name__ == "__main__":
    re = Solution().twoSum(nums=[4, 6, 2, 1], target=5)
    print(re)
