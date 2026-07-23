"""FORWARD_RATE_指定币种远期汇率计算.py: 计算指定币种的远期标准期限和不标准期限汇率（基准溢价定价模式）"""

from datetime import date, datetime
import logging
import os
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加跨境公共模块路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'Common'))
try:
    from kjMysql import execute_db_topic, execute_db
    _HAS_DB = True
except ImportError:
    _HAS_DB = False
    logger.warning("⚠ 无法导入 kjMysql，数据库查询功能不可用")

# ======================== ANSI 颜色 & 标签 ========================
# 启用 Windows 终端 ANSI & UTF-8 支持
if sys.platform == "win32":
    os.system("")  # 激活 ANSI 转义序列
sys.stdout.reconfigure(encoding='utf-8')

C_RESET   = "\033[0m"
C_BOLD    = "\033[1m"
C_CYAN    = "\033[96m"     # 横幅 / 主标题
C_GREEN   = "\033[92m"     # 标准期限命中 / 成功
C_YELLOW  = "\033[93m"     # 不标准期限 / 插值 / 警告
C_BLUE    = "\033[94m"     # 渠道汇率
C_MAGENTA = "\033[95m"     # 用户汇率
C_RED     = "\033[91m"     # 错误
C_GRAY    = "\033[90m"     # 辅助信息

# 标签 emoji
TAG_CHANNEL  = "🏦"   # 渠道汇率
TAG_USER     = "👤"   # 用户汇率
TAG_STANDARD = "✅"   # 标准期限命中
TAG_INTERP   = "🔄"   # 插值 / 不标准期限
TAG_WARN     = "⚠️"   # 警告
TAG_CONFIG   = "📊"   # 配置信息
TAG_TARGET   = "🎯"   # 目标交割日
TAG_DONE     = "🚀"   # 完成


def calculate_bp_float_forward(tod_bid, tod_ask, float_bid_bp, float_ask_bp):
    """
    bp浮动模式计算远期汇率
    远期BID价格(客卖) = TOD BID - 浮动值X / 100
    远期ASK价格(客买) = TOD ASK + 浮动值X / 100

    参数:
    - tod_bid: TOD买入价（客卖方向基准）(float)
    - tod_ask: TOD卖出价（客买方向基准）(float)
    - float_bid_bp: BID方向浮动bp值 (float)
    - float_ask_bp: ASK方向浮动bp值 (float)

    返回:
    - (forward_bid, forward_ask): 远期买入价和卖出价 (tuple)
    """
    forward_bid = tod_bid - float_bid_bp / 100
    forward_ask = tod_ask + float_ask_bp / 100
    logger.debug(f"  bp浮动计算: BID={tod_bid} - {float_bid_bp}/100 = {forward_bid:.4f}, "
                 f"ASK={tod_ask} + {float_ask_bp}/100 = {forward_ask:.4f}")
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


# =============================================================================
# 数据库查询：从 T_CHANNEL_RATE_REAL 获取渠道 TOD 汇率
# =============================================================================

def query_tod_from_db(env, channel_id, currency_pair):
    """
    从 T_CHANNEL_RATE_REAL 表查询指定渠道的 TOD 汇率。

    ⚠ 方向映射（渠道方向 → 用户方向）：
       - TRADE_DIRECTION=1（渠道买入）→ 用户卖出方向 → BID(客卖)
       - TRADE_DIRECTION=2（渠道卖出）→ 用户买入方向 → ASK(客买)

    参数:
    - env: 环境（FAT/UAT）
    - channel_id: 渠道编号
    - currency_pair: 货币对，如 "USD/VND"

    返回:
    - (tod_bid, tod_ask): 用户视角的 TOD 买入价和卖出价
    """
    if not _HAS_DB:
        raise RuntimeError("数据库模块未导入，无法查询 DB")

    ccy = currency_pair.split('/')
    source_ccy = ccy[0]
    dest_ccy = ccy[1]

    sql = (
        f"SELECT TRADE_DIRECTION, TRADE_RATE "
        f"FROM T_CHANNEL_RATE_REAL "
        f"WHERE CHANNEL_ID = '{channel_id}' "
        f"AND SOURCE_CCY = '{source_ccy}' "
        f"AND DEST_CCY = '{dest_ccy}' "
        f"AND CLOSING_TYPE = 'TOD' "
        f"AND STATUS = 1 "
        f"ORDER BY RATE_QUERY_DATE DESC "
        f"LIMIT 2"
    )

    logger.info(f"查询渠道 {channel_id} 的 TOD 汇率: {source_ccy}/{dest_ccy}")
    logger.debug(f"SQL: {sql}")

    result = execute_db(env, sql, database="BAOFU_CGW")

    tod_bid = None   # 用户 BID(客卖) ← TRADE_DIRECTION=1
    tod_ask = None   # 用户 ASK(客买) ← TRADE_DIRECTION=2

    for row in result:
        if row['TRADE_DIRECTION'] == 1:   # 渠道买入 → 用户卖出
            tod_bid = float(row['TRADE_RATE'])
        elif row['TRADE_DIRECTION'] == 2: # 渠道卖出 → 用户买入
            tod_ask = float(row['TRADE_RATE'])
        else:
            logger.warning(f"  未知 TRADE_DIRECTION={row['TRADE_DIRECTION']}，跳过")

    if tod_bid is None or tod_ask is None:
        missing = []
        if tod_bid is None: missing.append("BID(客卖/TRADE_DIRECTION=1)")
        if tod_ask is None: missing.append("ASK(客买/TRADE_DIRECTION=2)")
        raise ValueError(
            f"渠道 {channel_id} 未查询到完整的 TOD 汇率，缺失: {', '.join(missing)}。"
            f"查询结果: {result}"
        )

    # 校验：正常情况买入汇率 > 卖出汇率
    if tod_ask <= tod_bid:
        logger.warning(
            f"{TAG_WARN} 异常汇率: ASK(客买)={tod_ask} <= BID(客卖)={tod_bid}，"
            f"请检查渠道 {channel_id} 数据"
        )

    logger.info(f"  渠道 {channel_id} TOD: BID(客卖)={tod_bid}, ASK(客买)={tod_ask}")
    return tod_bid, tod_ask


def resolve_tod_rates_from_db(env, float_config, default_channel_id, currency_pair):
    """
    从 DB 解析各期限的 TOD 汇率：
    - 期限配置了 channel_id → 从该渠道查询 TOD
    - 期限未配置 channel_id → 使用 default_channel_id 查询 TOD

    参数:
    - env: 环境（FAT/UAT）
    - float_config: 浮动值配置
    - default_channel_id: 默认渠道编号
    - currency_pair: 货币对

    返回:
    - (tod_rates_map, default_tod_bid, default_tod_ask)
      tod_rates_map: {tenor: {"bid": ..., "ask": ...}}
    """
    # 先获取默认渠道的 TOD（兜底值）
    default_tod_bid, default_tod_ask = query_tod_from_db(
        env, default_channel_id, currency_pair
    )

    tod_rates_map = {}
    for tenor, config in float_config.items():
        channel_id = config.get("channel_id")
        if channel_id:
            # 期限有独立渠道，从该渠道获取 TOD
            tenor_tod_bid, tenor_tod_ask = query_tod_from_db(
                env, str(channel_id), currency_pair
            )
            tod_rates_map[tenor] = {"bid": tenor_tod_bid, "ask": tenor_tod_ask}
        else:
            # 使用默认渠道 TOD
            tod_rates_map[tenor] = {"bid": default_tod_bid, "ask": default_tod_ask}

    return tod_rates_map, default_tod_bid, default_tod_ask


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
    mode_label = f"{C_BOLD}bp浮动 (浮动值/10000){C_RESET}" if float_mode == "bp" else f"{C_BOLD}百分比浮动{C_RESET}"
    print(f"{C_CYAN}{'=' * 72}{C_RESET}")
    print(f"  {C_CYAN}{C_BOLD}{TAG_CHANNEL} 基准溢价定价模式 - 指定币种远期汇率计算{C_RESET}")
    print(f"  货币对: {C_BOLD}{currency_pair}{C_RESET}")
    print(f"  浮动模式: {mode_label}")
    print(f"{C_CYAN}{'=' * 72}{C_RESET}")

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"{C_BOLD}{TAG_CONFIG}【TOD基准汇率】{C_RESET}")
    print(f"  {C_GRAY}默认{C_RESET} {currency_pair} BID(客卖) TOD = {C_BOLD}{default_tod_bid}{C_RESET},  "
          f"ASK(客买) TOD = {C_BOLD}{default_tod_ask}{C_RESET}")

    # 检查是否有期限单独配置了TOD
    custom_tod_tenors = [t for t in standard_dates if t in float_config and "tod_bid" in float_config[t]]
    if custom_tod_tenors:
        print(f"  {C_YELLOW}以下期限使用了独立TOD汇率:{C_RESET}")
        for t in custom_tod_tenors:
            fc = float_config[t]
            print(f"    {t}: BID={C_BOLD}{fc['tod_bid']}{C_RESET}, ASK={C_BOLD}{fc['tod_ask']}{C_RESET}")

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"{C_BOLD}{TAG_CONFIG}【各期限浮动值配置】{C_RESET}浮动模式: {float_mode}")
    for tenor in standard_dates:
        if tenor in float_config:
            fc = float_config[tenor]
            print(f"  {tenor}: BID浮动={fc['bid']}, ASK浮动={fc['ask']}")
        else:
            logger.warning(f"  {tenor}: {TAG_WARN} 未配置浮动值")

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"{C_BOLD}{TAG_CHANNEL}【渠道标准期限远期汇率】{C_RESET}")


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
            print(f"  {C_BLUE}{tenor}{C_RESET} 交割日={date_val}: "
                  f"BID(客卖)={C_BOLD}{fwd_bid:.4f}{C_RESET}, "
                  f"ASK(客买)={C_BOLD}{fwd_ask:.4f}{C_RESET}")
        else:
            logger.warning(f"  期限 {tenor} 未配置浮动值，跳过")
    return standard_forwards


def calculate_target_forward(target_date, standard_forwards, currency_pair, label="渠道汇率"):
    """
    计算目标交割日的远期汇率（自动判断标准期限 / 不标准期限），并打印结果。
    label: "渠道汇率"（BID在上） 或 "用户汇率"（ASK在上）
    """
    standard_dates = {k: v["date"] for k, v in standard_forwards.items()}
    ccy = currency_pair.split('/')[0]

    # 检查是否命中标准期限
    for tenor, date_val in standard_dates.items():
        if target_date == date_val:
            fwd_bid = standard_forwards[tenor]["bid"]
            fwd_ask = standard_forwards[tenor]["ask"]
            print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
            print(f"  {C_BOLD}--------{label}------{C_RESET}")
            print(f"  {C_BOLD}{TAG_TARGET} 目标交割日: {target_date}{C_RESET}")
            print(f"  类型: {C_GREEN}{TAG_STANDARD} 标准期限 ({tenor}){C_RESET}")
            print(f"  远期ASK价格(客买/买入{ccy}方向) = {C_BOLD}{fwd_ask:.4f}{C_RESET}")
            print(f"  远期BID价格(客卖/卖出{ccy}方向) = {C_BOLD}{fwd_bid:.4f}{C_RESET}")
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

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"  {C_BOLD}--------{label}------{C_RESET}")
    print(f"  {C_BOLD}{TAG_TARGET} 目标交割日: {target_date}{C_RESET}")
    print(f"  类型: {C_YELLOW}{TAG_INTERP} 不标准期限（插值区间: {tenor1}({date1}) ~ {tenor2}({date2})）{C_RESET}")
    print(f"  远期ASK价格(客买/买入{ccy}方向) = {C_BOLD}{fwd_ask:.4f}{C_RESET}")
    print(f"  远期BID价格(客卖/卖出{ccy}方向) = {C_BOLD}{fwd_bid:.4f}{C_RESET}")


def apply_user_float(channel_bid, channel_ask, user_float_bid, user_float_ask, float_mode):
    """
    在渠道远期汇率基础上叠加用户浮动，得到用户最终汇率。
    公式同渠道浮动：
      bp模式:   用户BID = 渠道BID - user_float_bid / 10000
               用户ASK = 渠道ASK + user_float_ask / 10000
      百分比模式: 用户BID = 渠道BID * (1 - user_float_bid / 100)
               用户ASK = 渠道ASK * (1 + user_float_ask / 100)
    """
    if float_mode == "bp":
        user_bid = channel_bid - user_float_bid / 10000
        user_ask = channel_ask + user_float_ask / 10000
    elif float_mode == "percentage":
        user_bid = channel_bid * (1 - user_float_bid / 100)
        user_ask = channel_ask * (1 + user_float_ask / 100)
    else:
        raise ValueError(f"不支持的浮动模式: {float_mode}")
    return user_bid, user_ask


def apply_user_float_to_standard_forwards(channel_forwards, user_float_config, float_mode):
    """
    对渠道标准期限远期汇率叠加用户浮动，生成用户标准期限远期汇率。
    未配置用户浮动的期限，直接使用渠道汇率（无浮动）。
    """
    user_forwards = {}
    for tenor, fwd in channel_forwards.items():
        if tenor in user_float_config:
            ufc = user_float_config[tenor]
            user_bid, user_ask = apply_user_float(
                fwd["bid"], fwd["ask"], ufc["bid"], ufc["ask"], float_mode
            )
            user_forwards[tenor] = {"bid": user_bid, "ask": user_ask, "date": fwd["date"]}
            print(f"  {C_MAGENTA}{tenor}{C_RESET} 交割日={fwd['date']}: "
                  f"{C_GRAY}渠道BID={fwd['bid']:.4f}{C_RESET} → "
                  f"{C_MAGENTA}{C_BOLD}用户BID={user_bid:.4f}{C_RESET},  "
                  f"{C_GRAY}渠道ASK={fwd['ask']:.4f}{C_RESET} → "
                  f"{C_MAGENTA}{C_BOLD}用户ASK={user_ask:.4f}{C_RESET}")
        else:
            user_forwards[tenor] = fwd
            print(f"  {C_MAGENTA}{tenor}{C_RESET} 交割日={fwd['date']}: "
                  f"{C_GRAY}无用户浮动，使用渠道汇率 "
                  f"BID={C_BOLD}{fwd['bid']:.4f}{C_RESET}, ASK={C_BOLD}{fwd['ask']:.4f}{C_RESET}")
    return user_forwards


def print_user_header(user_float_config, standard_dates, float_mode):
    """打印用户浮动配置头信息"""
    print(f"\n{C_CYAN}{'=' * 72}{C_RESET}")
    print(f"{C_BOLD}{TAG_USER}【用户维度浮动】{C_RESET}浮动模式: {float_mode}")
    print(f"{C_CYAN}{'─' * 50}{C_RESET}")
    has_config = False
    for tenor in standard_dates:
        if tenor in user_float_config:
            ufc = user_float_config[tenor]
            print(f"  {C_MAGENTA}{tenor}{C_RESET}: BID浮动={ufc['bid']}, ASK浮动={ufc['ask']}")
            has_config = True
    if not has_config:
        print(f"  {C_GRAY}(无用户浮动配置，用户汇率=渠道汇率){C_RESET}")
    return has_config


def parse_date(date_str):
    """解析日期字符串 'YYYY-MM-DD' 为 date 对象"""
    return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()


if __name__ == '__main__':
    # ==================== 参数配置 ====================
    env = "FAT"                              # 环境: FAT / UAT
    currency_pair = "USD/VND"
    default_channel_id = "1200923033"        # 默认渠道ID（未配置独立渠道的期限使用此渠道TOD）
    float_mode = "percentage"                # "bp" 或 "percentage"

    # float_config 中每个期限可配置 bid/ask 浮动值，也可选配独立的 channel_id
    # 配置了 channel_id 的期限 → 从该渠道获取独立 TOD
    # 未配置 channel_id → 使用 default_channel_id 获取 TOD
    # 不写 channel_id 也不写 tod_bid/tod_ask → 自动使用默认渠道 TOD
    float_config = {
        "1D": {"bid": 0.5, "ask": 1},
        # "1W": {"bid": 0.02, "ask": 0.04},                               # 使用默认渠道 TOD
        "2W": {"bid": 0.4, "ask": 0.5, "channel_id": "1200923030"},     # 2W 使用独立渠道获取独立 TOD
        # "3W": {"bid": 260, "ask": 260},
        # "4W": {"bid": 350, "ask": 350},
        # "1M": {"bid": 380, "ask": 380},
    }
    float_config1 = {
        "1D": {"bid": 100, "ask": 100},
        "1W": {"bid": 200, "ask": 400},                               # 使用默认渠道 TOD
        "2W": {"bid": 400, "ask": 500, "channel_id": "1200923030"},     # 2W 使用独立渠道获取独立 TOD
        # "3W": {"bid": 260, "ask": 260},
        # "4W": {"bid": 350, "ask": 350},
        # "1M": {"bid": 380, "ask": 380},
    }

    # 用户维度浮动配置（在渠道汇率基础上叠加，未配置的期限无浮动）
    # 浮动模式同渠道 float_mode
    user_float_config = {
        "1D": {"bid": 5, "ask": 5},
        "1W": {"bid": 5, "ask": 5},
        "2W": {"bid": 1.2, "ask": 1.1},   # 不配置则2W无用户浮动
    }
    user_float_config1 = {
        "1D": {"bid": 100, "ask": 100},
        # "1W": {"bid": -1, "ask": -1},
        "2W": {"bid": 202, "ask": 201},   # 不配置则2W无用户浮动
    }

    standard_tenor_dates = {
        "1D": "2026-07-23",
        "1W": "2026-07-29",
        "2W": "2026-08-05",
        # "3W": "2026-08-12",
        # "4W": "2026-08-19",
        # "1M": "2026-08-22",
    }

    target_dates = [
        # "2026-07-23",   # 命中标准期限 1D
        "2026-07-28",   # 在 1D-1W 之间
        # "2026-08-05",   # 2W
        # "2026-08-04",   # 在 2W-3W 之间
        # "2026-08-15",   # 在 3W-4W 之间
        # "2026-08-20",   # 在 4W-1M 之间
        # "2026-08-30",   # 超过 1M（外推）
    ]

    # ==================== 汇率计算 ====================
    standard_dates = {t: parse_date(d) for t, d in standard_tenor_dates.items()}
    target_date_list = [parse_date(d) for d in target_dates]

    # ---- 从 DB 获取各期限的 TOD 汇率 ----
    if _HAS_DB:
        tod_rates_map, default_tod_bid, default_tod_ask = resolve_tod_rates_from_db(
            env, float_config, default_channel_id, currency_pair
        )
        # 将 DB 获取的 TOD 注入 float_config（后续 _get_tenor_tod 会自动读取注入的值）
        for tenor, rates in tod_rates_map.items():
            if tenor in float_config:
                float_config[tenor]["tod_bid"] = rates["bid"]
                float_config[tenor]["tod_ask"] = rates["ask"]
    else:
        # 回退：使用默认硬编码值
        default_tod_bid = 2637249.980000  # (结汇)买入价
        default_tod_ask = 2637250.030000  # 现汇(购汇)卖出价

    print_header(currency_pair, default_tod_bid, default_tod_ask, float_config, standard_dates, float_mode)

    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n  {C_BOLD}----------{start_time}------{C_RESET}")

    standard_forwards = calculate_all_standard_forwards(
        default_tod_bid, default_tod_ask, float_config, standard_dates, float_mode
    )

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"{C_BOLD}{TAG_CHANNEL}【目标交割日远期汇率（渠道）】{C_RESET}")

    for target_date in target_date_list:
        calculate_target_forward(target_date, standard_forwards, currency_pair, label="渠道汇率")

    # ==================== 用户维度浮动 ====================
    print_user_header(user_float_config, standard_dates, float_mode)

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"{C_BOLD}{TAG_USER}【用户标准期限远期汇率】{C_RESET}")
    user_standard_forwards = apply_user_float_to_standard_forwards(
        standard_forwards, user_float_config, float_mode
    )

    print(f"\n{C_CYAN}{'─' * 50}{C_RESET}")
    print(f"{C_BOLD}{TAG_USER}【目标交割日远期汇率（用户最终汇率）】{C_RESET}")

    for target_date in target_date_list:
        calculate_target_forward(target_date, user_standard_forwards, currency_pair, label="用户汇率")

    print(f"\n{C_CYAN}{'=' * 72}{C_RESET}")
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"  {C_BOLD}----------{end_time}------{C_RESET}")
    print(f"  {C_GREEN}{TAG_DONE} 计算完成{C_RESET}")
    print(f"{C_CYAN}{'=' * 72}{C_RESET}")
