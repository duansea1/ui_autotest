def calculate_profit_rate(TRADE_DIRECTION, user_rate, sale_rate):
    """
    计算利润率
    
    参数:
    TRADE_DIRECTION: str - 交易方向，取值为'买入'或'卖出'
    user_rate: float - 用户汇率
    sale_rate: float - 销售成本汇率
    
    返回:
    float - 利润率，保留6位小数
    """
    # 验证输入参数
    if TRADE_DIRECTION not in ['买入', '卖出']:
        raise ValueError("TRADE_DIRECTION必须为'买入'或'卖出'")
    
    if sale_rate == 0:
        raise ValueError("销售成本汇率不能为0")
    
    # 根据交易方向计算利润率
    if TRADE_DIRECTION == '卖出':
        # 卖出方向：(销售成本汇率-用户汇率)/销售成本汇率*100%
        print(f"卖出方向计算公式: (销售成本汇率-用户汇率)/销售成本汇率*100%")
        print(f"带入参数: ({sale_rate} - {user_rate}) / {sale_rate} * 100%")
        profit_rate = ((sale_rate - user_rate) / sale_rate) * 100
    else:  # TRADE_DIRECTION == '买入'
        # 买入方向：(用户汇率-销售成本汇率)/销售成本汇率*100%
        print(f"买入方向计算公式: (用户汇率-销售成本汇率)/销售成本汇率*100%")
        print(f"带入参数: ({user_rate} - {sale_rate}) / {sale_rate} * 100%")
        profit_rate = ((user_rate - sale_rate) / sale_rate) * 100
    
    # 保留6位小数
    return round(profit_rate, 6)

def calculate_floating_rate(TRADE_DIRECTION, float_type, rate, float_value):
    """
    计算浮动后的汇率
    
    参数:
    TRADE_DIRECTION: str - 交易方向，取值为'买入'或'卖出'
    float_type: str - 浮动类型，取值为'BP'（基点浮动）或'PC'（百分比浮动）
    rate: float - 渠道汇率
    float_value: float - 浮动值
    
    返回:
    float - 浮动后的新汇率
    """
    # 验证输入参数
    if TRADE_DIRECTION not in ['买入', '卖出']:
        raise ValueError("TRADE_DIRECTION必须为'买入'或'卖出'")
    
    if float_type not in ['BP', 'PC']:
        raise ValueError("float_type必须为'BP'（基点浮动）或'PC'（百分比浮动）")
    
    # 根据交易方向和浮动类型计算新汇率
    if float_type == 'BP':
        # BP浮动计算
        if TRADE_DIRECTION == '买入':
            # 买入方向：渠道汇率 + BP浮动
            new_rate = rate + float_value / 100  # BP转换为小数
            print(f"买入方向 BP浮动计算公式: 渠道汇率 + BP浮动/100")
            print(f"带入参数: {rate} + {float_value}/100 = {new_rate}")
        else:  # TRADE_DIRECTION == '卖出'
            # 卖出方向：渠道汇率 - BP浮动
            new_rate = rate - float_value / 100  # BP转换为小数
            print(f"卖出方向 BP浮动计算公式: 渠道汇率 - BP浮动/100")
            print(f"带入参数: {rate} - {float_value}/100 = {new_rate}")
    else:  # float_type == 'PC'
        # 百分比浮动计算
        if TRADE_DIRECTION == '买入':
            # 买入方向：渠道汇率 × (1 + 浮动百分比)
            new_rate = rate * (1 + float_value / 100)  # 百分比转换为小数
            print(f"买入方向 百分比浮动计算公式: 渠道汇率 × (1 + 浮动百分比/100)")
            print(f"带入参数: {rate} × (1 + {float_value}/100) = {new_rate}")
        else:  # TRADE_DIRECTION == '卖出'
            # 卖出方向：渠道汇率 × (1 - 浮动百分比)
            new_rate = rate * (1 - float_value / 100)  # 百分比转换为小数
            print(f"卖出方向 百分比浮动计算公式: 渠道汇率 × (1 - 浮动百分比/100)")
            print(f"带入参数: {rate} × (1 - {float_value}/100) = {new_rate}")
    
    return new_rate

# 示例用法
if __name__ == "__main__":
    print("====== 利润率计算示例 ======\n")

    # 买入方向示例 计算利润率
    buy_profit = calculate_profit_rate('买入', user_rate=2634400, sale_rate=3125806.2)
    print(f"⏩买入方向利润率: {buy_profit}%\n")

    # 卖出方向示例
    sell_profit = calculate_profit_rate('卖出', user_rate=2633500, sale_rate=2634816.75)
    print(f"⏩卖出方向利润率: {sell_profit}%")
    
    
    
    print("====== 浮动汇率计算示例 ======\n")
    # 买入方向 BP浮动示例
    # print("1. 买入方向 BP浮动示例:")
    # new_rate1 = calculate_floating_rate('买入', 'BP', 91.747000, -55)
    # print(f"⏩浮动后的新汇率: {new_rate1}\n")
    
    # # # 卖出方向 BP浮动示例
    # print("2. 卖出方向 BP浮动示例:")
    # new_rate2 = calculate_floating_rate('卖出', 'BP', 91.411700, -100)
    # print(f"⏩浮动后的新汇率: {new_rate2}\n")
    
    # # 买入方向 百分比浮动示例 
    # print("3. 买入方向 百分比浮动示例:")
    # new_rate3 = calculate_floating_rate('买入', 'PC', 2631830.000000, 1)
    # print(f"⏩浮动后的新汇率: {new_rate3}\n")
    
    # # 卖出方向 百分比浮动示例
    # print("4. 卖出方向 百分比浮动示例:")
    # new_rate4 = calculate_floating_rate('卖出', 'PC', 2609610, 1.11)
    # print(f"⏩浮动后的新汇率: {new_rate4}")