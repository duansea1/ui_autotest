# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年3月月22日 13:39
# ---
import heapq

import ast
from enum import Enum



def find_maxOrmin_num():

    # 获取列表中n个最大或最小的元素
    scores = [23,45,11,36,89,244,123, 11,244]
    print(heapq.nlargest(3,scores))
    print(heapq.nsmallest(1,scores))

my_list = [1,2,3,4,33]
def send_args(my_list):

    #将列表中的所有元素，作为参数传递
    dic = {}
    # print(**dic)
    print(*my_list)

    return my_list


def shift_str_to_list(str):
    #将字符串的列表转化 为list
    return ast.literal_eval(str)

class Status(Enum):
    NO_STATUS = -1
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLEFTED = 2

def stored_two_str(str1, str2):
    """比较两个字符是否相等"""
    str1 = str1.lower()
    str2 = str1.lower()
    return sorted(str1) == sorted(str2)

def lianjie():
    """"两个字典拼接到一个(合并字典)"""
    dic1 = {'key1':'value1', 'key2':'value2'}
    dic2 = {'key3': 'value3', 'key4': 'value333'}
    dic = dic1|dic2
    print('两个字典拼接到一个', dic, sep='-----')

    dicdic = {**dic1, **dic2}
    print('dicidc', dicdic)

def frozesetlist(mylist):
    """把一个列表变成不可变的列表"""
    return frozenset(mylist)
    # return my_list


def splitstr(start=0,end=0,str='abcdef ghjk'):
    return str[start, end]


def check_start(str=None, checkstr=None):
    """检查字符串是否以特定字符开头的"""
    return str.startswith(checkstr)


if __name__ == '__main__':
    # find_maxOrmin_num()
    print(send_args(my_list))
    str = "['q',1,2],[1,2]"
    print(shift_str_to_list(str))
    print(Status.IN_PROGRESS.value == 1)
    print(stored_two_str('Here','ereH'))
    lianjie()  # 把两个字典合并成一个
    newlist = frozesetlist(mylist=['1','qq','3'])
    # print(newlist.append('3'))
    dictionary = {"a": 1, "b": 2, "c": 3}
    print({value:key for key, value in dictionary.items()})

    my_string = "This is just a sentence"
    print(my_string[10:12:-1])  # This
    # Take three steps forward
    print(my_string[0:10:3])  # Tsse
    print(check_start(str='qwert',checkstr='qew'))
    # cities = ['Beijing', 'guangzhou']
    # print(id(cities))
    # cities.append('henan')
    # print(id(cities))
    # 列表、集合、字典都是可变的，发生变更后，不会改变其内存对象
    my_set = {1,2,3,4,}
    print(id(my_set))
    my_set.add("hhhh")
    print(id(my_set))


