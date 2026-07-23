# -*- coding: utf-8 -*-
"""
非基准交易剔除配置 - 凭证数据查询工具

功能：
1. 查询启用的配置 T_NON_BENCHMARK_TRADE_EXCLUDE_CONFIG (STATUS='ENABLE')
2. 按方向分组展示（卖出USD/买入VND、卖出VND/买入USD 成对出现）
3. 根据每条配置查询 T_TRADE_RECEIPT 凭证数据
   - SELL_CCY/BUY_CCY → 映射 SOURCE/TARGET + TRADE_DIRECTION
   - INCLUDE_MERCHANT_GROUP → exists 子查询 (使用常规算法)
   - EXCLUDE_MERCHANT_GROUP → not exists 子查询 (不使用常规算法)
4. 同方向多条配置的结果按 ID 取并集去重

方向映射（以货币对第一个币种为准）：
- SELL=VND, BUY=USD → TRADE_DIRECTION=1 (买入方向/收款：用户卖出VND买入USD)
- SELL=USD, BUY=VND → TRADE_DIRECTION=2 (卖出方向/付款：用户卖出USD买入VND)

商户分组说明：
- 指定商户分组(INCLUDE): 只有分组内商户交易且满足其他条件 → 使用常规算法
- 排除商户分组(EXCLUDE): 满足其他条件且不是分组内商户交易 → 不使用常规算法
- 商户分组查询 T_USER_GROUP WHERE GROUP_TYPE=2(浮动汇率商户分组) AND DELETE_FLAG=1
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


# ==================== 查询器 ====================

class NonBenchmarkTradeQuery:
    """非基准交易剔除配置 - 凭证数据查询器"""

    SELECT_COLS = [
        'ID', 'USER_NO', 'TRADE_TYPE', 'RECEIPT_NO', 'REQUEST_NO',
        'SOURCE_CURRENCY', 'TARGET_CURRENCY', 'TRADE_DIRECTION',
        'EXCHANGE_RATE', 'SALE_AMOUNT', 'BUY_AMOUNT', 'TRADE_DATE',
        'TRADE_TIME', 'STATUS', 'CUR_VERSION', 'CREATE_AT', 'CREATE_BY',
        'UPDATE_AT', 'UPDATE_BY', 'CLOSING_TYPE', 'CLOSING_DATE',
        'ORDER_GEP_RATE', 'ORIGINAL_CCY_PAIR', 'BUSINESS_TYPE'
    ]

    def __init__(self, env: str, start_time: str, end_time: str,
                 source_ccy: str, target_ccy: str):
        self.env = env
        self.start_time = start_time
        self.end_time = end_time
        self.source_currency = source_ccy
        self.target_currency = target_ccy

    def _normalize(self, result) -> List[Dict]:
        """统一返回为 dict 列表"""
        if not result or not isinstance(result, list):
            return []
        if isinstance(result[0], dict):
            return result
        return []

    def _map_direction(self, sell_ccy: str, buy_ccy: str) -> Tuple[int, str]:
        """
        根据配置的 SELL_CCY/BUY_CCY 映射到 T_TRADE_RECEIPT.TRADE_DIRECTION
        返回 (trade_direction, 方向标签)
        """
        if sell_ccy == self.target_currency and buy_ccy == self.source_currency:
            # SELL=VND, BUY=USD → 用户卖出VND买入USD → 买入方向(收款)
            return 1, "卖出VND/买入USD → 买入方向(收款)"
        else:
            # SELL=USD, BUY=VND → 用户卖出USD买入VND → 卖出方向(付款)
            return 2, "卖出USD/买入VND → 卖出方向(付款)"

    # ==================== Step 1: 查询启用配置 ====================

    def get_enabled_configs(self) -> List[Dict]:
        sql = """
            SELECT ID, BUSINESS_LINE, TRADE_TYPE, CURRENCY_PAIR, SELL_CCY, BUY_CCY,
                   INCLUDE_MERCHANT_GROUP, EXCLUDE_MERCHANT_GROUP, STATUS,
                   CREATE_AT, CREATE_BY, UPDATE_AT, UPDATE_BY
            FROM BAOFU_TRADE.T_NON_BENCHMARK_TRADE_EXCLUDE_CONFIG
            WHERE STATUS = 'ENABLE'
            ORDER BY ID
        """
        result = execute_db(self.env, sql)
        return self._normalize(result)

    def display_configs(self, configs: List[Dict]):
        """按方向分组展示配置"""
        cprint(f"\n[1] 启用配置查询 (共 {len(configs)} 条)", Clr.BOLD)

        # 按方向分组
        buy_direction = []   # SELL=VND/BUY=USD → 买入方向
        sell_direction = []  # SELL=USD/BUY=VND → 卖出方向
        for cfg in configs:
            sell_ccy = cfg.get('SELL_CCY', '')
            if sell_ccy == self.target_currency:
                buy_direction.append(cfg)
            else:
                sell_direction.append(cfg)

        # 卖出VND/买入USD (买入方向)
        cprint(f"\n  ▼ 卖出VND / 买入USD (买入方向/收款, TRADE_DIRECTION=1) - {len(buy_direction)} 条", Clr.YELLOW)
        if buy_direction:
            for cfg in buy_direction:
                self._print_config(cfg)
        else:
            print(f"    （无）")

        # 卖出USD/买入VND (卖出方向)
        cprint(f"\n  ▼ 卖出USD / 买入VND (卖出方向/付款, TRADE_DIRECTION=2) - {len(sell_direction)} 条", Clr.YELLOW)
        if sell_direction:
            for cfg in sell_direction:
                self._print_config(cfg)
        else:
            print(f"    （无）")

        cprint(f"\n  注: 两个方向成对出现，同方向可能有多条配置(不同商户分组)，结果取并集", Clr.CYAN)

    def _print_config(self, cfg: Dict):
        include_g = cfg.get('INCLUDE_MERCHANT_GROUP') or ''
        exclude_g = cfg.get('EXCLUDE_MERCHANT_GROUP') or ''
        if include_g:
            group_info = f"指定分组={include_g} (常规算法)"
            group_color = Clr.GREEN
        elif exclude_g:
            group_info = f"排除分组={exclude_g} (非基准算法)"
            group_color = Clr.RED
        else:
            group_info = "无分组限制"
            group_color = ''

        print(f"    ID={cfg.get('ID')} | 业务线={cfg.get('BUSINESS_LINE')} | "
              f"交易类型={cfg.get('TRADE_TYPE')} | {colored(group_info, group_color)}")

    # ==================== Step 2: 逐配置查询凭证 ====================

    def query_receipts_by_config(self, cfg: Dict, include_direction: bool = True) -> List[Dict]:
        """
        根据单条配置查询 T_TRADE_RECEIPT
        include_direction=True: 加 TRADE_DIRECTION 条件（符合配置查询）
        include_direction=False: 不加 TRADE_DIRECTION（对比查询，查该配置所有方向数据）
        """
        sell_ccy = cfg.get('SELL_CCY', '')
        buy_ccy = cfg.get('BUY_CCY', '')
        trade_direction, dir_label = self._map_direction(sell_ccy, buy_ccy)

        # 解析多选字段
        trade_types = [t.strip() for t in str(cfg.get('TRADE_TYPE', '')).split(',') if t.strip()]
        business_lines = [b.strip() for b in str(cfg.get('BUSINESS_LINE', '')).split(',') if b.strip()]
        include_groups = [g.strip() for g in str(cfg.get('INCLUDE_MERCHANT_GROUP', '') or '').split(',') if g.strip()]
        exclude_groups = [g.strip() for g in str(cfg.get('EXCLUDE_MERCHANT_GROUP', '') or '').split(',') if g.strip()]

        # 打印配置解析
        mode_label = "符合配置(加方向)" if include_direction else "对比查询(不加方向)"
        cprint(f"\n  ▶ 配置 ID={cfg.get('ID')} | {dir_label} | {mode_label}", Clr.CYAN)
        print(f"      业务线(BUSINESS_LINE)→BUSINESS_TYPE: {business_lines}")
        print(f"      交易类型(TRADE_TYPE): {trade_types}")
        if include_direction:
            print(f"      方向: TRADE_DIRECTION={trade_direction}")
        else:
            print(f"      方向: {Clr.YELLOW}不加 TRADE_DIRECTION (查所有方向){Clr.END}")
        if include_groups:
            print(f"      {Clr.GREEN}指定商户分组(INCLUDE): {include_groups} → exists (常规算法){Clr.END}")
        elif exclude_groups:
            print(f"      {Clr.RED}排除商户分组(EXCLUDE): {exclude_groups} → not exists (非基准算法){Clr.END}")
        else:
            print(f"      无商户分组限制")

        # 构建 SQL
        cols = ', '.join(self.SELECT_COLS)
        where = """
            WHERE receipt.CREATE_AT >= %s AND receipt.CREATE_AT <= %s
              AND receipt.SOURCE_CURRENCY = %s AND receipt.TARGET_CURRENCY = %s
        """
        params = [self.start_time, self.end_time,
                  self.source_currency, self.target_currency]

        if include_direction:
            where += " AND receipt.TRADE_DIRECTION = %s"
            params.append(trade_direction)

        where += " AND receipt.STATUS != -1"

        # TRADE_TYPE IN (...)
        if trade_types:
            tt_ph = ', '.join(['%s'] * len(trade_types))
            where += f" AND receipt.TRADE_TYPE IN ({tt_ph})"
            params.extend(trade_types)

        # BUSINESS_TYPE IN (...)
        if business_lines:
            bl_ph = ', '.join(['%s'] * len(business_lines))
            where += f" AND receipt.BUSINESS_TYPE IN ({bl_ph})"
            params.extend(business_lines)

        # 商户分组
        if include_groups:
            ig_ph = ', '.join(['%s'] * len(include_groups))
            where += f"""
              AND exists (
                select 1 from BAOFU_CRM.T_USER_GROUP userGroup
                where userGroup.GROUP_ID IN ({ig_ph})
                  and userGroup.GROUP_TYPE = 2
                  and userGroup.DELETE_FLAG = 1
                  and receipt.USER_NO = userGroup.USER_NO
              )
            """
            params.extend(include_groups)
        elif exclude_groups:
            eg_ph = ', '.join(['%s'] * len(exclude_groups))
            where += f"""
              AND not exists (
                select 1 from BAOFU_CRM.T_USER_GROUP userGroup
                where userGroup.GROUP_ID IN ({eg_ph})
                  and userGroup.GROUP_TYPE = 2
                  and userGroup.DELETE_FLAG = 1
                  and receipt.USER_NO = userGroup.USER_NO
              )
            """
            params.extend(exclude_groups)

        sql = f"SELECT {cols} FROM BAOFU_TRADE.T_TRADE_RECEIPT receipt {where} ORDER BY receipt.TRADE_TIME ASC"
        result = execute_db(self.env, sql, params=tuple(params))
        data = self._normalize(result)
        print(f"      → 查询结果: {colored(len(data), Clr.GREEN)} 条")
        return data

    # ==================== Step 3: 并集展示 ====================

    def display_union_results(self, all_records: Dict):
        cprint(f"\n[3] 并集结果 (按 ID 去重)", Clr.BOLD)
        total = len(all_records)
        cprint(f"    去重后总计: {colored(total, Clr.GREEN)} 条凭证", Clr.YELLOW)

        if total == 0:
            return

        # 按方向统计
        dir1 = [r for r in all_records.values() if r.get('TRADE_DIRECTION') == 1]
        dir2 = [r for r in all_records.values() if r.get('TRADE_DIRECTION') == 2]
        print(f"    - 收--买入方向(SELL=VND): {len(dir1)} 条")
        print(f"    - 付--卖出方向(SELL=USD): {len(dir2)} 条")

        cprint(f"\n    凭证明细 (符合配置):", Clr.BOLD)
        for rec in all_records.values():
            direction = rec.get('TRADE_DIRECTION')
            d_label = "收--买入方向" if direction == 1 else "付--卖出方向"
            d_color = Clr.GREEN if direction == 1 else Clr.YELLOW
            sale = rec.get('SALE_AMOUNT', 0)
            buy = rec.get('BUY_AMOUNT', 0)
            biz = rec.get('BUSINESS_TYPE', '')
            ttype = rec.get('TRADE_TYPE', '')
            print(f"      {colored(d_label, d_color)} | "
                  f"业务线={biz} | 交易类型={ttype} | "
                  f"RECEIPT_NO={rec.get('RECEIPT_NO')} | "
                  f"ID={rec.get('ID')} | USER_NO={rec.get('USER_NO')} | "
                  f"SALE={sale} | BUY={buy} | TRADE_TIME={rec.get('TRADE_TIME')}")

    # ==================== Step 4: 对比查询（仅不加方向，其他条件全保留） ====================

    def query_receipts_for_comparison(self, configs: List[Dict]) -> Dict:
        """
        对比查询：与 Step 2 完全相同的条件，仅不加 TRADE_DIRECTION
        商户分组/GROUP_TYPE=2/业务线/交易类型 等全部保留
        结果按 ID 并集去重
        """
        cprint(f"\n[4] 对比查询 (配置所有条件不变，仅不加 TRADE_DIRECTION)", Clr.BOLD)
        all_records = {}
        for cfg in configs:
            data = self.query_receipts_by_config(cfg, include_direction=False)
            for rec in data:
                rid = rec.get('ID')
                if rid is not None and rid not in all_records:
                    all_records[rid] = rec
        return all_records

    def display_comparison(self, comparison_records: Dict, matched_records: Dict):
        """
        对比展示：
        comparison_records: 配置所有条件(不含方向)查到的凭证
        matched_records: 符合配置(含方向)的凭证
        对比看哪些被方向过滤掉了
        """
        cprint(f"\n[5] 对比分析 (该货币对+业务线+交易类型，所有凭证数据)", Clr.BOLD)

        matched_ids = set(matched_records.keys())
        matched = [r for r in comparison_records.values() if r.get('ID') in matched_ids]
        unmatched = [r for r in comparison_records.values() if r.get('ID') not in matched_ids]

        cprint(f"    配置条件(不含方向): {colored(len(comparison_records), Clr.GREEN)} 条 | "
               f"符合配置(含方向): {colored(len(matched), Clr.GREEN)} 条 | "
               f"被方向过滤: {colored(len(unmatched), Clr.RED)} 条", Clr.YELLOW)

        # 不符合（被方向过滤掉的）
        cprint(f"\n    【不符合】(满足业务线+交易类型+分组，但方向不符合配置):", Clr.RED)
        if unmatched:
            for rec in unmatched:
                direction = rec.get('TRADE_DIRECTION')
                d_label = "收--买入方向" if direction == 1 else "付--卖出方向"
                biz = rec.get('BUSINESS_TYPE', '')
                ttype = rec.get('TRADE_TYPE', '')
                print(f"      {Clr.RED}【不符合】{Clr.END} 业务线={biz} 交易类型={ttype} | "
                      f"{d_label} | USER_NO={rec.get('USER_NO')} | "
                      f"凭证号={rec.get('RECEIPT_NO')} | ID={rec.get('ID')}")
        else:
            print(f"      （无）")

        # 符合
        cprint(f"\n    【符合】(完全符合配置的货币对+方向+业务线+交易类型+分组):", Clr.GREEN)
        if matched:
            for rec in matched:
                direction = rec.get('TRADE_DIRECTION')
                d_label = "收--买入方向" if direction == 1 else "付--卖出方向"
                biz = rec.get('BUSINESS_TYPE', '')
                ttype = rec.get('TRADE_TYPE', '')
                print(f"      {Clr.GREEN}【符合】{Clr.END} 业务线={biz} 交易类型={ttype} | "
                      f"{d_label} | USER_NO={rec.get('USER_NO')} | "
                      f"凭证号={rec.get('RECEIPT_NO')} | ID={rec.get('ID')}")
            # 凭证号汇总（方便复制到收付对冲损益计算工具）
            matched_nos = [r.get('RECEIPT_NO') for r in matched]
            recv_nos = [r.get('RECEIPT_NO') for r in matched if r.get('TRADE_DIRECTION') == 1]
            pay_nos = [r.get('RECEIPT_NO') for r in matched if r.get('TRADE_DIRECTION') == 2]
            cprint(f"\n    凭证号汇总 ({len(matched_nos)}条):", Clr.CYAN)
            print(f"      test_receipt_nos = {matched_nos}")
            print(f"      - 收--买入方向({len(recv_nos)}条): {recv_nos}")
            print(f"      - 付--卖出方向({len(pay_nos)}条): {pay_nos}")
        else:
            print(f"      （无）")

    # ==================== 主流程 ====================

    def run(self):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"\n{'='*18} {start_time} {'='*(80-18-2-len(start_time))}", Clr.CYAN)
        cprint(f"【非基准交易剔除配置-凭证查询】 环境: {self.env}  币种对: {self.source_currency}/{self.target_currency}", Clr.BOLD)
        print(f"时间范围: {self.start_time} ~ {self.end_time}")
        cprint(f"{'='*80}", Clr.CYAN)

        # 1. 查询启用配置
        configs = self.get_enabled_configs()
        if not configs:
            cprint(">>> 未查到启用的配置", Clr.RED)
            return

        self.display_configs(configs)

        # 2. 逐配置查询凭证
        cprint(f"\n[2] 逐配置查询凭证数据", Clr.BOLD)
        all_records = {}  # ID -> record, 自动去重
        for cfg in configs:
            data = self.query_receipts_by_config(cfg)
            for rec in data:
                rid = rec.get('ID')
                if rid is not None and rid not in all_records:
                    all_records[rid] = rec

        # 3. 并集展示
        self.display_union_results(all_records)

        # 4. 对比查询：按配置查但不加 TRADE_DIRECTION
        without_dir_records = self.query_receipts_for_comparison(configs)

        # 5. 对比分析：不加方向 vs 加方向
        self.display_comparison(without_dir_records, all_records)

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"\n{'='*18} {end_time} {'='*(80-18-2-len(end_time))}\n", Clr.CYAN)


# ==================== 入口 ====================

if __name__ == "__main__":
    db_env = 'UAT'
    start_time = '2026-06-25 00:00:00'
    end_time = '2026-06-25 23:59:59'
    source_ccy = 'USD'
    target_ccy = 'VND' 

    # source_ccy = 'THB'
    # target_ccy = 'CNH' 
    query = NonBenchmarkTradeQuery(
        env=db_env,
        start_time=start_time,
        end_time=end_time,
        source_ccy=source_ccy,
        target_ccy=target_ccy,
    )
    query.run()
