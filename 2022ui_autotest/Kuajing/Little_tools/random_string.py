# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-12-06 16:20
# ---
import random
import string

from datetime import datetime


def generate_random_string_with_time(length=12):
    """
    生成一个指定长度的随机字符串，其中包含时间信息。

    Args:
        length (int): 生成的字符串长度，默认为12。

    Returns:
        str: 包含时间信息的随机字符串。
    """
    # 获取当前时间并格式化为字符串
    now = datetime.now()
    time_str = now.strftime('%Y%m%d%H%M')  # 格式：年月日时分

    # 确保时间字符串的长度不超过给定的总长度
    if len(time_str) > length:
        raise ValueError("Time string is longer than the specified length.")

    # 随机字符集（字母和数字）
    chars = string.ascii_letters + string.digits

    # 计算需要补充的随机字符数量
    random_part_length = length - len(time_str)

    # 生成随机字符部分
    random_part = ''.join(random.choices(chars, k=random_part_length))

    # 组合时间字符串和随机字符
    result = time_str + random_part

    # 如果需要，可以对结果进行混洗以增加随机性
    result_list = list(result)
    random.shuffle(result_list)
    result = f"sea-{''.join(result_list)}"
    print(f"result::{result}")
    return result
if __name__ == '__main__':
    generate_random_string_with_time()