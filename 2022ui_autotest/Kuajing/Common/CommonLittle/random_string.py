"""
@Author    : duansea
@Date      : 2025/6/25 10:46
@Description: [文件功能的简要描述]
"""
import datetime
import random


def generate_random_string(prefix="", suffix_length=3):
    """
    生成时间戳 + 随机数的字符串（无横线分隔）

    参数:
        prefix (str): 可选前缀（例如 "sea"）
        suffix_length (int): 随机数位数（默认为3）

    返回:
        str: 格式为 {prefix}YYYYMMDDHHMMSS{random_numbers}
    """
    # 获取当前时间，格式化为 YYYYMMDDHHMMSS
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 生成指定位数的随机数（补零）
    random_num = str(random.randint(0, 10 ** suffix_length - 1)).zfill(suffix_length)

    # 拼接结果（无横线）
    return f"{prefix}{current_time}{random_num}"


# 示例用法
# print(generate_random_string())  # 输出如: 20250625104301001
# print(generate_random_string("sea"))  # 输出如: sea20250625104301001
# print(generate_random_string(suffix_length=4))  # 输出如: 202506251043010001