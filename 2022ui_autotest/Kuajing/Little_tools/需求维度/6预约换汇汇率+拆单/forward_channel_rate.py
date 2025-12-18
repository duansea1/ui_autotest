"""
@Author    : duansea
@Date      : 2025/8/5 09:56
@Description: [文件功能的简要描述]
"""
from decimal import Decimal

# 参数从 channel_center服务的日志中获取
# tail -f fat-baofu-channel-center.log | grep -3 -E "dateList=|渠道掉期点接口|HceRateBatchQuery|HceChannelRateQuery|hce批量rate返回, 结果"
data = [{"date":"20250806","symbol":"EUR/CNH","side":"sell","price":"8.2892","message":""},{"date":"20250806","symbol":"EUR/CNH","side":"buy","price":"8.3165","message":""},{"date":"20250907","symbol":"EUR/CNH","side":"sell","price":"8.2783","message":""},{"date":"20250907","symbol":"EUR/CNH","side":"buy","price":"8.3227","message":""},{"date":"20250807","symbol":"EUR/CNH","side":"sell","price":"8.2898","message":""},{"date":"20250807","symbol":"EUR/CNH","side":"buy","price":"8.3160","message":""},{"date":"20250805","symbol":"EUR/CNH","side":"sell","price":"8.2844","message":""},{"date":"20250805","symbol":"EUR/CNH","side":"buy","price":"8.3216","message":""}]
 # 存储每个日期的买卖价格
dates_prices = {}

for record in data:
    date = record['date']
    price = Decimal(record['price'])  # 使用 Decimal 精确表示
    scaled_price = price * 100       # 乘以 100

    if date not in dates_prices:
        dates_prices[date] = {'sell': None, 'buy': None}

    if record['side'] == 'sell':
        dates_prices[date]['sell'] = scaled_price
    elif record['side'] == 'buy':
        dates_prices[date]['buy'] = scaled_price

# 按日期排序并输出
for date in sorted(dates_prices.keys()):
    sell_price = dates_prices[date]['sell']
    buy_price = dates_prices[date]['buy']
    print(f"{date[:4]}年{date[4:6]}月{date[6:]}日： sellprice（BID 客卖）： {sell_price:.2f} ： buyprice（ASK 客买）： {buy_price:.2f}")