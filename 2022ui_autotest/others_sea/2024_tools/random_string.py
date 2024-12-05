# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-12-05 17:31
# ---
import random
import string


def generate_strong_password(length=12):
    if length < 4:
        print("为了保证密码强度，长度应至少为4。")
        return None

    # 确保密码包含至少一个大写字母、一个小写字母、一个数字和一个特殊字符
    password = [
        random.choice(string.ascii_uppercase),  # 至少一个大写字母
        random.choice(string.ascii_lowercase),  # 至少一个小写字母
        random.choice(string.digits),  # 至少一个数字
        random.choice(string.punctuation)  # 至少一个特殊字符
    ]

    # 剩余的字符可以是任意的
    if length > 4:
        characters = string.ascii_letters + string.digits + string.punctuation
        password += [random.choice(characters) for _ in range(length - 4)]

    # 打乱密码字符顺序以增加随机性
    random.shuffle(password)

    # 将列表转换为字符串并返回
    strong_password = ''.join(password)
    print(f"生成的强密码: {strong_password}")
    return strong_password


# 调用函数生成默认长度为12的强密码
generate_strong_password()