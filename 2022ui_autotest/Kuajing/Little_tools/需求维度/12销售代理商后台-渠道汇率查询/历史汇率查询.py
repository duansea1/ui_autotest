"""
@Author    : duansea
@Date      : 2025/9/23
@Description: 查询多渠道历史汇率对比（支持时间段），客户视角 + 点差日志打印
"""

from pymysql.cursors import DictCursor
import pymysql
from datetime import datetime
from typing import List, Dict, Any, Optional

from Kuajing.Common.kjMysql import get_db_config_topic

# 渠道映射（根据你提供的实际ID）
CHANNEL_MAP = {
    1200923010: "GEP官方汇率",
    1200923069: "Bloomberg",
    1000000011: "中国银行",
    1108701059: "XE汇率",
    1000000003: "海云汇",
    1200923071: "渠道71"  # 示例补充
}

# 默认渠道列表（使用你提供的真实ID）
DEFAULT_CHANNEL_IDS = [1200923010, 1200923069, 1000000011, 1108701059]


def query_channel_rates_as_list(
    env: str = 'FAT',
    currency_pair: str = 'USD/CNH',
    closing_type: str = 'TOD',
    channel_base_id: int = 1200923010,  # GEP官方汇率
    other_channel_ids: List[int] = None,
    start_time: str = None,
    end_time: str = None
) -> List[List[Any]]:
    if other_channel_ids is None:
        other_channel_ids = [cid for cid in DEFAULT_CHANNEL_IDS if cid != channel_base_id]

    source_ccy, dest_ccy = currency_pair.split('/')

    db_config = get_db_config_topic(env)
    conn = pymysql.connect(**db_config, cursorclass=DictCursor)
    cursor = conn.cursor()

    try:
        channel_ids = [channel_base_id] + other_channel_ids
        placeholders = ','.join(['%s'] * len(channel_ids))

        sql = f"""
        SELECT 
            create_time as createAt, 
            channelId as channelId, 
            sourceCcy as sourceCcy, 
            destCcy as destCcy, 
            tradeDirection as tradeDirection,
            tradeRate as tradeRate 
        FROM T_TOPIC_BAOFU_CGW_CHANNEL_RATE 
        WHERE tradeRate > 0 
          AND discountRate > 0 
          AND closingType = %s
          AND create_time BETWEEN %s AND %s
          AND channelId IN ({placeholders})
          AND CONCAT(sourceCcy,'/',destCcy) = %s
        ORDER BY channelId, tradeDirection, create_time ASC  -- 👈 按渠道、方向、时间排序，方便后续处理
        """

        params = [closing_type, start_time, end_time] + channel_ids + [currency_pair]
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        # 按方向 + 渠道 分组存储所有数据（带时间）
        # 结构：{ direction: { channel_id: [ {'rate': x, 'time': datetime}, ... ] } }
        all_data = {1: {}, 2: {}}
        for row in rows:
            direction = row['tradeDirection']
            channel_id = row['channelId']
            rate = float(row['tradeRate'])
            create_time = row['createAt']  # 保持为 datetime 对象，便于计算差值

            if channel_id not in all_data[direction]:
                all_data[direction][channel_id] = []
            all_data[direction][channel_id].append({
                'rate': rate,
                'time': create_time
            })

        results = []
        query_date = f"{start_time} ~ {end_time}"

        # 🔄 处理每个方向
        for direction in [1, 2]:
            dir_data = all_data.get(direction, {})
            base_records = dir_data.get(channel_base_id, [])  # GEP 的所有记录

            if not base_records:
                continue

            # 对 GEP 的每一条记录，找其他渠道最接近的时间点
            for base_record in base_records:
                base_time = base_record['time']
                base_rate = base_record['rate']

                # 初始化行数据
                customer_action = f"卖出{source_ccy} 买入{dest_ccy}" if direction == 1 else f"卖出{dest_ccy} 买入{source_ccy}"
                row_data = [
                    currency_pair,
                    closing_type,
                    query_date,
                    customer_action,
                    CHANNEL_MAP.get(channel_base_id, str(channel_base_id)),
                    base_rate,
                    base_time.strftime("%Y-%m-%d %H:%M:%S")
                ]

                # 遍历其他渠道，找最接近 base_time 的记录
                for cid in other_channel_ids:
                    ch_records = dir_data.get(cid, [])
                    if not ch_records:
                        row_data.extend(["-", "-", "-"])
                        continue

                    # 找时间最接近 base_time 的记录
                    closest_record = min(
                        ch_records,
                        key=lambda r: abs((r['time'] - base_time).total_seconds())
                    )

                    compare_rate = closest_record['rate']
                    compare_time = closest_record['time'].strftime("%Y-%m-%d %H:%M:%S")

                    # 计算点差
                    if direction == 1:  # 客户卖出 → 汇率越高越优
                        diff_pct = (compare_rate - base_rate) / base_rate * 100
                        label = "优" if diff_pct > 0 else "差"
                    else:  # 客户买入 → 汇率越低越优
                        diff_pct = (compare_rate - base_rate) / base_rate * 100
                        label = "优" if diff_pct < 0 else "差"

                    row_data.append(compare_rate)
                    row_data.append(compare_time)
                    row_data.append(f"{label}({diff_pct:+.6f}%)")

                results.append(row_data)

        # 校验（可选）：对每个快照，检查卖出 > 买入（如果同时间点有双向数据）
        # 此处略，因为不同时间点，校验意义不大

        return results

    finally:
        cursor.close()
        conn.close()

def print_rate_table(results: List[List[Any]], other_channel_ids: List[int]):
    if not results:
        print("⚠️  未查询到有效汇率数据")
        return

    # ✅ 修改：新增“基准时间”列，每个对比渠道新增“时间”列
    headers = ["货币对", "期限", "时间范围", "客户操作", "基准渠道", "基准汇率", "基准时间"]
    for cid in other_channel_ids:
        ch_name = CHANNEL_MAP.get(cid, str(cid))
        headers.append(ch_name)           # 汇率
        headers.append(f"{ch_name}时间")  # ✅ 新增时间列
        headers.append(f"{ch_name}_优差")

    def get_display_width(s):
        s = str(s)
        width = 0
        for c in s:
            width += 2 if '\u4e00' <= c <= '\u9fff' else 1
        return width

    col_widths = []
    for i in range(len(headers)):
        max_width = max(get_display_width(row[i]) if i < len(row) else 0 for row in [headers] + results)
        col_widths.append(max(max_width, len(headers[i])) + 2)

    header_parts = [f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)]
    print(" | ".join(header_parts))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    for row in results:
        row_parts = [f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)]
        print(" | ".join(row_parts))

def print_detail_diff_log(results: List[List[Any]], other_channel_ids: List[int], currency_pair: str = "USD/CNH"):
    if not results:
        print("📝 点差日志：无数据")
        return

    print(f"\n📝 详细点差日志（{currency_pair}）：")
    print("=" * 100)  # 拉宽

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    col_offset = 7  # 👈 现在前7列是：货币对、期限、时间范围、操作、基准渠道、基准汇率、基准时间

    for row in results:
        customer_action = row[3]
        base_channel = row[4]
        base_time = row[6]  # ✅ 基准时间

        for i, cid in enumerate(other_channel_ids):
            ch_name = CHANNEL_MAP.get(cid, str(cid))
            rate_col = col_offset + i * 3      # 汇率
            time_col = rate_col + 1            # 时间
            diff_col = time_col + 1            # 优差

            if rate_col >= len(row) or row[rate_col] == "-" or row[diff_col] == "-":
                continue

            compare_rate = row[rate_col]
            compare_time = row[time_col]       # ✅ 对比时间
            diff_str = row[diff_col]

            try:
                conclusion = diff_str.split("(")[0]
                diff_val_str = diff_str.split("(")[1].replace("%", "").replace(")", "")
                diff_val = float(diff_val_str)
            except Exception:
                conclusion = "?"
                diff_val = 0.0

            print(f"[{current_time}] [{currency_pair}] [{customer_action}] "
                  f"[{ch_name}({compare_time})] vs [{base_channel}({base_time})] => "  # ✅ 带上时间
                  f"点差: {diff_val:+.6f}%, 结论: {conclusion}")

    print("=" * 100)
# 示例调用
if __name__ == "__main__":
    channel_base = 1200923010  # GEP官方汇率
    other_channels = [1200923069, 1000000003, 1200923071]  # Bloomberg, 海云汇, 渠道71

    start = "2025-09-23 08:00:00"
    end = "2025-09-23 10:00:00"

    results = query_channel_rates_as_list(
        env='FAT',
        currency_pair='EUR/CNH',
        closing_type='TOD',
        channel_base_id=channel_base,
        other_channel_ids=other_channels,
        start_time=start,
        end_time=end
    )

    print("📊 历史汇率对比结果（客户视角）：")
    print_rate_table(results, other_channels)

    print_detail_diff_log(results, other_channels, currency_pair='HKD/CNH')

    print(f"\n✅ 原始数据（共{len(results)}条记录）：")
    for i, row in enumerate(results, 1):
        print(f"记录 {i}: {row}")