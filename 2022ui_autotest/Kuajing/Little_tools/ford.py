# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2025-01-10 16:34
# ---
def calculate_forward_bid(spot_bid, swap_bid):
    """
    计算 forward bid。

    参数:
    - spot_bid: 现货报价 (float)
    - swap_bid: 掉期报价 (float)

    返回:
    - forward bid 的计算结果 (float)
    """
    return spot_bid + swap_bid / 10000


def calculate_spot_bid(forward_bid, swap_bid):
    """
    根据 forward bid 和 swap bid 反推 spot bid。

    参数:
    - forward_bid: 远期报价 (float)
    - swap_bid: 掉期报价 (float)

    返回:
    - spot bid 的计算结果 (float)
    """
    return forward_bid - swap_bid / 10000


# 示例用法：
if __name__ == "__main__":
    # 已知数据点
    spot_bid_example = 735.3700   #
    swap_bid_example = -59.72

    spot_ask_example = 735.16
    swap_ask_example = -62


    forward_bid_result = calculate_forward_bid(spot_bid_example, swap_bid_example)
    print(f"计算-Forward bid: {forward_bid_result}")

    forward_ask_result = calculate_forward_bid(spot_ask_example, swap_ask_example)
    print(f"计算的--Forward ask: {forward_ask_result}")

    # # 使用 forward bid 和 swap bid 反推 spot bid
    # recalculated_spot_bid = calculate_spot_bid(735.219442, -5.58)
    # print(f"原始的spot汇率: {recalculated_spot_bid}")