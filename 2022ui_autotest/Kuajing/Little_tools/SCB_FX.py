
"""渣打渠道汇率（从日志中获取）提取工具，对比研发落表的数据是否一致"""


import json
from pathlib import Path


def format_json_file(file_name):
    """格式化并美化JSON文件"""
    try:
        # 读取原始JSON文件
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 美化并重新写入文件
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"JSON文件 {file_name} 已格式化美化")
    except Exception as e:
        print(f"格式化JSON文件时出错: {e}")


def extract_t0_rates(file_name, currency_pairs=None, appoint=True):
    """
    提取T+0汇率数据并处理特殊货币对

    参数:
        file_name: JSON文件名  --从channel-center中获取的日志文件
        currency_pairs: 要查询的货币对列表，如 ["GBP/JPY", "USD/CNY"]
        appoint: True-只返回指定货币对及其反向对，False-返回所有数据
    """
    try:
        # 首先格式化JSON文件
        format_json_file(file_name)

        # 读取JSON文件
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取符合条件的数据
        results = []
        found_pairs = set()

        for rate in data.get("rates", []):
            if rate.get("tenor") == "T+0":
                base_currency = rate.get("baseCurrency")
                quote_currency = rate.get("quoteCurrency")
                original_pair = f"{base_currency}/{quote_currency}"
                reverse_pair = f"{quote_currency}/{base_currency}"
                bid_rate = rate.get("bid", {}).get("rate")
                ask_rate = rate.get("ask", {}).get("rate")
                value_date = rate.get("valueDate")
                tenor = rate.get("tenor")

                # 如果没有指定货币对，或者指定了但不appoint，或者指定了且appoint且匹配
                if not currency_pairs or not appoint or (
                        currency_pairs and (original_pair in currency_pairs or reverse_pair in currency_pairs)):
                    # 处理指定货币对的情况
                    if currency_pairs:
                        # 检查是否是原始对或反向对
                        if original_pair in currency_pairs:
                            results.append({
                                "是否全匹配": "是",
                                "货币对": original_pair,
                                "bid": float(bid_rate)*100,
                                "ask": float(ask_rate)*100,
                                "tenor": tenor,
                                "valueDate": value_date
                            })
                            found_pairs.add(original_pair)
                        elif reverse_pair in currency_pairs:
                            # 找到反向对，计算反向汇率
                            results.append({
                                "是否全匹配": "否-转换",
                                "货币对": reverse_pair,
                                "bid": 100.0 / float(ask_rate) if ask_rate else None,
                                "ask": 100.0 / float(bid_rate) if bid_rate else None,
                                "tenor": tenor,
                                "valueDate": value_date
                            })
                            # 同时添加原始对的信息（如果需要）
                            if not appoint:
                                results.append({
                                    "是否全匹配": "是",
                                    "货币对": original_pair,
                                    "bid": float(bid_rate)*100,
                                    "ask": float(ask_rate)*100,
                                    "tenor": tenor,
                                    "valueDate": value_date
                                })
                            found_pairs.add(reverse_pair)
                    else:
                        # 没有指定货币对，添加所有T+0数据
                        results.append({
                            "是否全匹配": "是",
                            "货币对": original_pair,
                            "bid": float(bid_rate)*100,
                            "ask": float(ask_rate)*100,
                            "tenor": tenor,
                            "valueDate": value_date
                        })

        # 如果指定了货币对且appoint为True，检查是否有未找到的货币对
        if currency_pairs and appoint:
            not_found = set(currency_pairs) - found_pairs
            if not_found:
                print(f"警告: 未找到以下货币对: {', '.join(not_found)}")

        # 输出表格
        if results:
            # 计算列宽
            pair_width = max(15, max(len(r["货币对"]) for r in results))
            value_width = 15
            match_width = 15

            # 打印表头
            header = (
                f"{'是否全匹配':<{match_width}} "
                f"{'货币对':<{pair_width}} "
                f"{'tenor':<15} "
                f"{'bid(结汇)':<15} "
                f"{'ask(购汇)':<15} "
                f"{'valueDate':<{value_width}}"
            )
            print(header)
            print("-" * (match_width + pair_width + 15 + 15 + 15 + value_width + 5))

            # 打印数据
            for result in results:
                line = (
                    f"{result['是否全匹配']:<{match_width}} "
                    f"{result['货币对']:<{pair_width}} "
                    f"{result['tenor']:<15} "
                    f"{result['bid']:<15.8f} "
                    f"{result['ask']:<15.8f} "
                    f"{result['valueDate']:<{value_width}}"
                )
                print(line)
        else:
            print("未找到符合条件的数据。")

    except Exception as e:
        print(f"处理数据时出错: {e}")



if __name__ == "__main__":
    # 1. 格式化JSON文件并提取所有T+0数据
    # extract_t0_rates("SCB.json")

    # 2. 提取特定货币对列表（只返回这些货币对及其反向对）
    # extract_t0_rates("SCB.json", ["GBP/JPY", "USD/CNY"], appoint=True)

    # 3. 提取特定货币对但不限制只返回这些货币对
    extract_t0_rates("SCB.json", ["GBP/JPY", "USD/CNH","GBP/USD","CNH/JPY","USD/VND","EUR/USD"], appoint=False)

    # 4. 提取不存在的货币对（会显示警告）
    # extract_t0_rates("SCB.json", ["NON/EXISTENT", "GBP/USD"], appoint=True)