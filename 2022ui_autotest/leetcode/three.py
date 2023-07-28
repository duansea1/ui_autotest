# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年3月月02日 19:18
# ---

def removeElement1(nums, val):
    a = 0
    b = 0
    while a < len(nums):
        if nums[a] != val:
            nums[b] = nums[a]
            b = b + 1
        a = a + 1
    return b, nums


def removeElement2(nums, val):
    nums1 = []
    for index in range(0, len(nums)):
        if nums[index] != val:
            nums1.append(nums[index])
            print('被删除的数组',nums)
    return nums1

def removeElement4(nums, val):
    return [num for num in nums if num != val]


def removeElement3(nums, val):
    """输入：nums = [3,2,2,3], val = 3
    输出：2, nums = [2,2]
    解释：函数应该返回新的长度 2, 并且 nums 中的前两个元素均为
    2。你不需要考虑数组中超出新长度后面的元素。例如，函数返回的新长度为 2 ，
    而 nums = [2,2,3,3] 或 nums = [2,2,0,0]，也会被视作正确答案。
    来源：力扣（LeetCode）
    链接：https://leetcode.cn/problems/remove-element
    著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
    """
    n = nums.count(val)  # 计算val出现的次数
    for index in range(n):  # n-为val出现的次数
        nums.remove(val)  # 删除nums中的val
    return nums

def searchInsert(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: int
    """
    if len(nums) == 0:
        nums[0] = target
        return nums.index(target)
    if target in nums:
        for n in range(len(nums)):
            if nums[n] == target:
                return nums.index(target)
    else:
        for m in range(len(nums)):
            if nums[m] > target:
                if m == 0:
                    nums.insert(m, target)
                    return nums
                else:
                    nums.insert(m-1, target)
                    return nums
            else:
                nums.insert(m + 1, target)
                return nums

def searchInsert2(nums, target):
    """
    输入: nums = [1,3,5,6], target = 5
    输出: 2
    :type nums: List[int]
    :type target: int
    :rtype: int
    给定一个有序数组，给定1个数字，若存在数组中则返回位置，若不存在，则判断插入的位置并返回
    """
    for n in range(len(nums)):
        if nums[n] == target:
            return n
        elif nums[n] > target:
            return n

    return len(nums)

def check_string_isspace(str):
    '''检查字符串是否都是空格'''
    return str.isspace()

def shift_swapcase(str):
    """ 交换字符串中字符的大小写"""
    return str.swapcase()





if __name__ == "__main__":
    res = removeElement4(nums=[2, 1, 1, 2, 1], val=1)
    print('删除：',res)

    res1 = searchInsert2(nums=[1,2,3], target=1)
    print(res1)
    res2 = check_string_isspace(str=' 22  ')
    print(res2)
    res3 = shift_swapcase(str='This is a sentence !')
    print(res3)