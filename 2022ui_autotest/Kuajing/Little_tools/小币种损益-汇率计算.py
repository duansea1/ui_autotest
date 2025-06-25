"""
@Author    : duansea
@Date      : 2025/6/13 09:11
@Description: [文件功能的简要描述]
"""


def calculate_third_party_rate(channels, direction):
    """
    计算第三方汇率，并根据交易方向应用浮动比例

    :param channels: dict, 包含各个渠道的信息，每个渠道有出款金额、基础汇率和浮动比例，
                     例如：
                     {
                         "A": {"amount": 100, "rate": 7.25, "rate_float": 0.02},
                         "B": {"amount": 100, "rate": 7.25, "rate_float": 0.02}
                     }
    :param direction: str, 交易方向："买入" 或 "卖出"
    :return: float, 第三方汇率（保留4位小数）
    """

    total_amount = 0
    weighted_sum = 0.0
    calculation_steps = []

    if direction == "买入":
        direction_msg = "买入(针对第一个货币对)-如USD/CNH-购汇方向--bid"
    elif direction == "卖出":
        direction_msg = "卖出-如USD/CNH-结汇方向--bid"

    print(f"=★★★★★★★★★★★★★★★★★★★★======{direction_msg}=====★★★★★★★★★★★★★★★★★★★★==\n")

    for channel, info in channels.items():
        amount = info['amount']
        base_rate = info['rate']
        rate_float = info.get('rate_float', 0)  # 默认为0%

        # 根据方向调整实际使用的汇率
        if direction == "买入":
            chan_rate = base_rate * (1 + rate_float)

        elif direction == "卖出":
            chan_rate = base_rate * (1 - rate_float)

        else:
            raise ValueError("交易方向必须为“买入”或“卖出”。")

        contribution = chan_rate * amount
        weighted_sum += contribution
        total_amount += amount

        # 打印每个渠道的调整后汇率和贡献值

        print(f"渠道 {channel}: 原始汇率={base_rate:.6f}, 浮动={rate_float * 100:.2f}%, 实际使用汇率={chan_rate:.6f}")
        calculation_steps.append(f"({chan_rate:.6f} × {amount})")

    if total_amount == 0:
        raise ValueError("总出款金额为0，无法计算第三方汇率。")

    third_party_rate = weighted_sum / total_amount

    # 输出公式过程
    detailed_formula = " + ".join(calculation_steps)
    full_formula = f"第三方汇率 = ({detailed_formula}) / {total_amount}"

    print(full_formula)
    print(f"🚀第三方汇率 = {third_party_rate:.6f}")

    return round(third_party_rate, 6)


def calculate_profit_loss(sell_amount, buy_amount, third_party_rate, ccy_pair, direction):
    """
    计算销售损益并打印详细日志

    :param sell_amount: float, 卖出金额
    :param buy_amount: float, 买入金额
    :param third_party_rate: float, 第三方汇率
    :param ccy_pair: str, 币种对，如 "USD/KRW"
    :param direction: str, 交易方向："买入" 或 "卖出"
    :return: float, 销售损益（保留两位小数）
    """

    # 标准化币种对格式
    ccy_pair_upper = ccy_pair.upper().replace(" ", "").replace("\\", "/")
    is_usdkrw = ccy_pair_upper in ["USDKRW", "USD/KRW"]

    # 打印交易信息头部
    print("=" * 60)
    print(f"【{'韩元特殊处理' if is_usdkrw else '普通币种'}】")
    print(f"货币对: {ccy_pair_upper}")
    print(f"交易方向: {direction}")
    print(f"卖出金额: {sell_amount:.4f}")
    print(f"买入金额: {buy_amount:.4f}")
    print(f"第三方汇率: {third_party_rate:.6f}")
    print("-" * 60)

    # 计算逻辑
    if direction == "买入":
        if is_usdkrw:
            profit_loss = buy_amount - (sell_amount * 100 / third_party_rate)
            formula = f"USD/KRW 特殊处理:-销售损益 = {buy_amount} - ({sell_amount} × 100 / {third_party_rate:.6f})"
        else:
            profit_loss = (sell_amount * 100 / third_party_rate) - buy_amount
            formula = f"普通小币种-销售损益 = ({sell_amount} × 100 / {third_party_rate:.6f}) - {buy_amount}"

    elif direction == "卖出":
        profit_loss = sell_amount - (buy_amount * 100 / third_party_rate)
        formula = f"普通小币种-销售损益 = {sell_amount} - ({buy_amount} × 100 / {third_party_rate:.6f})"

    else:
        raise ValueError("交易方向必须为“买入”或“卖出”。")

    # 打印计算过程和结果
    print(formula)
    print(f"🚀🚀🚀🚀销售损益 = {profit_loss:.4f}")
    print("=" * 60 + "\n")

    return round(profit_loss, 4)



if __name__ == '__main__':

    # 计算电商渠道的第三方汇率
    channels1 = {
        "A_37": {"amount": 188000.0 , "rate":5641.500000, "rate_float": round(0/100,4)},   # 37qudao
        "B_77": {"amount": 99000.00, "rate":5631.450, "rate_float": round(2/100,4)}
    }
    channels1 = {
        "A_37": {"amount": 136702.00, "rate": 136250.000, "rate_float": round(0.3 / 100, 4)},  # KRW

    }
    channels = {
        "A_37": {"amount":45174500.0, "rate":136906.444, "rate_float": round(0 / 100, 4)},  # 2506161113001217108

    }
    print("电商渠道的第三方汇率：")
    third_party_rate =calculate_third_party_rate(channels,direction="买入")



    #  # # 计算销售损益
    calculate_profit_loss(
        ccy_pair="USD/PHP",
        direction="买入",
        sell_amount=45174500.0 ,
        buy_amount=33282.23,
        third_party_rate=third_party_rate,
    )

    # calculate_profit_loss(
    #     ccy_pair="USD/KRW",
    #     direction="卖出",
    #     sell_amount=10000,
    #     buy_amount= 13682900.00  ,
    #     third_party_rate=third_party_rate,
    # )

    # calculate_profit_loss(
    #     ccy_pair="USD/KRW",
    #     direction="买入",
    #     sell_amount=136702.00,
    #     buy_amount=100.26,
    #     third_party_rate=third_party_rate,
    # )