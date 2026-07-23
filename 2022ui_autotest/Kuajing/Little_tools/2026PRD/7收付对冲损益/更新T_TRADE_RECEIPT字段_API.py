# -*- coding: utf-8 -*-
"""
T_TRADE_RECEIPT 字段更新工具
用于更新指定订单的字段，支持两种场景：
1. 更新 CREATE_AT 的日期部分，保留原时间部分
   例: 原 2026-06-19 15:37:57，传入 2026-06-22 → 更新为 2026-06-22 15:37:57
2. 清空 SALES_PROFIT_AMT 和 PROFIT_CCY 字段（置为 NULL）
   例: UPDATE BAOFU_TRADE.T_TRADE_RECEIPT
       SET SALES_PROFIT_AMT = NULL, PROFIT_CCY = NULL WHERE ID = 68548

输入参数均为 test_receipt_nos（RECEIPT_NO 列表），内部自动查询 ID 后更新。
"""

from Kuajing.Common.kjMysql import execute_db
from typing import List, Dict, Tuple
from datetime import datetime


# ==================== 终端颜色 ====================
class Clr:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def cprint(text: str, color: str = ''):
    if color:
        print(f"{color}{text}{Clr.END}")
    else:
        print(text)


def colored(val, color: str) -> str:
    return f"{color}{val}{Clr.END}"


# ==================== 更新器 ====================

class ReceiptFieldUpdater:
    """T_TRADE_RECEIPT 字段更新器"""

    def __init__(self, env: str):
        self.env = env

    # ==================== 数据库查询 ====================

    def get_receipt_info(self, receipt_nos: List) -> Dict:
        """
        根据 RECEIPT_NO 列表查询 ID、CREATE_AT、SALES_PROFIT_AMT、PROFIT_CCY
        返回: {RECEIPT_NO: {'ID':..., 'CREATE_AT':..., 'SALES_PROFIT_AMT':..., 'PROFIT_CCY':...}}
        """
        if not receipt_nos:
            return {}

        placeholders = ', '.join(['%s'] * len(receipt_nos))
        sql = f"""
            SELECT RECEIPT_NO, ID, CREATE_AT, SALES_PROFIT_AMT, PROFIT_CCY
            FROM BAOFU_TRADE.T_TRADE_RECEIPT
            WHERE RECEIPT_NO IN ({placeholders})
        """
        result = execute_db(self.env, sql, params=tuple(receipt_nos))

        mapping = {}
        if result and isinstance(result, list):
            for row in result:
                if isinstance(row, dict):
                    mapping[row['RECEIPT_NO']] = {
                        'ID': row.get('ID'),
                        'CREATE_AT': row.get('CREATE_AT'),
                        'SALES_PROFIT_AMT': row.get('SALES_PROFIT_AMT'),
                        'PROFIT_CCY': row.get('PROFIT_CCY'),
                    }
                else:
                    # 兼容 tuple/list 返回
                    cols = ['RECEIPT_NO', 'ID', 'CREATE_AT', 'SALES_PROFIT_AMT', 'PROFIT_CCY']
                    d = dict(zip(cols, row))
                    mapping[d['RECEIPT_NO']] = d
        return mapping

    # ==================== 更新操作 ====================

    def update_create_at_date(self, receipt_nos: List, target_date: str):
        """
        情况1：更新 CREATE_AT 的日期部分，保留原时间部分
        target_date: 目标日期，格式 'YYYY-MM-DD'
        """
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"\n{'='*18} {start_time} {'='*(80-18-2-len(start_time))}", Clr.CYAN)
        cprint(f"【情况1: 更新 CREATE_AT 日期】 环境: {self.env}  目标日期: {target_date}", Clr.BOLD)
        print(f"订单号: {receipt_nos}")
        cprint(f"{'='*80}", Clr.CYAN)

        # 1. 查询当前数据
        mapping = self.get_receipt_info(receipt_nos)
        if not mapping:
            cprint(">>> 错误: 未查询到符合条件的订单数据", Clr.RED)
            return

        cprint(f"\n[1] 当前数据:", Clr.BOLD)
        for no, info in mapping.items():
            print(f"    RECEIPT_NO={no} | ID={info['ID']} | CREATE_AT={info['CREATE_AT']}")

        # 2. 校验日期格式
        try:
            datetime.strptime(target_date, '%Y-%m-%d')
        except ValueError:
            cprint(f">>> 错误: target_date 格式不正确，应为 'YYYY-MM-DD'，当前: {target_date}", Clr.RED)
            return

        # 3. 逐条更新
        cprint(f"\n[2] 执行更新:", Clr.BOLD)
        success, fail = 0, 0
        for no, info in mapping.items():
            rid = info['ID']
            create_at = info['CREATE_AT']

            if create_at is None:
                print(f"    {Clr.RED}✗{Clr.END} RECEIPT_NO={no} ID={rid}: CREATE_AT 为空，跳过")
                fail += 1
                continue

            old_str = str(create_at)
            # 提取原时间部分 HH:MM:SS
            if ' ' in old_str:
                time_part = old_str.split(' ')[1]
            else:
                time_part = '00:00:00'
            new_create_at = f"{target_date} {time_part}"

            sql = """
                UPDATE BAOFU_TRADE.T_TRADE_RECEIPT
                SET CREATE_AT = %s
                WHERE ID = %s
            """
            try:
                execute_db(self.env, sql, params=(new_create_at, rid))
                print(f"    {Clr.GREEN}✓{Clr.END} RECEIPT_NO={no} ID={rid}: "
                      f"{old_str} → {colored(new_create_at, Clr.GREEN)}")
                success += 1
            except Exception as e:
                print(f"    {Clr.RED}✗{Clr.END} RECEIPT_NO={no} ID={rid}: {e}")
                fail += 1

        # 4. 结果
        cprint(f"\n[3] 结果: 成功 {Clr.GREEN}{success}{Clr.END} 条, "
               f"失败 {Clr.RED}{fail}{Clr.END} 条", Clr.YELLOW)

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"{'='*18} {end_time} {'='*(80-18-2-len(end_time))}\n", Clr.CYAN)

    def clear_profit_fields(self, receipt_nos: List):
        """
        情况2：清空 SALES_PROFIT_AMT 和 PROFIT_CCY 字段（置为 NULL）
        """
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"\n{'='*18} {start_time} {'='*(80-18-2-len(start_time))}", Clr.CYAN)
        cprint(f"【情况2: 清空损益字段】 环境: {self.env}", Clr.BOLD)
        print(f"订单号: {receipt_nos}")
        cprint(f"{'='*80}", Clr.CYAN)

        # 1. 查询当前数据
        mapping = self.get_receipt_info(receipt_nos)
        if not mapping:
            cprint(">>> 错误: 未查询到符合条件的订单数据", Clr.RED)
            return

        cprint(f"\n[1] 当前数据:", Clr.BOLD)
        for no, info in mapping.items():
            print(f"    RECEIPT_NO={no} | ID={info['ID']} | "
                  f"SALES_PROFIT_AMT={info['SALES_PROFIT_AMT']} | PROFIT_CCY={info['PROFIT_CCY']}")

        # 2. 逐条更新
        cprint(f"\n[2] 执行更新:", Clr.BOLD)
        success, fail = 0, 0
        for no, info in mapping.items():
            rid = info['ID']
            sql = """
                UPDATE BAOFU_TRADE.T_TRADE_RECEIPT
                SET SALES_PROFIT_AMT = NULL, PROFIT_CCY = NULL
                WHERE ID = %s
            """
            try:
                execute_db(self.env, sql, params=(rid,))
                print(f"    {Clr.GREEN}✓{Clr.END} RECEIPT_NO={no} ID={rid}: "
                      f"SALES_PROFIT_AMT, PROFIT_CCY → {colored('NULL', Clr.GREEN)}")
                success += 1
            except Exception as e:
                print(f"    {Clr.RED}✗{Clr.END} RECEIPT_NO={no} ID={rid}: {e}")
                fail += 1

        # 3. 结果
        cprint(f"\n[3] 结果: 成功 {Clr.GREEN}{success}{Clr.END} 条, "
               f"失败 {Clr.RED}{fail}{Clr.END} 条", Clr.YELLOW)

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"{'='*18} {end_time} {'='*(80-18-2-len(end_time))}\n", Clr.CYAN)


# ==================== 入口 ====================

if __name__ == "__main__":
    db_env = 'FAT'
    test_receipt_nos = [2606171538003569496, 2606171537003569494,
                        2606171644003573090, 2606171643003573089]

    updater = ReceiptFieldUpdater(env=db_env)

    # 情况1：更新 CREATE_AT 的日期部分（保留原时间部分）
    # 传入目标日期，如 2026-06-22，原 2026-06-19 15:37:57 → 2026-06-22 15:37:57
    target_date = '2026-06-22'
    updater.update_create_at_date(test_receipt_nos, target_date)

    # 情况2：清空 SALES_PROFIT_AMT 和 PROFIT_CCY 字段（置为 NULL）
    updater.clear_profit_fields(test_receipt_nos)
