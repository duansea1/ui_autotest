"""
@Author    : duersea
@Date      : 2026/3/9
@Description: [统计客单批次已完成订单，轧差后金额]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Kuajing.Common.kjMysql import execute_db
from typing import Optional, List, Dict, Any
import time

exce_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

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


def get_batch_order_netting(
    env: str,
    currency_pair: Optional[str] = None,
    complete_date_start: Optional[str] = None,
    complete_date_end: Optional[str] = None,
    trade_direction: Optional[int] = None,
    user_no: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    统计客单批次已完成订单，轧差后金额
    
    Args:
        env: 环境名称(FAT/UAT/FAT_DATA)
        currency_pair: 货币对，如'USD/CNH'(可选)
        complete_date_start: 完成时间开始，如'2026-03-01 00:00:00'
        complete_date_end: 完成时间结束，如'2026-03-29 23:59:59'
        trade_direction: 交易方向(可选，1-买入，2-卖出)
        user_no: 用户号(可选)
    
    Returns:
        用户+货币对+方向维度的轧差统计结果
    """
    # 解析货币对（支持 EUR/USD 或 EURUSD 格式）
    ccy_pair = None
    if currency_pair:
        # 移除空格，转为大写，保留斜杠格式
        ccy_pair = currency_pair.replace(' ', '').strip().upper()
    
    # 构建T_EXCHANGE_BATCH_ORDER查询条件
    batch_conditions = []
    batch_params = []
    
    if ccy_pair:
        batch_conditions.append("CCY_PAIR = %s")
        batch_params.append(ccy_pair)
    
    if complete_date_start:
        batch_conditions.append("COMPLETE_DATE >= %s")
        batch_params.append(complete_date_start)
    
    if complete_date_end:
        batch_conditions.append("COMPLETE_DATE <= %s")
        batch_params.append(complete_date_end)
    
    # 状态: COMPLETED 或 NOT_PROCESS
    batch_conditions.append("STATUS IN ('COMPLETED', 'NOT_PROCESS')")
    
    batch_where = " AND ".join(batch_conditions) if batch_conditions else "1=1"
    
    # 查询批次号
    batch_sql = f"""
    SELECT BATCH_NO
    FROM BAOFU_TRADE.T_EXCHANGE_BATCH_ORDER
    WHERE {batch_where}
    """
    
    batch_result = execute_db(env, batch_sql, params=batch_params)
    
    if not batch_result:
        return []
    
    # 获取批次号列表
    batch_nos = [row['BATCH_NO'] for row in batch_result]
    
    if not batch_nos:
        return []
    
    # 构建T_TRADE_RECEIPT查询条件
    receipt_conditions = []
    receipt_params = []
    
    receipt_conditions.append(f"CHANNEL_ORDER_NO IN ({','.join(['%s'] * len(batch_nos))})")
    receipt_params.extend(batch_nos)
    
    if user_no:
        receipt_conditions.append("USER_NO = %s")
        receipt_params.append(user_no)
    
    if trade_direction:
        receipt_conditions.append("TRADE_DIRECTION = %s")
        receipt_params.append(trade_direction)
    
    # TODO默认查询已完成状态  无需兑换批次单，凭证状态是处理中，这个需要注释
    # receipt_conditions.append("TRADE_STATUS = 3")  
    
    receipt_where = " AND ".join(receipt_conditions)
    
    # 生成筛选条件描述
    ccy_desc = ccy_pair or "全部"
    direction_desc = "全部" if not trade_direction else ("买入" if trade_direction == 1 else "卖出")
    user_desc = user_no or "全部"
    date_desc = f"{complete_date_start or '开始'} 至 {complete_date_end or '结束'}"
    
    # 主查询SQL（用于执行）
    sql = f"""
    SELECT 
        USER_NO AS USER_NO,                                              
        SOURCE_CURRENCY AS SOURCE_CURRENCY,                              
        TARGET_CURRENCY AS TARGET_CURRENCY,                              
        CONCAT(SOURCE_CURRENCY, '/', TARGET_CURRENCY) AS CURRENCY_PAIR, 
        TRADE_DIRECTION AS TRADE_DIRECTION,                              
                                    
        
        SUM(BUY_AMOUNT) AS TOTAL_BUY_AMOUNT,                             
        SUM(SALE_AMOUNT) AS TOTAL_SALE_AMOUNT,                           
        
        SUM(COALESCE(PROFIT_AMT, 0)) AS TOTAL_PROFIT_AMT,               
        MAX(COALESCE(PROFIT_CCY, '')) AS PROFIT_CCY,                    
        SUM(COALESCE(SALES_PROFIT_AMT, 0)) AS TOTAL_SALES_PROFIT_AMT,   
        SUM(COALESCE(TRADES_PROFIT_AMT, 0)) AS TOTAL_TRADES_PROFIT_AMT, 

        COUNT(*) AS TRADE_COUNT                                          
    FROM BAOFU_TRADE.T_TRADE_RECEIPT
    WHERE {receipt_where}
    GROUP BY USER_NO, SOURCE_CURRENCY, TARGET_CURRENCY, TRADE_DIRECTION
    ORDER BY USER_NO, SOURCE_CURRENCY, TARGET_CURRENCY, TRADE_DIRECTION
    """
    
    # 打印SQL语句（带注释，用于显示）
    sql_display = f"""
    -- 统计客单批次已完成订单，轧差后金额
    -- 货币对: {ccy_desc}
    -- 完成时间: {date_desc}
    -- 交易方向: {direction_desc}
    -- 用户号: {user_desc}
    -- 批次数量: {len(batch_nos)}
    
    SELECT 
        USER_NO AS USER_NO,                                              -- 用户号
        SOURCE_CURRENCY AS SOURCE_CURRENCY,                              -- 源币种
        TARGET_CURRENCY AS TARGET_CURRENCY,                              -- 目标币种
        CONCAT(SOURCE_CURRENCY, '/', TARGET_CURRENCY) AS CURRENCY_PAIR, -- 货币对
        TRADE_DIRECTION AS TRADE_DIRECTION,                              -- 交易方向
        
        -- 按方向汇总金额
        SUM(BUY_AMOUNT) AS TOTAL_BUY_AMOUNT,                             -- 买入金额(目标币种)
        SUM(SALE_AMOUNT) AS TOTAL_SALE_AMOUNT,                           -- 卖出金额(源币种)
        
        -- 损益信息
        SUM(COALESCE(PROFIT_AMT, 0)) AS TOTAL_PROFIT_AMT,               -- 总损益
        MAX(COALESCE(PROFIT_CCY, '')) AS PROFIT_CCY,                    -- 损益币种
        SUM(COALESCE(SALES_PROFIT_AMT, 0)) AS TOTAL_SALES_PROFIT_AMT,  -- 销售员损益
        SUM(COALESCE(TRADES_PROFIT_AMT, 0)) AS TOTAL_TRADES_PROFIT_AMT, -- 交易员损益

        -- 统计信息
        COUNT(*) AS TRADE_COUNT                                          -- 交易数量
    FROM BAOFU_TRADE.T_TRADE_RECEIPT
    WHERE {receipt_where}
    GROUP BY USER_NO, SOURCE_CURRENCY, TARGET_CURRENCY, TRADE_DIRECTION
    ORDER BY USER_NO, SOURCE_CURRENCY, TARGET_CURRENCY, TRADE_DIRECTION
    """
    
    # 打印SQL语句
    print("\n" + "="*80)
    print(f" 生成的SQL查询 {exce_time}")
    print("="*80)
    print("\n【第一步：查询批次号】")
    
    # 生成可执行的SQL（替换参数）
    executable_batch_sql = batch_sql
    for param in batch_params:
        if isinstance(param, str):
            executable_batch_sql = executable_batch_sql.replace('%s', f"'{param}'", 1)
        else:
            executable_batch_sql = executable_batch_sql.replace('%s', str(param), 1)
    print(executable_batch_sql)
    
    print(f"\n查询到 {len(batch_nos)} 个批次号")
    
    if batch_nos:
        print("\n【第二步：查询凭证明细】")
        # 生成可执行的SQL（替换参数）
        executable_sql = sql
        for param in receipt_params:
            if isinstance(param, str):
                executable_sql = executable_sql.replace('%s', f"'{param}'", 1)
            else:
                executable_sql = executable_sql.replace('%s', str(param), 1)
        print(executable_sql)
    
    print("="*80 + "\n")
    
    result = execute_db(env, sql, params=receipt_params)
    return result


def print_netting_result(result: List[Dict[str, Any]], title: str = "客单批次轧差统计结果"):
    """
    格式化打印轧差统计结果
    """
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}")
    
    if not result:
        print("无数据")
        return
    
    # 检查PROFIT_CCY一致性
    print("\n" + "="*80)
    print(f" 检查PROFIT_CCY一致性  {exce_time}")
    print("="*80)
    
    # 按货币对分组，检查PROFIT_CCY
    currency_profit_ccy_map = {}
    inconsistent_data = []
    
    for row in result:
        currency_pair = row.get('CURRENCY_PAIR', '')
        profit_ccy = row.get('PROFIT_CCY', '')
        
        if currency_pair:
            if currency_pair not in currency_profit_ccy_map:
                currency_profit_ccy_map[currency_pair] = profit_ccy
            else:
                existing_ccy = currency_profit_ccy_map[currency_pair]
                if existing_ccy != profit_ccy:
                    inconsistent_data.append({
                        'user_no': row.get('USER_NO', ''),
                        'currency_pair': currency_pair,
                        'trade_direction': row.get('TRADE_DIRECTION', 0),
                        'expected_profit_ccy': existing_ccy,
                        'actual_profit_ccy': profit_ccy,

                    })
    
    if inconsistent_data:
        print("❌发现不一致的PROFIT_CCY❌:")
        for data in inconsistent_data:
            print(f"- 用户号: {data['user_no']}, 货币对: {data['currency_pair']}, 方向: {data['trade_direction']}")

            print(f"  期望币种: {data['expected_profit_ccy']}, 实际币种: {data['actual_profit_ccy']}")
    else:
        print("✅所有货币对的PROFIT_CCY一致，检查通过！")
    
    # 按货币对+交易方向全局汇总
    global_summary = {}
    
    for row in result:
        print("-" * 80)
        
        user_no = row.get('USER_NO', '')
        currency_pair = row.get('CURRENCY_PAIR', '')
        trade_direction = row.get('TRADE_DIRECTION', 0)
        direction_name = "买入" if trade_direction == 1 else "卖出"
        
        # 解析货币对
        src_ccy = row.get('SOURCE_CURRENCY', '')
        tgt_ccy = row.get('TARGET_CURRENCY', '')
        
        print(f" 用户号: {user_no}")
        print(f" 货币对: {currency_pair}")
        print(f" 交易方向: {trade_direction}({direction_name})")
        
        if trade_direction == 1:
            # 买入方向：卖出目标币种，买入源币种
            print(f" 卖出{tgt_ccy}: {row.get('TOTAL_SALE_AMOUNT', 0):.2f}")
            print(f" 买入{src_ccy}: {row.get('TOTAL_BUY_AMOUNT', 0):.2f}")
        else:
            # 卖出方向：卖出源币种，买入目标币种
            print(f" 卖出{src_ccy}: {row.get('TOTAL_SALE_AMOUNT', 0):.2f}")
            print(f" 买入{tgt_ccy}: {row.get('TOTAL_BUY_AMOUNT', 0):.2f}")
        
        # 损益信息
        profit_ccy = row.get('PROFIT_CCY', '')
        print(f" 总损益: {row.get('TOTAL_PROFIT_AMT', 0):.2f} {profit_ccy}")
        print(f" 销售员损益: {row.get('TOTAL_SALES_PROFIT_AMT', 0):.2f} {profit_ccy}")
        print(f" 交易员损益: {row.get('TOTAL_TRADES_PROFIT_AMT', 0):.2f} {profit_ccy}")
        print(f" 交易笔数: {row.get('TRADE_COUNT', 0)}")
        
        # 累计全局汇总
        key = (currency_pair, trade_direction)
        if key not in global_summary:
            global_summary[key] = {
                'TOTAL_SALE_AMOUNT': 0,
                'TOTAL_BUY_AMOUNT': 0,
                'TOTAL_PROFIT_AMT': 0,
                'TOTAL_SALES_PROFIT_AMT': 0,
                'TOTAL_TRADES_PROFIT_AMT': 0,
                'PROFIT_CCY': row.get('PROFIT_CCY', ''),
                'TRADE_COUNT': 0
            }
        
        global_summary[key]['TOTAL_SALE_AMOUNT'] += row.get('TOTAL_SALE_AMOUNT', 0)
        global_summary[key]['TOTAL_BUY_AMOUNT'] += row.get('TOTAL_BUY_AMOUNT', 0)
        global_summary[key]['TOTAL_PROFIT_AMT'] += row.get('TOTAL_PROFIT_AMT', 0)
        global_summary[key]['TOTAL_SALES_PROFIT_AMT'] += row.get('TOTAL_SALES_PROFIT_AMT', 0)
        global_summary[key]['TOTAL_TRADES_PROFIT_AMT'] += row.get('TOTAL_TRADES_PROFIT_AMT', 0)
        global_summary[key]['TRADE_COUNT'] += row.get('TRADE_COUNT', 0)
    
    # 打印全局汇总
    print("\n" + "="*80)
    print(f" 🚀🚀🚀🚀全局汇总（货币对+交易方向维度🚀🚀🚀🚀+{exce_time}）")
    print("="*80)
    
    for (currency_pair, trade_direction), summary in global_summary.items():
        print("-" * 80)
        direction_name = "买入" if trade_direction == 1 else "卖出"
        print(f" 货币对: {currency_pair}")
        print(f" 交易方向: {trade_direction}({direction_name})")
        
        # 解析货币对获取币种
        src_ccy = ''
        tgt_ccy = ''
        if currency_pair:
            parts = currency_pair.split('/')
            if len(parts) == 2:
                src_ccy, tgt_ccy = parts
        
        if trade_direction == 1:
            # 买入方向：卖出目标币种，买入源币种
            print(f" 卖出金额: {summary['TOTAL_SALE_AMOUNT']:.2f} {tgt_ccy}")
            print(f" 买入金额: {summary['TOTAL_BUY_AMOUNT']:.2f} {src_ccy}")
        else:
            # 卖出方向：卖出源币种，买入目标币种
            print(f" 卖出金额: {summary['TOTAL_SALE_AMOUNT']:.2f} {src_ccy}")
            print(f" 买入金额: {summary['TOTAL_BUY_AMOUNT']:.2f} {tgt_ccy}")
        
        print(f" 总损益: {summary['TOTAL_PROFIT_AMT']:.2f} {summary['PROFIT_CCY']}")
        print(f" 销售员损益: {summary['TOTAL_SALES_PROFIT_AMT']:.2f} {summary['PROFIT_CCY']}")
        print(f" 交易员损益: {summary['TOTAL_TRADES_PROFIT_AMT']:.2f} {summary['PROFIT_CCY']}")
        print(f" 交易笔数: {summary['TRADE_COUNT']}")
    
    print(f"{'='*80}\n")


if __name__ == "__main__":
    # ==================== 参数配置区 ====================
    env = 'FAT'                                  # 环境: FAT / UAT / FAT_DATA
    currency_pair = 'EUR/CNH'    
    # currency_pair = 'EUR/USD'                  # 货币对，如'USD/CNH'或'USDCNH'，None表示不筛选
    complete_date_start = '2026-03-17 00:00:00'  # 完成时间开始
    complete_date_end = '2026-03-17 23:59:59'   # 完成时间结束
    trade_direction = None                       # 交易方向: 1-买入, 2-卖出, None-全部
    user_no = None
    # user_no = '5181240628000024148'                               # 用户号，None表示不筛选
    # ===================================================
    
    print("=" * 80)
    print(" 🚀🚀🚀客单批次已完成订单轧差统计")
    print("=" * 80)
    print(f" 环境参数: env={env}")
    print(f" 货币对: {currency_pair}")
    print(f" 完成时间: {complete_date_start} 至 {complete_date_end}")
    print(f" 交易方向: {trade_direction if trade_direction else '全部'}")
    print(f" 用户号: {user_no if user_no else '全部'}")
    print("=" * 80)
    
    result = get_batch_order_netting(
        env=env,
        currency_pair=currency_pair,
        complete_date_start=complete_date_start,
        complete_date_end=complete_date_end,
        trade_direction=trade_direction,
        user_no=user_no
    )
    print_netting_result(result, "客单批次轧差统计结果")
