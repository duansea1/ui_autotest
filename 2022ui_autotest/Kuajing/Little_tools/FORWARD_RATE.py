"""forward_rate.py: 计算给定交割日的Forward报价"""

from datetime import date


def calculate_forward_quote(one_d_forward, one_w_forward, one_d_settlement_date, one_w_settlement_date,
                            target_settlement_date):
    """
    计算给定交割日的Forward报价。
    如交割日在1W-2W之间，对应交割日的Forward报价：（2w forward-1w forward）/（2w交割日期-1w交割日期）* （交割日-1w 交割日）+1w forward
    参数:
    - one_d_forward: 1天远期报价 (float)
    - one_w_forward: 1周远期报价 (float)
    - one_d_settlement_date: 1天交割日期 (datetime.date)
    - one_w_settlement_date: 1周交割日期 (datetime.date)
    - target_settlement_date: 目标交割日期 (datetime.date)

    返回:
    - 对应交割日的Forward报价 (float)
    """
    # 计算两个交割日之间的差异（以天为单位）
    days_diff = (one_w_settlement_date - one_d_settlement_date).days

    # 计算目标交割日与1天交割日之间的差异（以天为单位）
    target_days_diff = (target_settlement_date - one_d_settlement_date).days

    # 根据提供的公式计算报价
    forward_quote =  ((one_w_forward - one_d_forward) / days_diff) * target_days_diff + one_d_forward


    return forward_quote


# 示例使用
if __name__ == '__main__':
    # 假设的远期报价和交割日期
    one_d_forward = 	1957.1977
    one_w_forward = 1957.1937
    one_d_settlement_date = date(2025, 4, 20)  # 例如：2025-3-22作为1D交割日--
    one_w_settlement_date = date(2025, 4, 27)  # 例如：2025-3-28作为1W交割日
    target_settlement_date = date(2025, 4, 26)  # 目标交割日期

    # 计算并打印结果
    quote = calculate_forward_quote(one_d_forward, one_w_forward, one_d_settlement_date, one_w_settlement_date,
                                    target_settlement_date)
    print(f"目标交割日({target_settlement_date})的Forward报价为: {quote}")