# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年8月月28日 10:11
# ---

import random


def Uicode():
    """unicode码中收录了2万多个汉字,包含很多生僻的繁体字"""
    val = random.randint(0X4e00, 0x9fbf)
    return chr(val)


def GBK2312():
    """gbk2312对字符的编码采用两个字节相组合,第一个字节的范围是0xB0-0xF7, 第二个字节的范围是0xA1-0xFE."""
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xfe)
    val = f'{head:x} {body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str


if __name__ == '__main__':
    pass
print(Uicode())
print(GBK2312())

