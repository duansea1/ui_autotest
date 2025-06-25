


direction_result = 1  # 买入方向
buyCcy = "USD"
sellCcy = "CNH"
buyAmount_result = 10000
sellAmount_result = 10000
tradeRate_result = 6.88


if direction_result == 1:  # 买入方向
    if buyCcy == "USD" and sellCcy == "CNH":  # USD/CNH: 卖CNH -> 买USD
        temp_result = buyAmount_result * tradeRate_result
    elif buyCcy == "CNH" and sellCcy == "USD":  # CNH/USD: 卖USD -> 买CNH
        temp_result = buyAmount_result / tradeRate_result
    else:
        msg = u"买入方向：不支持的币种对 {} -> {}".format(sellCcy, buyCcy)
        AssertionResult.setFailureMessage(msg)
        AssertionResult.setFailure(True)
        temp_result = None
elif direction_result == 2:  # 卖出方向
    if buyCcy == "USD" and sellCcy == "CNH":  # USD/CNH: 卖USD -> 买CNH
        temp_result = sellAmount_result / tradeRate_result
    elif buyCcy == "CNH" and sellCcy == "USD":  # CNH/USD: 卖CNH -> 买USD
        temp_result = sellAmount_result * tradeRate_result