"""FORWARD_RATE_指定币种远期汇率计算.py: 计算指定币种的远期标准期限和不标准期限汇率（基准溢价定价模式）"""

from datetime import date, datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def calculate_bp_float_forward(tod_bid, tod_ask, float_bid_bp, float_ask_bp):
    """
    bp浮动模式计算远期汇率
    远期BID价格(客卖) = TOD BID - 浮动值X / 10000
    远期ASK价格(客买) = TOD ASK + 浮动值X / 10000

    参数:
    - tod_bid: TOD买入价（客卖方向基准）(float)
    - tod_ask: TOD卖出价（客买方向基准）(float)
    - float_bid_bp: BID方向浮动bp值 (float)
    - float_ask_bp: ASK方向浮动bp值 (float)

    返回:
    - (forward_bid, forward_ask): 远期买入价和卖出价 (tuple)
    """
    forward_bid = tod_bid - float_bid_bp / 10000
    forward_ask = tod_ask + float_ask_bp / 10000
    logger.debug(f"  bp浮动计算: BID={tod_bid} - {float_bid_bp}/10000 = {forward_bid:.4f}, "
                 f"ASK={tod_ask} + {float_ask_bp}/10000 = {forward_ask:.4f}")
    return forward_bid, forward_ask


def calculate_percentage_float_forward(tod_bid, tod_ask, float_bid_pct, float_ask_pct):
    """
    百分比浮动模式计算远期汇率
    远期BID价格(客卖) = TOD BID * (1 - X%)
    远期ASK价格(客买) = TOD ASK * (1 + Y%)

    参数:
    - tod_bid: TOD买入价（客卖方向基准）(float)
    - tod_ask: TOD卖出价（客买方向基准）(float)
    - float_bid_pct: BID方向浮动百分比 (float)，如1表示1%
    - float_ask_pct: ASK方向浮动百分比 (float)，如1表示1%

    返回:
    - (forward_bid, forward_ask): 远期买入价和卖出价 (tuple)
    """
    forward_bid = tod_bid * (1 - float_bid_pct / 100)
    forward_ask = tod_ask * (1 + float_ask_pct / 100)
    logger.debug(f"  百分比浮动计算: BID={tod_bid} * (1 - {float_bid_pct}%) = {forward_bid:.4f}, "
                 f"ASK={tod_ask} * (1 + {float_ask_pct}%) = {forward_ask:.4f}")
    return forward_bid, forward_ask


def calculate_standard_forward(tod_bid, tod_ask, float_bid_val, float_ask_val, float_mode="bp"):
    """
    计算单个标准期限的远期汇率

    参数:
    - tod_bid: TOD买入价 (float)
    - tod_ask: TOD卖出价 (float)
    - float_bid_val: BID方向浮动值 (float)
    - float_ask_val: ASK方向浮动值 (float)
    - float_mode: 浮动模式，"bp" 或 "percentage" (str)

    返回:
    - (forward_bid, forward_ask): 远期买入价和卖出价 (tuple)
    """
    if float_mode == "bp":
        return calculate_bp_float_forward(tod_bid, tod_ask, float_bid_val, float_ask_val)
    elif float_mode == "percentage":
        return calculate_percentage_float_forward(tod_bid, tod_ask, float_bid_val, float_ask_val)
    else:
        raise ValueError(f"不支持的浮动模式: {float_mode}，仅支持 'bp' 或 'percentage'")


def find_nearest_standard_tenors(target_date, standard_dates):
    """
    找到目标日期前后最近的两个标准期限（用于插值）
    按日期排序所有标准期限，找到包围目标日期的最近两个标准期限

    参数:
    - target_date: 目标交割日期 (datetime.date)
    - standard_dates: 标准期限日期字典，如 {"1D": date(...), "1W": date(...), ...}

    返回:
    - (tenor1, tenor2, date1, date2): 两个最近的标准期限名称和日期
    """
    # 按日期排序标准期限
    sorted_tenors = sorted(standard_dates.items(), key=lambda x: x[1])

    # 如果目标日期早于最早的标准期限，使用最近两个标准期限外推
    if target_date < sorted_tenors[0][1]:
        logger.warning(f"  目标日期 {target_date} 早于最早标准期限 {sorted_tenors[0][0]}({sorted_tenors[0][1]})，"
                       f"使用 {sorted_tenors[0][0]} 和 {sorted_tenors[1][0]} 外推")
        return sorted_tenors[0][0], sorted_tenors[1][0], sorted_tenors[0][1], sorted_tenors[1][1]

    # 如果目标日期晚于最晚的标准期限，使用最近两个标准期限外推
    if target_date > sorted_tenors[-1][1]:
        logger.warning(f"  目标日期 {target_date} 晚于最晚标准期限 {sorted_tenors[-1][0]}({sorted_tenors[-1][1]})，"
                       f"使用 {sorted_tenors[-2][0]} 和 {sorted_tenors[-1][0]} 外推")
        return sorted_tenors[-2][0], sorted_tenors[-1][0], sorted_tenors[-2][1], sorted_tenors[-1][1]

    # 目标日期在两个标准期限之间，找到最近的两个
    for i in range(len(sorted_tenors) - 1):
        if sorted_tenors[i][1] <= target_date <= sorted_tenors[i + 1][1]:
            return sorted_tenors[i][0], sorted_tenors[i + 1][0], sorted_tenors[i][1], sorted_tenors[i + 1][1]

    # 兜底：返回最后两个
    return sorted_tenors[-2][0], sorted_tenors[-1][0], sorted_tenors[-2][1], sorted_tenors[-1][1]


def calculate_non_standard_forward(forward_bid1, forward_ask1, date1,
                                   forward_bid2, forward_ask2, date2, target_date):
    """
    线性插值法计算不标准期限的远期汇率
    公式：(forward2 - forward1) / (date2 - date1) * (target_date - date1) + forward1

    参数:
    - forward_bid1: 第一个标准期远期买入价 (float)
    - forward_ask1: 第一个标准期远期卖出价 (float)
    - date1: 第一个标准期交割日期 (datetime.date)
    - forward_bid2: 第二个标准期远期买入价 (float)
    - forward_ask2: 第二个标准期远期卖出价 (float)
    - date2: 第二个标准期交割日期 (datetime.date)
    - target_date: 目标交割日期 (datetime.date)

    返回:
    - (forward_bid, forward_ask): 目标交割日的远期买入价和卖出价 (tuple)
    """
    days_diff = (date2 - date1).days
    target_days_diff = (target_date - date1).days

    if days_diff == 0:
        logger.warning(f"  两个标准期限日期相同 ({date1})，无法插值，返回第一个标准期汇率")
        return forward_bid1, forward_ask1

    forward_bid = ((forward_bid2 - forward_bid1) / days_diff) * target_days_diff + forward_bid1
    forward_ask = ((forward_ask2 - forward_ask1) / days_diff) * target_days_diff + forward_ask1

    logger.debug(f"  插值计算: days_diff={days_diff}, target_days_diff={target_days_diff}, "
                 f"BID={forward_bid1}->{forward_bid2} => {forward_bid:.4f}, "
                 f"ASK={forward_ask1}->{forward_ask2} => {forward_ask:.4f}")
    return forward_bid, forward_ask


def _get_tenor_tod(float_config, tenor, default_tod_bid, default_tod_ask):
    """获取指定期限的TOD汇率，如未配置则使用默认值"""
    fc = float_config.get(tenor, {})
    return fc.get("tod_bid", default_tod_bid), fc.get("tod_ask", default_tod_ask)


def print_header(currency_pair, default_tod_bid, default_tod_ask, float_config, standard_dates, float_mode):
    """打印汇率计算头信息"""
    print("=" * 72)
    print(f"  基准溢价定价模式 - 指定币种远期汇率计算")
    print(f"  货币对: {currency_pair}")
    print(f"  浮动模式: {'bp浮动 (浮动值/10000)' if float_mode == 'bp' else '百分比浮动'}")
    print("=" * 72)

    print(f"\n{'─' * 50}")
    print(f"【TOD基准汇率】")
    print(f"  默认 {currency_pair} BID(客卖) TOD = {default_tod_bid}, ASK(客买) TOD = {default_tod_ask}")

    # 检查是否有期限单独配置了TOD
    custom_tod_tenors = [t for t in standard_dates if t in float_config and "tod_bid" in float_config[t]]
    if custom_tod_tenors:
        print(f"  以下期限使用了独立TOD汇率:")
        for t in custom_tod_tenors:
            fc = float_config[t]
            print(f"    {t}: BID={fc['tod_bid']}, ASK={fc['tod_ask']}")

    print(f"\n{'─' * 50}")
    print(f"【各期限浮动值配置】浮动模式: {float_mode}")
    for tenor in standard_dates:
        if tenor in float_config:
            fc = float_config[tenor]
            print(f"  {tenor}: BID浮动={fc['bid']}, ASK浮动={fc['ask']}")
        else:
            logger.warning(f"  {tenor}: ⚠ 未配置浮动值")

    print(f"\n{'─' * 50}")
    print(f"【标准期限远期汇率】")


def calculate_all_standard_forwards(default_tod_bid, default_tod_ask, float_config, standard_dates, float_mode="bp"):
    """
    计算所有标准期限的远期汇率。
    每个期限可从 float_config[tenor] 中读取独立的 tod_bid/tod_ask，未配置则使用默认值。
    """
    standard_forwards = {}
    for tenor, date_val in standard_dates.items():
        if tenor in float_config:
            tod_bid, tod_ask = _get_tenor_tod(float_config, tenor, default_tod_bid, default_tod_ask)
            fwd_bid, fwd_ask = calculate_standard_forward(
                tod_bid, tod_ask,
                float_config[tenor]["bid"],
                float_config[tenor]["ask"],
                float_mode
            )
            standard_forwards[tenor] = {"bid": fwd_bid, "ask": fwd_ask, "date": date_val}
            print(f"  {tenor} 交割日={date_val}: BID(客卖)={fwd_bid:.4f}, ASK(客买)={fwd_ask:.4f}")
        else:
            logger.warning(f"  期限 {tenor} 未配置浮动值，跳过")
    return standard_forwards


def calculate_target_forward(target_date, standard_forwards, currency_pair):
    """
    计算目标交割日的远期汇率（自动判断标准期限 / 不标准期限），并打印结果
    """
    standard_dates = {k: v["date"] for k, v in standard_forwards.items()}

    # 检查是否命中标准期限
    for tenor, date_val in standard_dates.items():
        if target_date == date_val:
            fwd_bid = standard_forwards[tenor]["bid"]
            fwd_ask = standard_forwards[tenor]["ask"]
            print(f"\n{'─' * 50}")
            print(f"  目标交割日: {target_date}")
            print(f"  类型: ★ 标准期限 ({tenor})")
            print(f"  远期BID价格(客卖/卖出{currency_pair.split('/')[0]}方向) = {fwd_bid:.4f}")
            print(f"  远期ASK价格(客买/买入{currency_pair.split('/')[0]}方向) = {fwd_ask:.4f}")
            return

    # 不标准期限，通过插值法计算
    tenor1, tenor2, date1, date2 = find_nearest_standard_tenors(target_date, standard_dates)

    fwd_bid1 = standard_forwards[tenor1]["bid"]
    fwd_ask1 = standard_forwards[tenor1]["ask"]
    fwd_bid2 = standard_forwards[tenor2]["bid"]
    fwd_ask2 = standard_forwards[tenor2]["ask"]

    fwd_bid, fwd_ask = calculate_non_standard_forward(
        fwd_bid1, fwd_ask1, date1,
        fwd_bid2, fwd_ask2, date2,
        target_date
    )

    print(f"\n{'─' * 50}")
    print(f"  目标交割日: {target_date}")
    print(f"  类型: ▲ 不标准期限（插值区间: {tenor1}({date1}) ~ {tenor2}({date2})）")
    print(f"  远期BID价格(客卖/卖出{currency_pair.split('/')[0]}方向) = {fwd_bid:.4f}")
    print(f"  远期ASK价格(客买/买入{currency_pair.split('/')[0]}方向) = {fwd_ask:.4f}")


def parse_date(date_str):
    """解析日期字符串 'YYYY-MM-DD' 为 date 对象"""
    return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()


if __name__ == '__main__':
    # ==================== 参数配置 ====================
    currency_pair = "USD/VND"

    # 默认TOD汇率（同一渠道），各期限可单独覆盖
    default_tod_bid =2637249.980000  # (结汇)买入价
    default_tod_ask = 2637250.030000   # 现汇(购汇)卖出价
    float_mode = "percentage"                # "bp" 或 "percentage"

    # float_config 中每个期限可配置 bid/ask 浮动值，也可选配独立的 tod_bid/tod_ask
    # 示例：1W 使用独立TOD，其余期限使用默认TOD
    float_config = {
        "1D": {"bid": 0.5, "ask": 1},
        "1W": {"bid": 0.02, "ask": 0.04},                                   # 使用默认TOD
        "2W": {"bid": 0.4, "ask": 0.5, "tod_bid": 2629400.000000, "tod_ask": 2629700.000000},  # 独立TOD
        # "3W": {"bid": 260, "ask": 260},
        # "4W": {"bid": 350, "ask": 350},
        # "1M": {"bid": 380, "ask": 380},
    }

    standard_tenor_dates = {
        "1D": "2026-07-23",
        "1W": "2026-07-30",
        "2W": "2026-08-05",
        # "3W": "2026-08-12",
        # "4W": "2026-08-19",
        # "1M": "2026-08-22",
    }

    target_dates = [
        "2026-07-23",   # 命中标准期限 1D
        # "2026-07-25",   # 在 1D-1W 之间
        # "2026-08-05",   # 2W
        # "2026-08-04",   # 在 2W-3W 之间
        # "2026-08-15",   # 在 3W-4W 之间
        # "2026-08-20",   # 在 4W-1M 之间
        # "2026-08-30",   # 超过 1M（外推）
    ]

    # ==================== 汇率计算 ====================
    standard_dates = {t: parse_date(d) for t, d in standard_tenor_dates.items()}
    target_date_list = [parse_date(d) for d in target_dates]

    print_header(currency_pair, default_tod_bid, default_tod_ask, float_config, standard_dates, float_mode)

    standard_forwards = calculate_all_standard_forwards(
        default_tod_bid, default_tod_ask, float_config, standard_dates, float_mode
    )

    print(f"\n{'─' * 50}")
    print(f"【目标交割日远期汇率】")

    for target_date in target_date_list:
        calculate_target_forward(target_date, standard_forwards, currency_pair)

    print(f"\n{'=' * 72}")
    print(f"  计算完成")
    print(f"{'=' * 72}")
