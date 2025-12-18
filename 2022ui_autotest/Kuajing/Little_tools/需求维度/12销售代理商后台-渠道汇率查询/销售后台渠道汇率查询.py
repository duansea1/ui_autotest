"""
@Author    : duansea
@Date      : 2025/9/22 17:39
@Description: 查询多渠道汇率对比，支持客户视角方向展示 + 点差日志打印
"""

from pymysql.cursors import DictCursor
import pymysql
from datetime import datetime
from typing import List, Dict, Any, Optional

from Kuajing.Common.kjMysql import get_db_config

# 渠道映射（根据你提供的实际ID）
CHANNEL_MAP = {
    1200923010: "GEP官方汇率",
    1200923069: "Bloomberg",
    1000000011: "中国银行",
    1108701059: "XE汇率",
    1000000003:"海云汇"
}

# 默认渠道列表（使用你提供的真实ID）
DEFAULT_CHANNEL_IDS = [1200923010, 1200923069, 1000000011, 1108701059]


def query_channel_rates_as_list(
    env: str = 'FAT',
    currency_pair: str = 'USD/CNH',
    closing_type: str = 'SPOT',
    channel_base_id: int = 1200923010,
    other_channel_ids: List[int] = None
) -> List[List[Any]]:
    """
    查询汇率并以列表形式返回（客户视角）
    数据库 TRADE_DIRECTION:
        1 = 系统买入 → 客户卖出
        2 = 系统卖出 → 客户买入
    所以展示时要反转！
    """
    if other_channel_ids is None:
        other_channel_ids = [cid for cid in DEFAULT_CHANNEL_IDS if cid != channel_base_id]

    source_ccy, dest_ccy = currency_pair.split('/')

    db_config = get_db_config(env)
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    try:
        channel_ids = [channel_base_id] + other_channel_ids
        placeholders = ','.join(['%s'] * len(channel_ids))

        sql = f"""
        SELECT 
            t.CHANNEL_ID as channelId, 
            t.SOURCE_CCY as sourceCcy, 
            t.DEST_CCY as destCcy, 
            t.TRADE_DIRECTION as tradeDirection,
            t.CLOSING_TYPE AS closingType, 
            MAX(t.TRADE_RATE) AS tradeRate, 
            MIN(t.UPDATE_AT) as updateAt 
        FROM BAOFU_CGW.T_CHANNEL_RATE_REAL t 
        WHERE t.STATUS = 1 
          AND t.CHANNEL_ID IN ({placeholders})
          AND t.CLOSING_TYPE = %s
          AND t.CREATE_AT >= DATE_ADD(NOW(), INTERVAL -2 DAY)
          AND (
              (t.SOURCE_CCY = %s AND t.DEST_CCY = %s) OR
              (t.SOURCE_CCY = %s AND t.DEST_CCY = %s)
          )
        GROUP BY t.CHANNEL_ID, t.SOURCE_CCY, t.DEST_CCY, t.TRADE_DIRECTION, t.CLOSING_TYPE 
        ORDER BY t.CHANNEL_ID, t.TRADE_DIRECTION
        """

        params = channel_ids + [closing_type, source_ccy, dest_ccy, dest_ccy, source_ccy]
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        # 按数据库方向组织数据（1=系统买入/客户卖出，2=系统卖出/客户买入）
        direction_data = {1: {}, 2: {}}
        for row in rows:
            direction_data[row['tradeDirection']][row['channelId']] = float(row['tradeRate'])

        results = []
        today = datetime.now().strftime("%Y-%m-%d")

        # 🔄 客户视角方向1：客户卖出 source_ccy，买入 dest_ccy → 对应数据库 TRADE_DIRECTION=1
        # ✅ 汇率越大越好（客户卖出外币，希望换更多本币）
        dir1_rates = direction_data.get(1, {})  # 客户卖出
        base_rate_sell = dir1_rates.get(channel_base_id)
        if base_rate_sell is not None:
            row_data = [
                currency_pair,
                closing_type,
                today,
                f"卖出{source_ccy} 买入{dest_ccy}",  # 客户操作
                CHANNEL_MAP.get(channel_base_id, str(channel_base_id)),
                base_rate_sell
            ]
            for cid in other_channel_ids:
                rate = dir1_rates.get(cid)
                if rate is None:
                    row_data.append("-")
                    row_data.append("-")
                else:
                    diff_pct = (rate - base_rate_sell) / base_rate_sell * 100
                    label = "优" if diff_pct > 0 else "差"  # 汇率越大越好 → 正数=优
                    row_data.append(rate)
                    row_data.append(f"{label}({diff_pct:+.6f}%)")
            results.append(row_data)

        # 🔄 客户视角方向2：客户买入 source_ccy，卖出 dest_ccy → 对应数据库 TRADE_DIRECTION=2
        # ✅ 汇率越小越好（客户买入外币，希望花更少本币）
        dir2_rates = direction_data.get(2, {})  # 客户买入
        base_rate_buy = dir2_rates.get(channel_base_id)
        if base_rate_buy is not None:
            row_data = [
                currency_pair,
                closing_type,
                today,
                f"买入{source_ccy} 卖出{dest_ccy}",  # 客户操作
                CHANNEL_MAP.get(channel_base_id, str(channel_base_id)),
                base_rate_buy
            ]
            for cid in other_channel_ids:
                rate = dir2_rates.get(cid)
                if rate is None:
                    row_data.append("-")
                    row_data.append("-")
                else:
                    diff_pct = (rate - base_rate_buy) / base_rate_buy * 100
                    label = "优" if diff_pct < 0 else "差"  # 汇率越小越好 → 负数=优
                    row_data.append(rate)
                    row_data.append(f"{label}({diff_pct:+.6f}%)")
            results.append(row_data)

        # ✅ 校验逻辑：客户卖出汇率应 > 客户买入汇率
        if base_rate_sell is not None and base_rate_buy is not None:
            if base_rate_sell <= base_rate_buy:
                print(f"⚠️  警告：卖出汇率({base_rate_sell}) 应大于买入汇率({base_rate_buy})，数据可能异常！")

        return results

    finally:
        cursor.close()
        conn.close()


def print_rate_table(results: List[List[Any]], other_channel_ids: List[int]):
    """
    以表格形式打印列表结果（对齐优化）
    """
    if not results:
        print("⚠️  未查询到有效汇率数据")
        return

    headers = ["货币对", "期限", "日期", "客户操作", "基准渠道", "基准汇率"]
    for cid in other_channel_ids:
        ch_name = CHANNEL_MAP.get(cid, str(cid))
        headers.append(ch_name)
        headers.append(f"{ch_name}_优差")

    # 自动计算列宽（中文按2字符宽度估算）
    def get_display_width(s):
        s = str(s)
        width = 0
        for c in s:
            width += 2 if '\u4e00' <= c <= '\u9fff' else 1  # 中文算2宽度
        return width

    col_widths = []
    for i in range(len(headers)):
        max_width = max(get_display_width(row[i]) if i < len(row) else 0 for row in [headers] + results)
        col_widths.append(max(max_width, len(headers[i])) + 2)  # 最小留2空格

    # 打印表头
    header_parts = []
    for i, h in enumerate(headers):
        header_parts.append(f"{h:<{col_widths[i]}}")
    print(" | ".join(header_parts))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))  # 分隔线长度

    # 打印数据
    for row in results:
        row_parts = []
        for i, cell in enumerate(row):
            row_parts.append(f"{str(cell):<{col_widths[i]}}")
        print(" | ".join(row_parts))


def print_detail_diff_log(results: List[List[Any]], other_channel_ids: List[int], currency_pair: str = "USD/CNH"):
    """
    🆕 修复版：打印详细的点差日志（直接使用表格中已计算的优差结论，避免二次逻辑错误）
    格式：
    [时间] [货币对] [客户操作] [对比渠道] vs [基准渠道] => 点差: X.XXXXXX%, 结论: 优/差
    """
    if not results:
        print("📝 点差日志：无数据")
        return

    print(f"\n📝 详细点差日志（{currency_pair}）：")
    print("=" * 80)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    col_offset = 6  # 前6列是：货币对、期限、日期、客户操作、基准渠道、基准汇率

    for row in results:
        customer_action = row[3]  # 如 "卖出USD 买入CNH"
        base_channel = row[4]
        base_rate = row[5]

        for i, cid in enumerate(other_channel_ids):
            ch_name = CHANNEL_MAP.get(cid, str(cid))
            rate_col = col_offset + i * 2
            diff_col = rate_col + 1  # 优差列，如 "优(-0.148061%)"

            if rate_col >= len(row) or row[rate_col] == "-" or row[diff_col] == "-":
                continue

            compare_rate = row[rate_col]
            diff_str = row[diff_col]  # 如 "优(-0.148061%)"

            # ✅ 直接提取“优”或“差”标签，不再重新计算！
            try:
                # 提取括号前的“优”或“差”
                conclusion = diff_str.split("(")[0]  # "优" 或 "差"
                # 提取数值部分
                diff_val_str = diff_str.split("(")[1].replace("%", "").replace(")", "")
                diff_val = float(diff_val_str)
            except Exception as e:
                conclusion = "?"
                diff_val = 0.0

            print(f"[{current_time}] [{currency_pair}] [{customer_action}] "
                  f"[{ch_name}] vs [{base_channel}] => "
                  f"点差: {diff_val:+.6f}%, 结论: {conclusion}")

    print("=" * 80)


# 示例调用
if __name__ == "__main__":
    channel_base = 1200923010  # GEP官方汇率
    other_channels = [1200923069,1000000003]  # Bloomberg

    results = query_channel_rates_as_list(
        env='FAT',
        currency_pair='USD/VND',
        closing_type='TOD',
        channel_base_id=channel_base,
        other_channel_ids=other_channels
    )

    print("📊 汇率对比结果（客户视角）：")
    print_rate_table(results, other_channels)

    # ✅ 新增：打印点差日志
    print_detail_diff_log(results, other_channels, currency_pair='USD/CNH')

    print(f"\n✅ 原始数据（共{len(results)}条记录）：")
    for i, row in enumerate(results, 1):
        print(f"记录 {i}: {row}")