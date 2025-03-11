from datetime import datetime

def calculate_swap_point(delivery_date_str, d1_delivery_date_str, w1_delivery_date_str, d1_swap, w1_swap):
    """
    计算交割日在1D到1W之间的掉期点。

    参数:
    delivery_date_str (str): 目标交割日（格式为 'YYYY-MM-DD'）。
    d1_delivery_date_str (str): 1D交割日（格式为 'YYYY-MM-DD'）。
    w1_delivery_date_str (str): 1W交割日（格式为 'YYYY-MM-DD'）。
    d1_swap (float): 1D掉期点。
    w1_swap (float): 1W掉期点。

    返回:
    float: 目标交割日对应的掉期点。
    """
    # 将日期字符串转换为datetime对象
    delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d')
    d1_delivery_date = datetime.strptime(d1_delivery_date_str, '%Y-%m-%d')
    w1_delivery_date = datetime.strptime(w1_delivery_date_str, '%Y-%m-%d')

    # 检查输入有效性
    if not (d1_delivery_date <= delivery_date <= w1_delivery_date):
        raise ValueError("目标交割日必须在1D交割日和1W交割日之间。")

    # 计算日期差值（以天数为单位）
    delta_w1_d1 = (w1_delivery_date - d1_delivery_date).days
    delta_delivery_d1 = (delivery_date - d1_delivery_date).days

    # 计算掉期点
    swap_point = (
        (w1_swap - d1_swap) / delta_w1_d1 * delta_delivery_d1 + d1_swap
    )
    return swap_point


if __name__ == "__main__":
    # 示例数据
    delivery_date_str = "2025-3-30"  # 目标交割日-查询日期
    d1_delivery_date_str = "2025-3-29"  # 1D交割日
    w1_delivery_date_str = "2025-4-5"  # 1W交割日
    d1_swap = -100.53000  # 1D掉期点
    w1_swap = -151.73000  # 1W掉期点

    # 计算结果
    result = calculate_swap_point(delivery_date_str, d1_delivery_date_str, w1_delivery_date_str, d1_swap, w1_swap)
    print(f"目标交割日 {delivery_date_str} 对应的掉期点为: {result:.8f}")