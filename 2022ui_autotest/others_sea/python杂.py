# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年1月月09日 18:59
# ---
<<<<<<< HEAD
<<<<<<< HEAD

from collections import Counter


def strpinjie(l=[]):
    '''列表-拼接字符串'''
    newstr = "".join(l)
    return newstr


def maxnumstr(l=[]):
    """"查找列表中频率最高的值"""
    ll = set(l)
    print('ll', ll)
    print('count:', l.count)
    return max(l, key=l.count)


def maxcounter(a):
    """统计出现的次数"""
    msg = '其他类型，不是str、list、tuple'
    re = {'code': 0, 'msg': msg}
    if isinstance(a, list):
        l = Counter(a)
        print('列表类型：', l)
        return {'code': 0, 'msg': l, 'maxsow': l.most_common(3)}
    elif isinstance(a, str):
        l = Counter(a)
        print('str类型：', l)
        return {'code': 1, 'msg': l, 'maxsow': l.most_common(3)}
    elif isinstance(a, tuple):
        l = Counter(a)
        print('tuple类型：', l)
        return {'code': 2, 'msg': l, 'maxsow': l.most_common(3)}
    else:
        return {'code': 3, 'msg': msg, 'maxsow': a}


def check_diffict_two(a, b):
    """比较两个数据是否是 相同字母不同顺序组成的
    :param a: 第一个参数
    :param b : 第二个参数
    """
    return Counter(a) == Counter(b)


def resver_str(a, method):
    """字符串翻转"""
    if method == 1:
        resver_str = a[::-1]
        return resver_str
    elif method == 2:
        # a = a[::-1]
        for char in reversed(a):
            print('char:', char)
            return list(reversed(a))  # 翻转list
    elif method == 3:
        return int(str(a)[::-1])  # in类型转化为字符串
    else:
        return "参数错误"


def transposed_zip(zips=[['a', 'b'], ['b', 'c'], ['e', 'f'], ['ee', 'ff']]):
    """转置二位数组"""
    transposed = zip(*zips)
    return list(transposed)


def chained(b=6):
    """判断区间数字是否存在 """
    return 2 == b < 9  # true or false


def yichuChongfuZhifu(l, method='list'):
    if method == 'list':
        newl = list(set(l))
        return newl
    else:
        return 'wuyich'


def TwoNumsIndex(nums, target):
    """给出一个不重复的整数组，获取两个num相加等于target对应num的索引"""
    for i in range(len(nums)):
        req = target - nums[i]
        if req in nums[i+1:]:
            return [i, nums[i+1:].index(req)+i+1]


def TwoNumsIndex2(nums, target):
    """给出一个不重复的整数组，获取两个num相加等于target对应num的索引"""
    lens = len(nums)
    for i in range(lens):
        for j in range(i+1, lens):
            if i != j and (target - nums[i]) in nums[i+1:]:
                # nums[i+1].index(target-nums[i]+i+1) 为获取第2个数字的索引，
                # 因第2个数的索引从i+1开始，估在原列表的索引位置需加上
                return [i, nums[i+1:].index(target-nums[i])+i+1]

# def TwoNumsIndex3(nums, target):
#     """给出一个不重复的整数组，获取两个num相加等于target对应num的索引"""
#     dic = enumerate(nums)
#     for i in range(len(nums)):
#         if j, (target - nums) in dic:
#             return [i, dic[target-nums]]


def nums_add(nums):
    """给定一个列表，累计计算  [1,2,3,4]-->[1,3,6,10]
    一维数组的动态和"""
    n = len(nums)
    for i in range(1, n):
        nums[i] = nums[i-1]+nums[i]
    return nums



if __name__ == '__main__':
    """
    re = strpinjie(l=['12', 'dhk', '中国'])
    print(re)
    l = [1, 2, 3, 4, 1, 1, 1, 1, 5, 6, 66, 33, 4]

    print(maxnumstr(l=l))

    print(maxcounter(a='dsgdfhdfhffffff'))

    print(maxcounter(a=['as', 'as', 'dd', 'tt', 'f']))
    print(maxcounter(a=1))
    print(check_diffict_two(a=[1, 2, 3], b=[1, 2, 3]))  # 比较两个数据是否一样
    print(resver_str(1234, method=3))
    print(resver_str(['a', 'b', 'c'], method=2))
    print(transposed_zip())  # 转换二维数组
    print(chained(b=6))
    """
    # 2023-2-1日
    reqnum = TwoNumsIndex([1, 2, 3, 4], 6)  # 两个数之后，求其对应数的索引
    print('两个数的索引：', reqnum)
    reqnum2 = TwoNumsIndex2([1, 2, 3, 4], 5)  # 两个数之后，求其对应数的索引
    print('两个数的索引：', reqnum2)
    # reqnum3 = TwoNumsIndex3([1, 2, 3, 4], 4)  # 两个数之后，求其对应数的索引
    # print('两个数的索引：', reqnum3)

    # 计算列表中的两束之和
    res_num = nums_add([1, 2, 3, 4, 5])
    print('列表中的数之和:{0}'.format(res_num))
=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
