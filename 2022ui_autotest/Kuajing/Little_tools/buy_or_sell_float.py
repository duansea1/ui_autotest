# -*- coding: utf-8 -*-
# ---
# 计算客买、客卖浮动值
# @Time: 2024-12-02 15:13
# ---

def calculate_exchange_rates(target_ASK_rate, target_BID_rate, X=0, Y=0, Z=0, X1=0, Y1=0, Z1=0):
    """
    计算客卖方向和客买方向的汇率。

    参数:
    - target_ASK_rate (float): 目标汇率-客买方向
    - X-交易员设置的浮动
    -Y-销售设置的浮动
    Z-代理商设置的浮动

    - target_BID_rate (float): 目标汇率-客卖方向
    - X1-交易员设置的浮动
    -Y1-销售设置的浮动
    Z1-代理商设置的浮动

    返回:
    - sell_rate (float): 客卖方向汇率
    - buy_rate (float): 客买方向汇率
    """
    # 客买方向汇率
    buy_rate = target_ASK_rate * (1 + X / 100) * (1 + Y / 100) * (1 + Z / 100)
    print(f"客买-方向汇率：{buy_rate}")

    # 客卖方向汇率
    sell_rate = target_BID_rate * (1 - X1/100)*(1-Y1/100)*(1-Z1/100)
    print(f"客卖-方向汇率：{sell_rate}")

    return sell_rate, buy_rate

def calculate_BP_rates(target_ASK_rate, target_BID_rate, X=0, Y=0, Z=0, X1=0, Y1=0, Z1=0):
    """
    计算客卖方向和客买方向的汇率。

    参数:
    - target_ASK_rate (float): 目标汇率-客买方向
    - X-交易员设置的浮动
    -Y-销售设置的浮动
    Z-代理商设置的浮动

    - target_BID_rate (float): 目标汇率-客卖方向
    - X1-交易员设置的浮动
    -Y1-销售设置的浮动
    Z1-代理商设置的浮动

    返回:
    - sell_rate (float): 客卖方向汇率
    - buy_rate (float): 客买方向汇率
    """
    # 客买方向汇
    buy_rate = target_ASK_rate + X/100 + Y/100 + Z/100
    print(f"客买-方向汇率：{buy_rate}")

    # 客卖方向汇率
    sell_rate = target_BID_rate - X1/100 - Y1/100 - Z1/100
    print(f"客卖-方向汇率：{sell_rate}")

    return sell_rate, buy_rate


def reverse_calculate_exchange_rates(sell_rate, buy_rate, X=0, Y=0, Z=0, X1=0, Y1=0, Z1=0):
    """
    根据客卖方向和客买方向的汇率以及各浮动比例，反推目标汇率。

    参数:
    - sell_rate (float): 已知的客卖方向汇率
    - buy_rate (float): 已知的客买方向汇率
    - X, Y, Z, X1, Y1, Z1: 浮动比例

    返回:
    - target_ASK_rate (float): 反推出的客买方向目标汇率
    - target_BID_rate (float): 反推出的客卖方向目标汇率
    """

    # 确保分母不为零
    if (1 + X / 100) * (1 + Y / 100) * (1 + Z / 100) == 0 or (1 - X1 / 100) * (1 - Y1 / 100) * (1 - Z1 / 100) == 0:
        raise ValueError("浮动比例导致分母为零，无法计算。")

    # 反推客买方向目标汇率
    target_ASK_rate = buy_rate / ((1 + X / 100) * (1 + Y / 100) * (1 + Z / 100))
    print(f"反推的客买-方向目标汇率：{target_ASK_rate}")

    # 反推客卖方向目标汇率
    target_BID_rate = sell_rate / ((1 - X1 / 100) * (1 - Y1 / 100) * (1 - Z1 / 100))
    print(f"反推的客卖-方向目标汇率：{target_BID_rate}")

    return target_ASK_rate, target_BID_rate


# 示例用法
if __name__ == "__main__":
    # 目标汇率
    print("百分比浮动")
    calculate_exchange_rates(target_ASK_rate=2058.880000, X=2, Y=-1, Z=0.85,
                             target_BID_rate=2058.980000, X1=-1.23, Y1=0, Z1=-1.45)
#     BP
    print("BP浮动")
    calculate_BP_rates(target_ASK_rate=728.2248,  X=-100, Y=-10, Z=90,
                       target_BID_rate=728.1248, X1=300, Y1=-10, Z1=-110)
