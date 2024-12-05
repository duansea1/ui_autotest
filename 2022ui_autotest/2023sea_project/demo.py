# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月21日 12:48
# ---

def age():
    "今年父亲45岁，儿子11岁，求多少年前父亲是儿子年龄的11倍"
    x = 45
    y = 15
    for i in range(0, y):
        if x / y == 11 and x % y == 0:
            print(f'{i}年前。父亲{x}岁，儿子{y}')
            break
        x -= 1
        y -= 1

def sums(num):
    sum = 0
    if num > 0:
        for i in range(num):
            sum += i
        return sum
    return sum

def digui_sums(num):
    sum =0
    if num > 0:
        return sum + digui_sums(num-1)
    return 0

t = {'你好':123 , 2023:1, '结束':3}
def add(a, b,c):
    """ 数组使用*传参"""
    return str(a) + str(b)

if __name__ == '__main__':
    # age()
    pass
    print(sums(200))
    print(digui_sums(200))
    print(add(*(t.values())))


class API_demo:
    pass