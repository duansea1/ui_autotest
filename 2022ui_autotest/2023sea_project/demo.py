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
if __name__ == '__main__':
    age()