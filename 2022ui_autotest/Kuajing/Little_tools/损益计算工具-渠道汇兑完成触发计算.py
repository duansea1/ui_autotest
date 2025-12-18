"""

1.	渠道成交订单判断。客户明细为 “买入方向”&“生成渠道订单，以源币种为固定金额” 例如USDCNH
If手续费内扣，汇兑损益(in目标币种)：（买入金额）*（客户汇率/100-渠道汇率）
If手续费外扣，汇兑损益(in目标币种)：买入金额*（客户汇率/100-渠道汇率）

2.	渠道成交订单判断。客户明细为 “买入方向”&“生成渠道订单，以目标币种为固定金额” 例如USDVND
If手续费内扣，汇兑损益(in 源币种)：（卖出金额-0）*（1/渠道汇率-100/客户汇率）
If手续费外扣，汇兑损益(in 源币种)：卖出金额 *（1/渠道汇率-100/客户汇率）

3.	渠道成交订单判断。客户明细为 “卖出方向”&“生成渠道订单，以源币种为固定金额”
if手续费内扣，汇兑损益(in 目标币种)：(卖出金额-手续费金额）*（渠道汇率-客户汇率/100）
if手续费外扣，汇兑损益(in 目标币种)：卖出金额*（渠道汇率-客户汇率/100）

4.	渠道成交订单判断。客户明细为 “卖出方向”&“生成渠道订单，以目标币种为固定金额”
汇兑损益(in 源币种)：(买入金额-手续费金额）*（100/客户汇率-1/渠道汇率）

5.	渠道成交订单判断。客户明细为双向，且损益计算方法为“成本还原法”
买入订单损益=（买入金额）*（客户汇率/100-渠道成交汇率）
卖出订单损益= (卖出金额）*（渠道成交汇率-客户汇率/100）
总损益-买入订单损益-卖出订单损益=轧差损益
买入订单逐笔损益=买入订单损益+加权平均轧差损益
卖出订单逐笔损益=卖出订单损益+加权平均轧差损益

6.	渠道成交订单判断。客户明细为双向，且损益计算方法为“加权平均法” 。详见附件GBP.xlsx
买入订单以卖出金额计算权数
卖出订单以买入金额计算权数
总损益*权数=逐笔损益



交易方向为买入，收益币种为左边币种，则销售收益为：卖出金额*100/第三方汇率-买入金额；交易员损益为：收益-销售收益
交易方向为买入，收益币种为右边币种，则销售收益为：卖出金额-买入金额*第三方汇率/100；交易员损益为：收益-销售收益
交易方向为卖出，收益币种为左边币种，则销售收益为：卖出金额-买入金额*100/第三方汇率；交易员损益为：收益-销售收益
交易方向为卖出，收益币种为右边币种，则销售收益为：卖出金额*第三方汇率/100-买入金额；交易员损益为：收益-销售收益
以下特殊情况，损益计算公式：
关联类型交易类型为取消交易或GEP分发渠道兑换：交易员损益=0，销售收益=收益
第三方汇率为空：，交易员损益=0，销售收益=收益
货币对USDCNH，第三方汇率数值不在650-750之间：销售收益为0，交易员损益=收益

涉及菜单：
汇率管理-交易管理-用户兑换凭证，导出增加销售收益、交易员损益字段。
汇率管理-渠道兑换订单明细，里面增加销售收益、交易员损益字段。

"""


def calculate_forex_profits(
        buy_amount: float,
        sell_amount: float,
        customer_rate: float,
        channel_rate: float,
        third_party_rate: float,
        direction: str,  # '买入' 或 '卖出'
        fee: float = 0,
        is_internal_fee: bool = True
) -> dict:
    """
    外汇交易损益计算（方向敏感版）
    参数说明：
    - direction: 明确指定当前计算方向（'买入'/'卖出'）
    - 其他参数与原函数一致
    """
    # 汇率单位转换
    effective_customer_rate = customer_rate / 100  # 目标币种/源币种
    effective_third_rate = third_party_rate / 100

    # 方向校验
    direction = direction.strip()
    assert direction in ('买入', '卖出'), "方向参数必须为'买入'或'卖出'"

    results = {}

    # ========== 总损益计算 ==========
    if direction == '买入':
        # 场景1：源币种固定
        profit_source = buy_amount * (effective_customer_rate - channel_rate)
        # 场景2：目标币种固定
        profit_target = (sell_amount - fee if is_internal_fee else sell_amount) * \
                        (1 / channel_rate - 1 / effective_customer_rate)
        total_profit = {'1.渠道成交订单判断。客户明细为 “买入方向”&“生成渠道订单，以源币种（右边）为固定金额源币种固定': profit_source, '2.渠道成交订单判断。客户明细为 “买入方向”&“生成渠道订单，以目标币种(左边)固定': profit_target}
    else:
        # 场景3：源币种固定
        profit_source = (sell_amount - fee if is_internal_fee else sell_amount) * \
                        (channel_rate - effective_customer_rate)
        # 场景4：目标币种固定
        profit_target = (buy_amount - fee) * (1 / effective_customer_rate - 1 / channel_rate)
        total_profit = {'3.渠道成交订单判断。客户明细为 “卖出方向”&“生成渠道订单，以源币种（右边）为固定金额源币种固定': profit_source, '4.渠道成交订单判断。客户明细为 “卖出方向”&“生成渠道订单，以目标币种(左边)固定': profit_target}

    results['总损益'] = total_profit

    # ========== 销售损益计算 ==========
    if direction == '买入':
        sales_profit = {
            '交易方向为买入，收益币种为 左边币种收益': sell_amount / effective_third_rate - buy_amount,
            '交易方向为买入，收益币种为 右边币种收益': sell_amount - buy_amount * effective_third_rate
        }
    else:
        sales_profit = {
            '交易方向为卖出，收益币种为 左边币种收益': sell_amount - buy_amount / effective_third_rate,
            '交易方向为卖出，收益币种为 右边币种收益': sell_amount * effective_third_rate - buy_amount
        }

    results['销售损益'] = sales_profit
    return results


def format_directional_results(results: dict, direction: str) -> str:
    """格式化方向明确的输出"""
    output = [f"\n===== {direction}方向计算结果 ====="]

    # 总损益输出
    output.append("\n 【总损益】")
    for scenario, value in results['总损益'].items():
        output.append(f"{scenario}:  {value:.3f}")

    # 销售损益输出
    output.append("\n 【销售损益】")
    for scenario, value in results['销售损益'].items():
        output.append(f"{scenario}:  {value:.3f}")

    return '\n'.join(output)


if __name__ == "__main__":
    # 测试数据（保持不变）
    params = {
        'sell_amount': 13.88,  # 卖出金额
        'buy_amount': 53.00 ,  # 买入金额

        'customer_rate': 371.1816,  # 用户汇率
        'channel_rate': 372.181500,   # 渠道汇率
        'third_party_rate': 360.465970,    # 第三方汇率
        'fee': 0,
        'is_internal_fee': True
    }

    # 分别计算买卖方向
    buy_results = calculate_forex_profits(direction='买入', **params)
    print(format_directional_results(buy_results, '买入'))

    sell_results = calculate_forex_profits(direction='卖出', **params)
    print(format_directional_results(sell_results, '卖出'))

    # 打印结果



    # # 验证关键计算（买入方向-右边币种）
    # manual_check = 419.64 - 50 * 8.41
    # print(f"\n验证买入方向右边币种销售损益: {manual_check:.2f} (理论值应≈-0.86)")