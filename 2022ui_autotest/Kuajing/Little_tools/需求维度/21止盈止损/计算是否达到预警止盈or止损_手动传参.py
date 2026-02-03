import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_profit_loss_threshold(trader_profit_loss, profit_loss_currency, trade_amount, 
                                 # 止盈参数配置
                                 profit_type, profit_value, 
                                 # 止损参数配置
                                 loss_type, loss_value,
                                 # 固定汇率专用参数
                                 direction=None, currency_pair=None, channel_rate=None):
    """
    检查是否达到止盈或止损阈值
    
    参数:
    trader_profit_loss: float, 预计交易员损益（汇总）
    
    profit_loss_currency: str, 损益币种
    trade_amount: float, 买入或卖出金额（与损益币种一致）
    
    # 止盈参数配置
    profit_type: str, 止盈阈值类型 ('percentage' 百分比, 'fixed_amount' 固定金额, 'fixed_rate' 固定汇率)
    profit_value: float, 止盈阈值数值
    
    # 止损参数配置
    loss_type: str, 止损阈值类型 ('percentage' 百分比, 'fixed_amount' 固定金额, 'fixed_rate' 固定汇率)
    loss_value: float, 止损阈值数值
    
    # 固定汇率专用参数（仅当profit_type或loss_type为'fixed_rate'时需要）
    direction: str, 交易方向 ('buy' 买入, 'sell' 卖出)
    currency_pair: str, 货币对 (如 'USD/CNH')
    channel_rate: float, 渠道实时汇率
    
    返回:
    tuple: (是否触发止盈, 是否触发止损)
    """
    # 初始化结果
    profit_triggered = False
    loss_triggered = False
    
    # 止盈判断
    profit_reason = ""
    # 固定汇率类型：直接根据汇率判断，不需要考虑交易员收益
    if profit_type == 'fixed_rate':
        # 固定汇率止盈：根据不同方向判断汇率是否更优或一样
        # 买入方向：渠道汇率低于固定汇率，渠道汇率优
        # 卖出方向：渠道汇率高于固定汇率，渠道汇率优
        if direction and currency_pair and channel_rate is not None:
            if direction == 'buy':
                # 买入方向：渠道汇率 < 固定汇率 → 汇率更优
                if channel_rate <= profit_value:
                    profit_triggered = True
                    profit_reason = f"固定汇率止盈：{currency_pair} 买入方向，渠道汇率{channel_rate} <= 止盈阈值{profit_value}，汇率更优或一样"
                else:
                    profit_triggered = False
                    profit_reason = f"固定汇率止盈：{currency_pair} 买入方向，渠道汇率{channel_rate} > 止盈阈值{profit_value}，汇率更差"
            elif direction == 'sell':
                # 卖出方向：渠道汇率 > 固定汇率 → 汇率更优
                if channel_rate >= profit_value:
                    profit_triggered = True
                    profit_reason = f"固定汇率止盈：{currency_pair} 卖出方向，渠道汇率{channel_rate} >= 止盈阈值{profit_value}，汇率更优或一样"
                else:
                    profit_triggered = False
                    profit_reason = f"固定汇率止盈：{currency_pair} 卖出方向，渠道汇率{channel_rate} < 止盈阈值{profit_value}，汇率更差"
            else:
                profit_reason = f"固定汇率止盈：无效的交易方向{direction}"
        else:
            profit_reason = "固定汇率止盈：缺少必要参数（direction、currency_pair或channel_rate）"
    # 非固定汇率类型：需要考虑交易员收益为正
    elif trader_profit_loss > 0:
        if profit_type == 'percentage':
            # 百分比止盈：(损益/交易金额)*100% >= 止盈阈值
            calculation_result = (trader_profit_loss / trade_amount) * 100
            if calculation_result >= profit_value:
                profit_triggered = True
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，(预计交易员损益/交易金额)*100% = {calculation_result:.2f}% >= 止盈阈值{profit_value}%"
            else:
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，(预计交易员损益/交易金额)*100% = {calculation_result:.2f}% < 止盈阈值{profit_value}%"
        elif profit_type == 'fixed_amount':
            # 固定金额止盈：损益 >= 止盈阈值
            if trader_profit_loss >= profit_value:
                profit_triggered = True
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，预计交易员损益 >= 止盈阈值{profit_value}"
            else:
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，预计交易员损益 < 止盈阈值{profit_value}"
    else:
        profit_reason = f"预计交易员损益({trader_profit_loss})不为正数，不触发止盈"
    
    # 止损判断
    loss_reason = ""
    # 固定汇率类型：直接根据汇率判断，不需要考虑交易员收益
    if loss_type == 'fixed_rate':
        # 固定汇率止损：根据不同方向判断汇率是否更差或一样
        # 买入方向：渠道汇率高于固定汇率，渠道汇率差
        # 卖出方向：渠道汇率低于固定汇率，渠道汇率差
        if direction and currency_pair and channel_rate is not None:
            if direction == 'buy':
                # 买入方向：渠道汇率 > 固定汇率 → 汇率更差
                if channel_rate >= loss_value:
                    loss_triggered = True
                    loss_reason = f"固定汇率止损：{currency_pair} 买入方向，渠道汇率{channel_rate} >= 止损阈值{loss_value}，汇率更差或一样"
                else:
                    loss_triggered = False
                    loss_reason = f"固定汇率止损：{currency_pair} 买入方向，渠道汇率{channel_rate} < 止损阈值{loss_value}，汇率更优"
            elif direction == 'sell':
                # 卖出方向：渠道汇率 < 固定汇率 → 汇率更差
                if channel_rate <= loss_value:
                    loss_triggered = True
                    loss_reason = f"固定汇率止损：{currency_pair} 卖出方向，渠道汇率{channel_rate} <= 止损阈值{loss_value}，汇率更差或一样"
                else:
                    loss_triggered = False
                    loss_reason = f"固定汇率止损：{currency_pair} 卖出方向，渠道汇率{channel_rate} > 止损阈值{loss_value}，汇率更优"
            else:
                loss_reason = f"固定汇率止损：无效的交易方向{direction}"
        else:
            loss_reason = "固定汇率止损：缺少必要参数（direction、currency_pair或channel_rate）"
    # 非固定汇率类型：需要考虑交易员收益为负
    elif trader_profit_loss < 0:
        abs_profit_loss = abs(trader_profit_loss)
        if loss_type == 'percentage':
            # 百分比止损：(损益绝对值/交易金额)*100% >= 止损阈值
            calculation_result = (abs_profit_loss / trade_amount) * 100
            if calculation_result >= loss_value:
                loss_triggered = True
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，(预计交易员损益绝对值/交易金额)*100% = {calculation_result:.2f}% >= 止损阈值{loss_value}%"
            else:
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，(预计交易员损益绝对值/交易金额)*100% = {calculation_result:.2f}% < 止损阈值{loss_value}%"
        elif loss_type == 'fixed_amount':
            # 固定金额止损：损益绝对值 >= 止损阈值
            if abs_profit_loss >= loss_value:
                loss_triggered = True
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，预计交易员损益绝对值({abs_profit_loss}) >= 止损阈值{loss_value}"
            else:
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，预计交易员损益绝对值({abs_profit_loss}) < 止损阈值{loss_value}"
    else:
        loss_reason = f"预计交易员损益({trader_profit_loss})不为负数，不触发止损"
    
    # 打印日志
    logging.info(f"交易员损益: {trader_profit_loss}, 损益币种: {profit_loss_currency}, 交易金额: {trade_amount}")
    logging.info(f"交易方向: {direction}, 货币对: {currency_pair}, 渠道汇率: {channel_rate}")
    logging.info(f"止盈配置: 类型={profit_type}, 阈值={profit_value}")
    logging.info(f"止损配置: 类型={loss_type}, 阈值={loss_value}")
    logging.info(f"📊止盈判断: {profit_reason}")
    logging.info(f"📉止损判断: {loss_reason}")
    logging.info(f"🚀止盈: {'触发' if profit_triggered else '不触发'}, 🚀止损: {'触发' if loss_triggered else '不触发'}")
    
    # 打印结果
    print(f"结果：止盈={'触发' if profit_triggered else '不触发'}, 止损={'触发' if loss_triggered else '不触发'}\n")
    
    return profit_triggered, loss_triggered

# 示例使用
if __name__ == "__main__":
    # 函数参数说明：
    # check_profit_loss_threshold(
    #     trader_profit_loss,    # 预计交易员损益
    #     profit_loss_currency,  # 损益币种
    #     trade_amount,          # 交易金额
    #     profit_type,           # 止盈类型：'percentage'/'fixed_amount'/'fixed_rate'
    #     profit_value,          # 止盈阈值
    #     loss_type,             # 止损类型：'percentage'/'fixed_amount'/'fixed_rate'
    #     loss_value,            # 止损阈值
    #     direction=None,        # 交易方向：'buy'/'sell'（固定汇率时必填）
    #     currency_pair=None,    # 货币对：如 'USD/CNH'（固定汇率时必填）
    #     channel_rate=None      # 渠道汇率（固定汇率时必填）
    # )
    
    # 示例1：百分比止盈（触发），百分比止损（不触发）- 收益为正
    print("=== 示例1：百分比止盈（触发），百分比止损（不触发）- 收益为正 ===")
    check_profit_loss_threshold(
        trader_profit_loss=1500,        # 交易员收益1500
        profit_loss_currency="USD",     # 损益币种USD
        trade_amount=10000,              # 交易金额10000
        profit_type="percentage",       # 止盈类型：百分比
        profit_value=10,                 # 止盈阈值：10%
        loss_type="percentage",         # 止损类型：百分比
        loss_value=5                     # 止损阈值：5%
    )

    