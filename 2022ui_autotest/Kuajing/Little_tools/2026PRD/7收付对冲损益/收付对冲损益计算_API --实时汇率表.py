# -*- coding: utf-8 -*-
"""
收付对冲损益计算工具
用于计算指定订单的收付对冲损益

逻辑说明：
1. 平均销售成本：target/source（卖出target金额/买入source金额）。
2. 收付平均销售成本 = (收款平均销售成本 + 付款平均销售成本) / 2。
3. 渠道平均成本汇率：根据收付情况，只查询用到方向的配置和汇率。
4. 损益计价币种 = 货币对中"非小币种"（小币种列表: VND/THB/IDR）。
   - USD/VND: VND小 → 损益算USD(source)
   - THB/CNH: THB小 → 损益算CNH(target)
5. 损益按每条记录维度计算：
   - source计价: 收款=target/汇率-source；付款=source-target/汇率
   - target计价: 收款=target-source*汇率；付款=source*汇率-target
6. 三种对冲情况：根据收付target金额大小关系，对等部分按收付平均销售成本，剩余部分按渠道平均成本。
"""

from Kuajing.Common.kjMysql import execute_db
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
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


# ==================== 计算器 ====================

class HedgeProfitCalculator:
    """收付对冲损益计算器"""

    def __init__(self, env: str, source_ccy: str, target_ccy: str,
                 rate_mode: str = 'table', fixed_recv_rate=None, fixed_pay_rate=None):
        """
        rate_mode: 'table' 查表汇率 / 'fixed' 固定传值汇率
        fixed_recv_rate: 固定收款渠道成本汇率（rate_mode='fixed' 时使用）
        fixed_pay_rate:   固定付款渠道成本汇率（rate_mode='fixed' 时使用）
        """
        self.env = env
        self.source_currency = source_ccy
        self.target_currency = target_ccy
        self.rate_mode = rate_mode
        self.fixed_recv_rate = self.safe_decimal(fixed_recv_rate) if fixed_recv_rate is not None else None
        self.fixed_pay_rate = self.safe_decimal(fixed_pay_rate) if fixed_pay_rate is not None else None

    def safe_decimal(self, value, default='0') -> Decimal:
        if value is None:
            return Decimal(default)
        try:
            return Decimal(str(value))
        except:
            return Decimal(default)

    # ==================== 数据库查询 ====================

    def get_receipt_data(self, receipt_nos: List[str]) -> List[Dict]:
        if not receipt_nos:
            return []

        placeholders = ', '.join(['%s'] * len(receipt_nos))
        sql = f"""
            SELECT ID, RECEIPT_NO, TRADE_DIRECTION, EXCHANGE_RATE,
                   SALE_AMOUNT, BUY_AMOUNT, SOURCE_CURRENCY, TARGET_CURRENCY,
                   TRADE_TIME, USER_NO
            FROM BAOFU_TRADE.T_TRADE_RECEIPT
            WHERE RECEIPT_NO IN ({placeholders})
              AND SOURCE_CURRENCY = %s AND TARGET_CURRENCY = %s
              AND STATUS != -1
            ORDER BY TRADE_TIME ASC
        """
        params = tuple(receipt_nos) + (self.source_currency, self.target_currency)
        result = execute_db(self.env, sql, params=params)

        data_list = []
        if result and isinstance(result, list):
            if isinstance(result[0], dict):
                data_list = result
            else:
                cols = ['ID', 'RECEIPT_NO', 'TRADE_DIRECTION', 'EXCHANGE_RATE',
                        'SALE_AMOUNT', 'BUY_AMOUNT', 'SOURCE_CURRENCY', 'TARGET_CURRENCY',
                        'TRADE_TIME', 'USER_NO']
                for row in result:
                    data_list.append(dict(zip(cols, row)))
        return data_list

    def get_channel_avg_cost_rate(self, used_direction: str) -> Dict:
        """
        获取渠道平均成本汇率（在知道用哪个方向后调用）
        used_direction: 'receive'（买入方向）或 'pay'（卖出方向）

        返回: {'receive_channel_rate': Decimal, 'pay_channel_rate': Decimal, 'detail': dict}
        """
        cprint(f"\n{'─'*80}", Clr.CYAN)

        # ===== 固定传值汇率模式 =====
        if self.rate_mode == 'fixed':
            cprint("【渠道平均成本汇率 - 固定传值汇率模式】", Clr.BOLD)
            recv_rate = self.fixed_recv_rate if self.fixed_recv_rate is not None else Decimal('0')
            pay_rate = self.fixed_pay_rate if self.fixed_pay_rate is not None else Decimal('0')
            print(f"  收款渠道成本汇率(固定传值): {recv_rate}")
            print(f"  付款渠道成本汇率(固定传值): {pay_rate}")
            print(f"  使用方向: {'买入方向(receive)' if used_direction == 'receive' else '卖出方向(pay)'}")
            cprint(f"{'─'*80}\n", Clr.CYAN)
            return {'receive_channel_rate': recv_rate,
                    'pay_channel_rate': pay_rate, 'detail': {'mode': 'fixed'}}

        # ===== 查表汇率模式 =====
        cprint("【渠道平均成本汇率查询 - 查表汇率模式】", Clr.BOLD)
        detail = {}
        RATE_COLS = ['ID', 'RECORD_ID', 'CHANNEL_ID', 'SOURCE_CCY', 'DEST_CCY',
                     'TRADE_DIRECTION', 'TRADE_RATE', 'DISCOUNT_RATE', 'DISCOUNT_RATE_BP',
                     'RATE_QUERY_DATE', 'QUERY_BATCH_NO', 'CLOSING_TYPE', 'RATE_DATE',
                     'CAL_RATE', 'STATUS', 'REMARKS', 'CREATE_AT', 'CREATE_BY',
                     'UPDATE_AT', 'UPDATE_BY']
        use_buy = (used_direction == 'receive')

        # ==== Step 1: 配置表 ====
        cprint("\n[Step 1] 查询渠道配置表 BAOFU_CBCA.T_CHANNEL_AVG_COST_RATE_CONFIG", Clr.YELLOW)

        # 买入方向
        buy_config = execute_db(self.env, """
            SELECT * FROM BAOFU_CBCA.T_CHANNEL_AVG_COST_RATE_CONFIG
            WHERE SELL_CURRENCY = %s AND BUY_CURRENCY = %s AND STATUS LIKE %s
            ORDER BY ID DESC LIMIT 1
        """, params=(self.target_currency, self.source_currency, '%OPEN%'))

        symbol_buy = '✅' if use_buy else '  '
        symbol_sell = '✅' if not use_buy else '  '
        tag_buy = colored('← 本次使用', Clr.GREEN) if use_buy else ''
        tag_sell = colored('← 本次使用', Clr.GREEN) if not use_buy else ''

        print(f"  {symbol_buy} [买入] SELL={self.target_currency}, BUY={self.source_currency} {tag_buy}")
        if buy_config and isinstance(buy_config, list) and len(buy_config) > 0:
            buy_cfg = buy_config[0] if isinstance(buy_config[0], dict) else buy_config[0]
            if isinstance(buy_cfg, (list, tuple)):
                buy_cfg = dict(zip(
                    ['ID', 'RECORD_ID', 'SELL_CURRENCY', 'BUY_CURRENCY', 'RATE_RESOURCE',
                     'RATE_BP', 'BP_UNIT', 'STATUS', 'CREATE_AT', 'CREATE_BY',
                     'UPDATE_AT', 'UPDATE_BY'], buy_cfg))
            detail['buy_config'] = buy_cfg
            print(f"     RECORD_ID={buy_cfg.get('RECORD_ID')}, "
                  f"RATE_RESOURCE={buy_cfg.get('RATE_RESOURCE')}, "
                  f"RATE_BP={buy_cfg.get('RATE_BP')}, BP_UNIT={buy_cfg.get('BP_UNIT')}")
        else:
            print(f"     ❌ 未查到买入方向渠道配置!")
            detail['buy_config'] = {}

        # 卖出方向
        sell_config = execute_db(self.env, """
            SELECT * FROM BAOFU_CBCA.T_CHANNEL_AVG_COST_RATE_CONFIG
            WHERE SELL_CURRENCY = %s AND BUY_CURRENCY = %s AND STATUS LIKE %s
            ORDER BY ID DESC LIMIT 1
        """, params=(self.source_currency, self.target_currency, '%OPEN%'))

        print(f"  {symbol_sell} [卖出] SELL={self.source_currency}, BUY={self.target_currency} {tag_sell}")
        if sell_config and isinstance(sell_config, list) and len(sell_config) > 0:
            sell_cfg = sell_config[0] if isinstance(sell_config[0], dict) else sell_config[0]
            if isinstance(sell_cfg, (list, tuple)):
                sell_cfg = dict(zip(
                    ['ID', 'RECORD_ID', 'SELL_CURRENCY', 'BUY_CURRENCY', 'RATE_RESOURCE',
                     'RATE_BP', 'BP_UNIT', 'STATUS', 'CREATE_AT', 'CREATE_BY',
                     'UPDATE_AT', 'UPDATE_BY'], sell_cfg))
            detail['sell_config'] = sell_cfg
            print(f"     RECORD_ID={sell_cfg.get('RECORD_ID')}, "
                  f"RATE_RESOURCE={sell_cfg.get('RATE_RESOURCE')}, "
                  f"RATE_BP={sell_cfg.get('RATE_BP')}, BP_UNIT={sell_cfg.get('BP_UNIT')}")
        else:
            print(f"     ❌ 未查到卖出方向渠道配置!")
            detail['sell_config'] = {}

        # ==== Step 2: 实时汇率 ====
        cprint("\n[Step 2] 查询渠道汇率表 BAOFU_CGW.T_CHANNEL_RATE_REAL (TRADE_RATE/100)", Clr.YELLOW)
        receive_channel_rate = Decimal('0')
        pay_channel_rate = Decimal('0')

        # 买入方向
        if detail.get('buy_config'):
            ch_id = detail['buy_config'].get('RATE_RESOURCE', '')
            buy_rate = execute_db(self.env, """
                SELECT * FROM BAOFU_CGW.T_CHANNEL_RATE_REAL
                WHERE CHANNEL_ID = %s AND SOURCE_CCY = %s AND DEST_CCY LIKE %s
                  AND TRADE_DIRECTION = 2
                ORDER BY RECORD_ID DESC LIMIT 1
            """, params=(ch_id, self.source_currency, f'%{self.target_currency}%'))

            tag = colored('← 本次使用', Clr.GREEN) if use_buy else ''
            print(f"  {symbol_buy} CHANNEL_ID={ch_id}, TRADE_DIRECTION=2(渠道卖出) {tag}")
            if buy_rate and isinstance(buy_rate, list) and len(buy_rate) > 0:
                rate_row = buy_rate[0] if isinstance(buy_rate[0], dict) else buy_rate[0]
                if isinstance(rate_row, (list, tuple)):
                    rate_row = dict(zip(RATE_COLS, rate_row))
                detail['buy_rate'] = rate_row
                raw_rate = self.safe_decimal(rate_row.get('TRADE_RATE'))
                base_rate = raw_rate / Decimal('100')
                bp = self.safe_decimal(detail['buy_config'].get('RATE_BP'))
                bp_unit = detail['buy_config'].get('BP_UNIT')

                print(f"      TRADE_RATE(原始)={raw_rate}  →  /100  →  {base_rate}")
                if str(bp_unit) == '2':
                    receive_channel_rate = base_rate * (Decimal('1') + bp / Decimal('100'))
                    print(f"      BP_UNIT=2(%%): {base_rate} * (1 + {float(bp):g}/100) = {receive_channel_rate}")
                elif str(bp_unit) == '1':
                    receive_channel_rate = base_rate + bp / Decimal('10000')
                    print(f"      BP_UNIT=1(BP): {base_rate} + {float(bp):g}/10000 = {receive_channel_rate}")
                else:
                    receive_channel_rate = base_rate
            else:
                print(f"      ❌ 未查到实时汇率!")

        # 卖出方向
        if detail.get('sell_config'):
            ch_id = detail['sell_config'].get('RATE_RESOURCE', '')
            sell_rate = execute_db(self.env, """
                SELECT * FROM BAOFU_CGW.T_CHANNEL_RATE_REAL
                WHERE CHANNEL_ID = %s AND SOURCE_CCY = %s AND DEST_CCY LIKE %s
                  AND TRADE_DIRECTION = 1
                ORDER BY RECORD_ID DESC LIMIT 1
            """, params=(ch_id, self.source_currency, f'%{self.target_currency}%'))

            tag = colored('← 本次使用', Clr.GREEN) if not use_buy else ''
            print(f"  {symbol_sell} CHANNEL_ID={ch_id}, TRADE_DIRECTION=1(渠道买入) {tag}")
            if sell_rate and isinstance(sell_rate, list) and len(sell_rate) > 0:
                rate_row = sell_rate[0] if isinstance(sell_rate[0], dict) else sell_rate[0]
                if isinstance(rate_row, (list, tuple)):
                    rate_row = dict(zip(RATE_COLS, rate_row))
                detail['sell_rate'] = rate_row
                raw_rate = self.safe_decimal(rate_row.get('TRADE_RATE'))
                base_rate = raw_rate / Decimal('100')
                bp = self.safe_decimal(detail['sell_config'].get('RATE_BP'))
                bp_unit = detail['sell_config'].get('BP_UNIT')

                print(f"      TRADE_RATE(原始)={raw_rate}  →  /100  →  {base_rate}")
                if str(bp_unit) == '2':
                    pay_channel_rate = base_rate * (Decimal('1') - bp / Decimal('100'))
                    print(f"      BP_UNIT=2(%%): {base_rate} * (1 - {float(bp):g}/100) = {pay_channel_rate}")
                elif str(bp_unit) == '1':
                    pay_channel_rate = base_rate - bp / Decimal('10000')
                    print(f"      BP_UNIT=1(BP): {base_rate} - {float(bp):g}/10000 = {pay_channel_rate}")
                else:
                    pay_channel_rate = base_rate
            else:
                print(f"      ❌ 未查到实时汇率!")

        cprint(f"{'─'*80}\n", Clr.CYAN)
        return {'receive_channel_rate': receive_channel_rate,
                'pay_channel_rate': pay_channel_rate, 'detail': detail}

    # ==================== 汇总与计算 ====================

    def summarize_by_direction(self, data_list: List[Dict]) -> Dict:
        """
        按方向汇总
        方向定义（以 source_ccy 为准）：
        - TRADE_DIRECTION=1（收款/买入方向）: SALE=target_ccy, BUY=source_ccy
        - TRADE_DIRECTION=2（付款/卖出方向）: SALE=source_ccy, BUY=target_ccy
        """
        summary = {
            'receive': {'records': [], 'total_target': Decimal('0'), 'total_source': Decimal('0')},
            'pay':     {'records': [], 'total_target': Decimal('0'), 'total_source': Decimal('0')},
        }
        for record in data_list:
            direction = record.get('TRADE_DIRECTION')
            sale_amt = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
            buy_amt = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
            if direction == 1:
                summary['receive']['records'].append(record)
                summary['receive']['total_target'] += sale_amt
                summary['receive']['total_source'] += buy_amt
            elif direction == 2:
                summary['pay']['records'].append(record)
                summary['pay']['total_source'] += sale_amt
                summary['pay']['total_target'] += buy_amt
        return summary

    def calc_avg_cost(self, target_amt: Decimal, source_amt: Decimal) -> Decimal:
        if source_amt == 0:
            return Decimal('0')
        return target_amt / source_amt

    # ==================== 损益币种与计算辅助 ====================

    # 小币种列表：命中则损益取另一币种计价
    SMALL_CURRENCIES = {'VND', 'THB', 'IDR'}

    def determine_profit_currency(self):
        """
        根据小币种列表确定损益计价币种。损益以货币对中"非小币种"计价。
          - USD/VND: VND小 → 损益算USD(source)
          - THB/CNH: THB小 → 损益算CNH(target)
        返回: (profit_ccy, profit_in_source, err_msg)
          profit_in_source=True  → 损益以source计价
          profit_in_source=False → 损益以target计价
        """
        src = self.source_currency
        tgt = self.target_currency
        src_small = src in self.SMALL_CURRENCIES
        tgt_small = tgt in self.SMALL_CURRENCIES
        if src_small and tgt_small:
            return None, None, f"{src}和{tgt}都是小币种，无法确定损益单位"
        if not src_small and not tgt_small:
            return None, None, f"{src}和{tgt}都不是小币种，无法确定损益单位"
        if src_small:
            return tgt, False, None   # source是小币种 → 损益算target
        return src, True, None        # target是小币种 → 损益算source

    def _recv_profit(self, target_amt: Decimal, source_amt: Decimal,
                     rate: Decimal, pis: bool):
        """收款方向(卖出target买入source)损益. 返回(mid, profit)"""
        if pis:
            # source计价: target/rate - source
            mid = target_amt / rate
            return mid, mid - source_amt
        # target计价: target - source*rate
        mid = source_amt * rate
        return mid, target_amt - mid

    def _pay_profit(self, target_amt: Decimal, source_amt: Decimal,
                    rate: Decimal, pis: bool):
        """付款方向(买入target卖出source)损益. 返回(mid, profit)"""
        if pis:
            # source计价: source - target/rate
            mid = target_amt / rate
            return mid, source_amt - mid
        # target计价: source*rate - target
        mid = source_amt * rate
        return mid, mid - target_amt

    def _print_simple_profit(self, receipt_no, target_amt: Decimal, source_amt: Decimal,
                             rate: Decimal, is_receive: bool, pis: bool, profit_ccy: str):
        """全对冲(单一汇率)损益打印"""
        tgt = self.target_currency
        src = self.source_currency
        if is_receive:
            mid, profit = self._recv_profit(target_amt, source_amt, rate, pis)
        else:
            mid, profit = self._pay_profit(target_amt, source_amt, rate, pis)
        p_color = Clr.GREEN if profit >= 0 else Clr.RED
        print(f"    {receipt_no}: {tgt} {target_amt:,.0f} | {src} {source_amt:,.2f}")
        if is_receive:
            if pis:
                print(f"      → 销售损益 = {target_amt:,.0f}/{rate:.4f} - {source_amt:,.2f}")
                print(f"                 = {mid:,.4f} - {source_amt:,.2f}"
                      f" = {p_color}{profit:,.4f} {profit_ccy}{Clr.END}")
            else:
                print(f"      → 销售损益 = {target_amt:,.0f} - {source_amt:,.2f}*{rate:.4f}")
                print(f"                 = {target_amt:,.0f} - {mid:,.4f}"
                      f" = {p_color}{profit:,.4f} {profit_ccy}{Clr.END}")
        else:
            if pis:
                print(f"      → 销售损益 = {source_amt:,.2f} - {target_amt:,.0f}/{rate:.4f}")
                print(f"                 = {source_amt:,.2f} - {mid:,.4f}"
                      f" = {p_color}{profit:,.4f} {profit_ccy}{Clr.END}")
            else:
                print(f"      → 销售损益 = {source_amt:,.2f}*{rate:.4f} - {target_amt:,.0f}")
                print(f"                 = {mid:,.4f} - {target_amt:,.0f}"
                      f" = {p_color}{profit:,.4f} {profit_ccy}{Clr.END}")

    def _print_split_profit(self, receipt_no, target_amt: Decimal, source_amt: Decimal,
                            ratio: Decimal, hedge_rate: Decimal, channel_rate: Decimal,
                            is_receive: bool, pis: bool, profit_ccy: str):
        """对冲+渠道拆分损益打印 (情况1收款 / 情况2付款)"""
        tgt = self.target_currency
        src = self.source_currency
        hedge_target = target_amt * ratio
        remain_target = target_amt - hedge_target
        hedge_source = source_amt * ratio
        remain_source = source_amt - hedge_source
        pct = Decimal('1') - ratio

        if is_receive:
            h_mid, h_profit = self._recv_profit(hedge_target, hedge_source, hedge_rate, pis)
            r_mid, r_profit = self._recv_profit(remain_target, remain_source, channel_rate, pis)
        else:
            h_mid, h_profit = self._pay_profit(hedge_target, hedge_source, hedge_rate, pis)
            r_mid, r_profit = self._pay_profit(remain_target, remain_source, channel_rate, pis)

        p_total = h_profit + r_profit
        p_color = Clr.GREEN if p_total >= 0 else Clr.RED
        print(f"    {receipt_no}: {tgt} {target_amt:,.0f} | {src} {source_amt:,.2f}")
        # ---- 对冲部分 ----
        if is_receive:
            if pis:
                print(f"      → 对冲部分: 销售损益 = {target_amt:,.0f}*{ratio:.4%}/{hedge_rate:.4f} - {source_amt:,.2f}*{ratio:.4%}")
                print(f"                   = {hedge_target:,.0f}/{hedge_rate:.4f} - {hedge_source:,.2f}")
                print(f"                   = {h_mid:,.4f} - {hedge_source:,.2f} = {h_profit:,.4f} {profit_ccy}")
            else:
                print(f"      → 对冲部分: 销售损益 = {target_amt:,.0f}*{ratio:.4%} - {source_amt:,.2f}*{ratio:.4%}*{hedge_rate:.4f}")
                print(f"                   = {hedge_target:,.0f} - {hedge_source:,.2f}*{hedge_rate:.4f}")
                print(f"                   = {hedge_target:,.0f} - {h_mid:,.4f} = {h_profit:,.4f} {profit_ccy}")
        else:
            if pis:
                print(f"      → 对冲部分: 销售损益 = {source_amt:,.2f}*{ratio:.4%} - {target_amt:,.0f}*{ratio:.4%}/{hedge_rate:.4f}")
                print(f"                   = {hedge_source:,.2f} - {hedge_target:,.0f}/{hedge_rate:.4f}")
                print(f"                   = {hedge_source:,.2f} - {h_mid:,.4f} = {h_profit:,.4f} {profit_ccy}")
            else:
                print(f"      → 对冲部分: 销售损益 = {source_amt:,.2f}*{ratio:.4%}*{hedge_rate:.4f} - {target_amt:,.0f}*{ratio:.4%}")
                print(f"                   = {hedge_source:,.2f}*{hedge_rate:.4f} - {hedge_target:,.0f}")
                print(f"                   = {h_mid:,.4f} - {hedge_target:,.0f} = {h_profit:,.4f} {profit_ccy}")
        # ---- 渠道剩余 ----
        if is_receive:
            if pis:
                print(f"      → 渠道剩余: 销售损益 = {target_amt:,.0f}*{pct:.4%}/{channel_rate:.4f} - {source_amt:,.2f}*{pct:.4%}")
                print(f"                   = {remain_target:,.0f}/{channel_rate:.4f} - {remain_source:,.2f}")
                print(f"                   = {r_mid:,.4f} - {remain_source:,.2f} = {r_profit:,.4f} {profit_ccy}")
            else:
                print(f"      → 渠道剩余: 销售损益 = {target_amt:,.0f}*{pct:.4%} - {source_amt:,.2f}*{pct:.4%}*{channel_rate:.4f}")
                print(f"                   = {remain_target:,.0f} - {remain_source:,.2f}*{channel_rate:.4f}")
                print(f"                   = {remain_target:,.0f} - {r_mid:,.4f} = {r_profit:,.4f} {profit_ccy}")
        else:
            if pis:
                print(f"      → 渠道剩余: 销售损益 = {source_amt:,.2f}*{pct:.4%} - {target_amt:,.0f}*{pct:.4%}/{channel_rate:.4f}")
                print(f"                   = {remain_source:,.2f} - {remain_target:,.0f}/{channel_rate:.4f}")
                print(f"                   = {remain_source:,.2f} - {r_mid:,.4f} = {r_profit:,.4f} {profit_ccy}")
            else:
                print(f"      → 渠道剩余: 销售损益 = {source_amt:,.2f}*{pct:.4%}*{channel_rate:.4f} - {target_amt:,.0f}*{pct:.4%}")
                print(f"                   = {remain_source:,.2f}*{channel_rate:.4f} - {remain_target:,.0f}")
                print(f"                   = {r_mid:,.4f} - {remain_target:,.0f} = {r_profit:,.4f} {profit_ccy}")
        print(f"      → 该笔记损 = {h_profit:,.4f} + {r_profit:,.4f}"
              f" = {p_color}{p_total.quantize(Decimal('0.01'), ROUND_HALF_UP)} {profit_ccy}{Clr.END}")

    # ==================== 主计算 ====================

    def calculate_hedge_profit(self, receipt_nos: List[str]):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"\n{'='*18} {start_time} {'='*(80-18-2-len(start_time))}", Clr.CYAN)
        cprint(f"【收付对冲损益分析】 币种对: {self.source_currency}/{self.target_currency}  环境: {self.env}", Clr.BOLD)
        print(f"查询订单: {receipt_nos}")
        cprint(f"{'='*80}", Clr.CYAN)

        # 1. 交易数据
        data_list = self.get_receipt_data(receipt_nos)
        if not data_list:
            cprint(">>> 错误: 未查询到符合条件的订单数据", Clr.RED)
            return

        summary = self.summarize_by_direction(data_list)
        rec = summary['receive']
        pay = summary['pay']

        # 2. 平均销售成本
        rec_avg_cost = self.calc_avg_cost(rec['total_target'], rec['total_source'])
        pay_avg_cost = self.calc_avg_cost(pay['total_target'], pay['total_source'])

        # 3. 收付平均销售成本
        if rec_avg_cost > 0 and pay_avg_cost > 0:
            hedge_cost = (rec_avg_cost + pay_avg_cost) / Decimal('2')
        else:
            hedge_cost = rec_avg_cost if rec_avg_cost > 0 else pay_avg_cost

        src = self.source_currency
        tgt = self.target_currency
        label_rec = f"收款客户（卖出{tgt}）--买入方向"
        label_pay = f"付款客户（买入{tgt}）--卖出方向"
        # 损益计价币种（取货币对中非小币种）
        profit_ccy, pis, err = self.determine_profit_currency()
        if err:
            cprint(f">>> 错误: {err}", Clr.RED)
            return

        # 对冲判定用小币种金额比较（target是小币种→用target；source是小币种→用source）
        if pis:
            small_ccy = tgt
            v_rec = rec['total_target']
            v_pay = pay['total_target']
        else:
            small_ccy = src
            v_rec = rec['total_source']
            v_pay = pay['total_source']

        # ---- 汇总 ----
        cprint(f"\n[1] 数据汇总统计:", Clr.BOLD)
        print(f"    - {label_rec}: {tgt} {rec['total_target']:,.2f} | {src} {rec['total_source']:,.2f} "
              f"| 平均销售成本 = {rec['total_target']:,.0f} / {rec['total_source']:,.2f} = {rec_avg_cost:.4f}")
        print(f"    - {label_pay}: {tgt} {pay['total_target']:,.2f} | {src} {pay['total_source']:,.2f} "
              f"| 平均销售成本 = {pay['total_target']:,.0f} / {pay['total_source']:,.2f} = {pay_avg_cost:.4f}")
        cprint(f"    - 收付平均销售成本 = ({rec_avg_cost:.4f} + {pay_avg_cost:.4f}) / 2 = {hedge_cost:.4f}", Clr.YELLOW)
        cprint(f"    - 损益计价币种: {profit_ccy} ({'source计价' if pis else 'target计价'})", Clr.YELLOW)
        # 凭证号汇总
        recv_nos = [r.get('RECEIPT_NO') for r in rec['records']]
        pay_nos = [r.get('RECEIPT_NO') for r in pay['records']]
        all_nos = recv_nos + pay_nos
        cprint(f"    凭证号列表: {all_nos}", Clr.CYAN)
        print(f"      - {label_rec}({len(recv_nos)}条): {recv_nos}")
        print(f"      - {label_pay}({len(pay_nos)}条): {pay_nos}")
        print(f"{'-'*80}")

        # ============ 情况1: 收 > 付 ============
        if v_rec > v_pay:
            ratio = v_pay / v_rec
            print(f"\n[2] 对冲判定: {Clr.YELLOW}情况1 (收--买入方向 > 付--卖出方向){Clr.END} → 使用 {Clr.RED}【买入方向】{Clr.END} 渠道汇率")
            print(f"    {label_rec}: {small_ccy} {v_rec:,.0f}")
            print(f"    {label_pay}: {small_ccy} {v_pay:,.0f}")
            print(f"    占比(付--卖出方向/收--买入方向) = {v_pay:,.0f} / {v_rec:,.0f} = {ratio:.4%}")

            # 查渠道（买入方向）
            channel_info = self.get_channel_avg_cost_rate(used_direction='receive')
            rec_channel_cost = channel_info['receive_channel_rate']
            pay_channel_cost = channel_info['pay_channel_rate']
            if rec_channel_cost == 0:
                cprint(">>> 错误: 未获取到买入方向渠道汇率", Clr.RED)
                return

            print(f"    收款渠道成本汇率: {rec_channel_cost:.4f}  |  付款渠道成本汇率: {pay_channel_cost:.4f} (未使用)")

            cprint(f"\n[3] 逐条损益明细 ({label_rec}):", Clr.BOLD)
            for record in rec['records']:
                r_target = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
                r_source = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
                self._print_split_profit(record.get('RECEIPT_NO'), r_target, r_source,
                                         ratio, hedge_cost, rec_channel_cost,
                                         is_receive=True, pis=pis, profit_ccy=profit_ccy)

            cprint(f"\n[4] 逐条损益明细 ({label_pay}):", Clr.BOLD)
            for record in pay['records']:
                p_target = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
                p_source = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
                self._print_simple_profit(record.get('RECEIPT_NO'), p_target, p_source,
                                          hedge_cost, is_receive=False, pis=pis, profit_ccy=profit_ccy)

        # ============ 情况2: 收 < 付 ============
        elif v_rec < v_pay:
            ratio = v_rec / v_pay
            print(f"\n[2] 对冲判定: {Clr.YELLOW}情况2 (收--买入方向 < 付--卖出方向){Clr.END} → 使用 {Clr.RED}【卖出方向】{Clr.END} 渠道汇率")
            print(f"    {label_rec}: {small_ccy} {v_rec:,.0f}")
            print(f"    {label_pay}: {small_ccy} {v_pay:,.0f}")
            print(f"    占比(收--买入方向/付--卖出方向) = {v_rec:,.0f} / {v_pay:,.0f} = {ratio:.4%}")

            # 查渠道（卖出方向）
            channel_info = self.get_channel_avg_cost_rate(used_direction='pay')
            rec_channel_cost = channel_info['receive_channel_rate']
            pay_channel_cost = channel_info['pay_channel_rate']
            if pay_channel_cost == 0:
                cprint(">>> 错误: 未获取到卖出方向渠道汇率", Clr.RED)
                return

            print(f"    收款渠道成本汇率: {rec_channel_cost:.4f} (未使用)  |  付款渠道成本汇率: {pay_channel_cost:.4f}")

            cprint(f"\n[3] 逐条损益明细 ({label_rec}):", Clr.BOLD)
            for record in rec['records']:
                r_target = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
                r_source = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
                self._print_simple_profit(record.get('RECEIPT_NO'), r_target, r_source,
                                          hedge_cost, is_receive=True, pis=pis, profit_ccy=profit_ccy)

            cprint(f"\n[4] 逐条损益明细 ({label_pay}):", Clr.BOLD)
            for record in pay['records']:
                p_target = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
                p_source = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
                self._print_split_profit(record.get('RECEIPT_NO'), p_target, p_source,
                                         ratio, hedge_cost, pay_channel_cost,
                                         is_receive=False, pis=pis, profit_ccy=profit_ccy)

        # ============ 情况3: 收 == 付 ============
        else:
            cprint(f"\n[2] 对冲判定: 情况3 (收--买入方向 == 付--卖出方向) → 不涉及渠道配置", Clr.YELLOW)
            print(f"    {label_rec}: {small_ccy} {v_rec:,.0f}")
            print(f"    {label_pay}: {small_ccy} {v_pay:,.0f}")
            print(f"    ❌ 无需查询渠道成本汇率，仅使用收付平均销售成本")

            cprint(f"\n[3] 逐条损益明细 ({label_rec}):", Clr.BOLD)
            for record in rec['records']:
                r_target = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
                r_source = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
                self._print_simple_profit(record.get('RECEIPT_NO'), r_target, r_source,
                                          hedge_cost, is_receive=True, pis=pis, profit_ccy=profit_ccy)

            cprint(f"\n[4] 逐条损益明细 ({label_pay}):", Clr.BOLD)
            for record in pay['records']:
                p_target = abs(self.safe_decimal(record.get('BUY_AMOUNT')))
                p_source = abs(self.safe_decimal(record.get('SALE_AMOUNT')))
                self._print_simple_profit(record.get('RECEIPT_NO'), p_target, p_source,
                                          hedge_cost, is_receive=False, pis=pis, profit_ccy=profit_ccy)

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cprint(f"{'='*18} {end_time} {'='*(80-18-2-len(end_time))}\n", Clr.CYAN)


# ==================== 入口 ====================

if __name__ == "__main__":
    db_env = 'UAT'
    # source_ccy = 'THB'
    # target_ccy = 'CNH'
    source_ccy = 'USD'
    target_ccy = 'VND'

    test_receipt_nos = [2606251514003214840, 2606251514003214839, 2606251513003214838, 26061716440035730901]

    # ==================== 汇率模式选择 ====================
    # rate_mode = 'table'   # 查表汇率（从数据库查询渠道成本汇率）
    rate_mode = 'fixed'     # 固定传值汇率（直接传入汇率值，不查数据库）

    # 固定传值汇率（仅 rate_mode='fixed' 时生效）
    fixed_pay_rate = '22762.699575000000'  # 付款渠道成本汇率（卖出方向）
    fixed_recv_rate = None                  # 收款渠道成本汇率（买入方向，None则默认按0处理）

    if rate_mode == 'table':
        calc = HedgeProfitCalculator(env=db_env, source_ccy=source_ccy, target_ccy=target_ccy,
                                     rate_mode='table')
    else:
        calc = HedgeProfitCalculator(env=db_env, source_ccy=source_ccy, target_ccy=target_ccy,
                                     rate_mode='fixed',
                                     fixed_recv_rate=fixed_recv_rate,
                                     fixed_pay_rate=fixed_pay_rate)

    calc.calculate_hedge_profit(test_receipt_nos)
