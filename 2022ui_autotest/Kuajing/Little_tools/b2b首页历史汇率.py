import pymysql
import pandas as pd
from decimal import Decimal
"""
需求：KJ-9732 B2B首页汇率波动曲线接口优化
"""


def adjust_fx_rates(df, ask_float, bid_float, bp_type="bp"):
    """
    根据给定的浮动类型和浮动值调整汇率。

    参数:
        df: 原始汇率数据 DataFrame。
        ask_float: 卖出价浮动（购汇）。
        bid_float: 买入价浮动（结汇）。
        bp_type: "bp"（基点）或 "bb"（百分比），默认 "bp"。

    返回:
        调整后的 DataFrame。
    """
    df['guanwBuyRate_结汇USDCNH'] = df['guanwBuyRate_结汇USDCNH'].astype(float)
    df['guanwSellRate_购汇CNHUSD'] = df['guanwSellRate_购汇CNHUSD'].astype(float)

    if bp_type == "bp":
        df['guanwBuyRate_结汇USDCNH'] -= bid_float / 10000
        df['guanwSellRate_购汇CNHUSD'] = round(100 / (df['guanwSellRate_购汇CNHUSD'] + ask_float / 100), 6)
    elif bp_type == "bb":
        df['guanwBuyRate_结汇USDCNH'] *= (1 - bid_float / 100)
        df['guanwSellRate_购汇CNHUSD'] *= (1 + ask_float / 100)
        df['guanwSellRate_购汇CNHUSD'] = df['guanwSellRate_购汇CNHUSD'].apply(lambda x: 100 / float(x))
    else:
        raise ValueError("bp_type must be 'bp' or 'bb'")

    return df[['buyCreateTime', 'sellCreateTime', 'channelId', 'buyRate', 'sellRate',
               'guanwBuyRate_结汇USDCNH', 'guanwSellRate_购汇CNHUSD']]


def fetch_fx_data(channel_id=1200923069, source_ccy='USD', dest_ccy='JPY',
                  start_time='2025-06-03 00:00:00', end_time='2025-06-03 23:59:59'):
    """
    连接数据库并获取指定条件下的汇率数据。

    返回:
        原始 DataFrame。
    """
    conn = pymysql.connect(
        host='10.0.19.156',
        port=9030,
        user='bf_hpt',
        password='bf_hpt',
        database='BAOFU_CGW',
        charset='utf8mb4'
    )

    try:
        sql = f"""
        WITH hourly_data AS (
            SELECT *, DATE_FORMAT(create_time, '%Y-%m-%d %H:00:00') AS hour_point,
                   ABS(TIMESTAMPDIFF(SECOND, create_time, DATE_FORMAT(create_time, '%Y-%m-%d %H:00:00'))) AS diff_seconds
            FROM BAOFU_CGW.T_TOPIC_BAOFU_CGW_CHANNEL_RATE
            WHERE channelId = {channel_id}
              AND sourceCcy = '{source_ccy}'
              AND destCcy = '{dest_ccy}'
              AND create_time >= '{start_time}'
              AND create_time < '{end_time}'
              AND tradeRate > 0
              AND discountRate > 0
              AND closingType IN ('TOD')
        ),
        buy_sell_data AS (
            SELECT h.*, ROW_NUMBER() OVER (PARTITION BY h.hour_point, h.tradeDirection ORDER BY h.diff_seconds ASC) AS rn
            FROM hourly_data h
        )
        SELECT 
            b.create_time AS buyCreateTime,
            s.create_time AS sellCreateTime,
            b.channelId,
            CASE WHEN b.destCcy = 'CNY' THEN '在岸牌价' ELSE '离岸牌价' END AS rateType,
            b.discountRate AS buyRate,
            s.discountRate AS sellRate,
            b.closingType,
            b.tradeRate AS guanwBuyRate_结汇USDCNH,
            s.tradeRate AS guanwSellRate_购汇CNHUSD
        FROM 
            (SELECT * FROM buy_sell_data WHERE tradeDirection = 1 AND rn = 2) b
        JOIN 
            (SELECT * FROM buy_sell_data WHERE tradeDirection = 2 AND rn = 2) s
        ON 
            b.hour_point = s.hour_point
            AND b.channelId = s.channelId
            AND b.sourceCcy = s.sourceCcy
            AND b.destCcy = s.destCcy
            AND b.closingType = s.closingType
        ORDER BY b.create_time DESC;
        """

        df = pd.read_sql(sql, conn)
        return df

    finally:
        conn.close()


def main():
    """
    主程序：提取数据、调整汇率并输出。
    """
    # 参数设置（可自定义）
    ask_float = 2      # 卖出浮动（购汇）
    bid_float = 1      # 买入浮动（结汇）
    bp_type = "bb"     # 调整方式：'bp' 或 'bb'-百分比计算

    df = fetch_fx_data(channel_id=1200923069, source_ccy='USD', dest_ccy='JPY',
                  start_time='2025-06-03 00:00:00', end_time='2025-06-03 23:59:59')

    adjusted_df = adjust_fx_rates(df, ask_float, bid_float, bp_type)
    print(adjusted_df.to_string(index=False))


if __name__ == '__main__':
    main()
