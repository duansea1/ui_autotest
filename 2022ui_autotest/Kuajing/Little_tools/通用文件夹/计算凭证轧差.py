"""
@Author    : duansea
@Date      : 2025/7/18 15:42
@Description: [计算凭证轧差统计工具]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Kuajing.Common.kjMysql import execute_db
from typing import Optional, List, Dict, Any


def parse_currency_pair(currency_pair: str) -> tuple:
    """
    解析货币对，返回源币种和目标币种
    """
    if not currency_pair:
        return None, None
    
    currency_pair = currency_pair.replace('/', '').strip()
    if len(currency_pair) >= 6:
        return currency_pair[:3], currency_pair[3:6]
    return None, None


def build_where_conditions(
    user_no: Optional[str] = None,
    source_currency: Optional[str] = None,
    target_currency: Optional[str] = None,
    currency_pair: Optional[str] = None,
    update_time_start: Optional[str] = None,
    update_time_end: Optional[str] = None,
    status: Optional[int] = 2
) -> tuple:
    """
    构建SQL WHERE条件
    """
    conditions = []
    params = []
    
    if user_no:
        conditions.append("USER_NO = %s")
        params.append(user_no)
    
    if currency_pair:
        src, tgt = parse_currency_pair(currency_pair)
        if src and tgt:
            source_currency = src
            target_currency = tgt
    
    if source_currency:
        conditions.append("SOURCE_CURRENCY = %s")
        params.append(source_currency)
    
    if target_currency:
        conditions.append("TARGET_CURRENCY = %s")
        params.append(target_currency)
    
    if update_time_start:
        conditions.append("UPDATE_AT >= %s")
        params.append(update_time_start)
    
    if update_time_end:
        conditions.append("UPDATE_AT <= %s")
        params.append(update_time_end)
    
    if status is not None:
        conditions.append("STATUS = %s")
        params.append(status)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    return where_clause, params


def get_receipt_netting(
    env: str,
    user_no: Optional[str] = None,
    source_currency: Optional[str] = None,
    target_currency: Optional[str] = None,
    currency_pair: Optional[str] = None,
    update_time_start: Optional[str] = None,
    update_time_end: Optional[str] = None,
    group_by_user: bool = False,
    group_by_currency: bool = True
) -> List[Dict[str, Any]]:
    """
    凭证轧差统计 - 通过参数控制统计维度
    """
    # 构建WHERE条件
    where_clause, params = build_where_conditions(
        user_no=user_no,
        source_currency=source_currency,
        target_currency=target_currency,
        currency_pair=currency_pair,
        update_time_start=update_time_start,
        update_time_end=update_time_end
    )
    
    # 生成详细的WHERE条件描述
    where_description = []
    if user_no:
        where_description.append(f"用户号 = '{user_no}'")
    if currency_pair:
        where_description.append(f"货币对 = '{currency_pair}'")
    elif source_currency or target_currency:
        if source_currency:
            where_description.append(f"源币种 = '{source_currency}'")
        if target_currency:
            where_description.append(f"目标币种 = '{target_currency}'")
    if update_time_start:
        where_description.append(f"更新时间 >= '{update_time_start}'")
    if update_time_end:
        where_description.append(f"更新时间 <= '{update_time_end}'")
    where_description.append("交易状态 = 2 (已完成)")
    where_desc_str = " AND ".join(where_description)
    
    group_fields = []
    select_fields = []
    
    if group_by_user:
        group_fields.append("USER_NO")
        select_fields.append("USER_NO")
    
    if group_by_currency:
        group_fields.extend(["SOURCE_CURRENCY", "TARGET_CURRENCY"])
        select_fields.append("CONCAT(SOURCE_CURRENCY, '/', TARGET_CURRENCY) AS CURRENCY_PAIR")
    
    group_clause = ", ".join(group_fields) if group_fields else None
    
    select_clause = ", ".join(select_fields) if select_fields else ""
    if select_clause:
        select_clause = select_clause + ", "
    
    sql = f"""
    -- 查询凭证轧差统计
    -- 筛选条件: {where_desc_str}
    -- 分组方式: {group_clause or '无分组'}
    
    SELECT 
        {select_clause}
        -- 方向统计
        SUM(CASE WHEN TRADE_DIRECTION = 1 THEN 1 ELSE 0 END) AS BUY_DIRECTION_COUNT,     -- 买入方向交易笔数
        SUM(CASE WHEN TRADE_DIRECTION = 2 THEN 1 ELSE 0 END) AS SELL_DIRECTION_COUNT,    -- 卖出方向交易笔数
        
        -- 买入方向金额
        SUM(CASE WHEN TRADE_DIRECTION = 1 THEN SALE_AMOUNT ELSE 0 END) AS BUY_DIRECTION_SALE_AMT,   -- 买入方向卖出金额
        SUM(CASE WHEN TRADE_DIRECTION = 1 THEN BUY_AMOUNT ELSE 0 END) AS BUY_DIRECTION_BUY_AMT,     -- 买入方向买入金额
        
        -- 卖出方向金额
        SUM(CASE WHEN TRADE_DIRECTION = 2 THEN SALE_AMOUNT ELSE 0 END) AS SELL_DIRECTION_SALE_AMT,  -- 卖出方向卖出金额
        SUM(CASE WHEN TRADE_DIRECTION = 2 THEN BUY_AMOUNT ELSE 0 END) AS SELL_DIRECTION_BUY_AMT,    -- 卖出方向买入金额
        
        -- 损益信息
        MAX(COALESCE(PROFIT_CCY, '')) AS PROFIT_CCY,                                         -- 损益币种
        
        -- 轧差计算
        SUM(CASE WHEN TRADE_DIRECTION = 1 THEN BUY_AMOUNT ELSE -SALE_AMOUNT END) AS NETTING_AMOUNT,  -- 轧差金额
        
        -- 损益统计
        SUM(COALESCE(PROFIT_AMT, 0)) AS TOTAL_PROFIT_AMT,                                      -- 总损益
        SUM(COALESCE(SALES_PROFIT_AMT, 0)) AS TOTAL_SALES_PROFIT_AMT,                          -- 销售员损益
        SUM(COALESCE(TRADES_PROFIT_AMT, 0)) AS TOTAL_TRADES_PROFIT_AMT,                        -- 交易员损益
        
        -- 统计信息
        COUNT(*) AS TRADE_COUNT                                                                -- 交易总笔数
    FROM BAOFU_TRADE.T_TRADE_RECEIPT
    WHERE {where_clause}
    """
    
    if group_clause:
        sql += f" GROUP BY {group_clause}"
        sql += f" ORDER BY {group_clause}"
    
    result = execute_db(env, sql, params=params)
    return result


def print_netting_result(result: List[Dict[str, Any]], title: str = "轧差统计结果"):
    """
    格式化打印轧差统计结果
    """
    print(f"\n{'='*70}")
    print(f" {title}")
    print(f"{'='*70}")
    
    if not result:
        print("无数据")
        return
    
    if isinstance(result, dict):
        result = [result]
    
    for row in result:
        print("-" * 70)
        
        # 获取货币对信息
        currency_pair = row.get('CURRENCY_PAIR', '')
        user_no = row.get('USER_NO', '')
        profit_ccy = row.get('PROFIT_CCY', '')
        
        if user_no:
            print(f" 用户号: {user_no}")
        if currency_pair:
            print(f" 货币对: {currency_pair}")
        
        # 买入方向统计
        buy_count = row.get('BUY_DIRECTION_COUNT', 0)
        buy_sale_amt = row.get('BUY_DIRECTION_SALE_AMT', 0)
        buy_buy_amt = row.get('BUY_DIRECTION_BUY_AMT', 0)
        
        # 卖出方向统计
        sell_count = row.get('SELL_DIRECTION_COUNT', 0)
        sell_sale_amt = row.get('SELL_DIRECTION_SALE_AMT', 0)
        sell_buy_amt = row.get('SELL_DIRECTION_BUY_AMT', 0)
        
        # 解析货币对获取币种
        src_ccy = ''
        tgt_ccy = ''
        if currency_pair:
            parts = currency_pair.split('/')
            if len(parts) == 2:
                src_ccy, tgt_ccy = parts
        
        # 打印买入方向
        print(f" 买入方向（TRADE_DIRECTION=1）: {buy_count}条")
        if src_ccy and tgt_ccy:
            print(f"    买入{src_ccy}: {buy_buy_amt:.2f}, 卖出{tgt_ccy}: {buy_sale_amt:.2f}")
        
        # 打印卖出方向
        print(f" 卖出方向（TRADE_DIRECTION=2）: {sell_count}条")
        if src_ccy and tgt_ccy:
            print(f"    卖出{src_ccy}: {sell_sale_amt:.2f}, 买入{tgt_ccy}: {sell_buy_amt:.2f}")
        
        # 计算详细轧差
        netting_amt = row.get('NETTING_AMOUNT', 0)
        print(f" 轧差结果: {netting_amt:.2f}")
        
        # 详细轧差分析
        if src_ccy and tgt_ccy:
            # 同币种轧差
            src_netting = buy_buy_amt - sell_sale_amt  # 买入方向买入 - 卖出方向卖出
            tgt_netting = sell_buy_amt - buy_sale_amt  # 卖出方向买入 - 买入方向卖出
            
            print(f" 详细轧差:")
            details = []
            
            # 源币种（货币对第一个币种）的轧差
            if abs(src_netting) > 0:
                if src_netting > 0:
                    details.append(f"买入{src_ccy}: {src_netting:.2f}")
                else:
                    details.append(f"卖出{src_ccy}: {abs(src_netting):.2f}")
            
            # 目标币种的轧差
            if abs(tgt_netting) > 0:
                if tgt_netting > 0:
                    details.append(f"买入{tgt_ccy}: {tgt_netting:.2f}")
                else:
                    details.append(f"卖出{tgt_ccy}: {abs(tgt_netting):.2f}")
            
            if details:
                # 确定最终方向（以源币种的方向为准）
                if src_netting > 0:
                    final_direction = "买入"
                elif src_netting < 0:
                    final_direction = "卖出"
                else:
                    # 源币种无轧差时，以目标币种方向为准
                    if tgt_netting > 0:
                        final_direction = "买入"
                    elif tgt_netting < 0:
                        final_direction = "卖出"
                    else:
                        final_direction = "无"
                
                print(f"    {final_direction}方向：{', '.join(details)}")
        
        # 打印损益信息
        print(f" 总损益: {row.get('TOTAL_PROFIT_AMT', 0):.2f} {profit_ccy}")
        print(f" 销售员损益: {row.get('TOTAL_SALES_PROFIT_AMT', 0):.2f} {profit_ccy}")
        print(f" 交易员损益: {row.get('TOTAL_TRADES_PROFIT_AMT', 0):.2f} {profit_ccy}")
        print(f" 交易总笔数: {row.get('TRADE_COUNT', 0)}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    # ==================== 参数配置区 ====================
    env = 'FAT'                          # 环境: FAT / UAT
    user_no = None                       # 用户号，如 '123456'，None表示不筛选
    currency_pair = 'USD/CNH'            # 货币对，如 'USD/CNH' 或 'USDCNH'，None表示不筛选
    source_currency = "USD"               # 源币种，如 'USD'，None表示不筛选
    target_currency = "CNH"               # 目标币种，如 'CNH'，None表示不筛选
    update_time_start = "2026-03-01 00:00:00"             # 更新时间开始，如 '2025-01-01 00:00:00'
    update_time_end = "2026-03-06 00:00:00"               # 更新时间结束，如 '2025-01-31 23:59:59'
    group_by_user = False                # 是否按用户分组
    group_by_currency = True             # 是否按货币对分组
    # ===================================================
    
    print("=" * 80)
    print(" 凭证轧差统计工具")
    print("=" * 80)
    print(f" 环境参数: env={env}")
    print(f" 筛选参数: user_no={user_no}, currency_pair={currency_pair}")
    print(f" 时间参数: update_time_start={update_time_start}, update_time_end={update_time_end}")
    print(f" 分组参数: group_by_user={group_by_user}, group_by_currency={group_by_currency}")
    print("=" * 80)
    
    result = get_receipt_netting(
        env=env,
        user_no=user_no,
        source_currency=source_currency,
        target_currency=target_currency,
        currency_pair=currency_pair,
        update_time_start=update_time_start,
        update_time_end=update_time_end,
        group_by_user=group_by_user,
        group_by_currency=group_by_currency
    )
    print_netting_result(result, "轧差统计结果")
