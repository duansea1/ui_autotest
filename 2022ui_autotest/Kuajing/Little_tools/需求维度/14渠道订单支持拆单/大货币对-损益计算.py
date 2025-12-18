import pymysql
import logging
import sys
import os


from Kuajing.Common.kjMysql import get_db_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_dynamic_params_from_db(exchange_no: str, env: str = 'FAT') -> dict:
    """
    根据exchange_no从数据库获取动态参数
    
    Args:
        exchange_no: 交易订单号(RECEIPT_NO)
        env: 环境，默认为'FAT'
    
    Returns:
        dict: 包含所需参数的字典
    """
    # 获取数据库配置并修改为BAOFU_TRADE数据库
    db_config = get_db_config(env).copy()
    db_config['database'] = 'BAOFU_TRADE'
    
    connection = None
    try:
        # 建立数据库连接
        connection = pymysql.connect(**db_config)
        logger.info(f"成功连接到数据库: {db_config['database']}")
        
        # SQL查询
        sql = """
        SELECT 
            SALE_AMOUNT as sell_amount,
            BUY_AMOUNT as buy_amount,
            RECEIPT_GEP_RATE as third_party_rate,
            ORIGINAL_CCY_PAIR as ccy_pair,
            PROFIT_CCY as profit_ccy,
            TRADE_DIRECTION as direction,
            EXCHANGE_RATE as customer_rate
        FROM 
            T_TRADE_RECEIPT 
        WHERE 
            RECEIPT_NO = %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(sql, (exchange_no,))
            result = cursor.fetchone()
            
            if result:
                # 转换交易方向代码为中文
                direction_map = {1: '买入', 2: '卖出'}
                result_dict = dict(result)
                
                # 将decimal.Decimal类型转换为float
                for key, value in result_dict.items():
                    if hasattr(value, '__module__') and value.__module__ == 'decimal':
                        result_dict[key] = float(value)
                
                result_dict['direction'] = direction_map.get(result_dict['direction'], result_dict['direction'])
                logger.info(f"成功获取交易订单{exchange_no}的参数: {result_dict}")
                return result_dict
            else:
                logger.warning(f"未找到交易订单: {exchange_no}")
                return None
                
    except Exception as e:
        logger.error(f"查询数据库时出错: {str(e)}")
        return None
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")

def calculate_forex_profits(
    buy_amount: float,
    sell_amount: float,
    customer_rate: float,
    channel_rate: float,
    third_party_rate: float,
    direction: str,  # '买入' 或 '卖出'
    ccy_pair: str,   # 如 "USD/CNH"
    profit_ccy: str, # 如 "CNH"
    fee: float = 0,
    is_internal_fee: bool = True,
    method: str = "default"  # 可选: "default", "cost_recovery", "weighted_avg"
) -> dict:
    """
    外汇交易损益计算（增强版）
    """
    # === 参数校验 ===
    direction = direction.strip()
    assert direction in ('买入', '卖出'), "方向参数必须为'买入'或'卖出'"
    assert '/' in ccy_pair, "货币对格式应为 'XXX/YYY'"
    left_ccy, right_ccy = ccy_pair.split('/')
    profit_ccy = profit_ccy.strip()
    assert profit_ccy in (left_ccy, right_ccy), f"收益币种 {profit_ccy} 不在货币对 {ccy_pair} 中"

    # 汇率单位转换：客户汇率通常为“每100单位源币兑换目标币”，故除以100
    effective_customer_rate = customer_rate / 100  # 目标币/源币
    effective_third_rate = third_party_rate / 100 if third_party_rate else None

    results = {}

    # === 特殊规则处理 ===
    is_usd_cnh = ccy_pair.replace('/', '').upper() == "USDCNH"
    third_party_invalid = (
        is_usd_cnh and third_party_rate is not None and not (650 <= third_party_rate <= 750)
    )

    # === 总损益：仅计算匹配当前方向+固定金额类型的场景 ===
    total_profit = 0.0
    scenario_desc = ""

    if direction == '买入':
        # 判断是“源币种固定”还是“目标币种固定”
        # 实际业务中需额外字段，此处假设：若 buy_amount 固定 → 源币种固定（如 USDCNH 中 CNH 固定？需澄清）
        # 但根据原始描述：
        #   - 源币种固定：如 USDCNH → 买入 CNH，固定 CNH（目标币）？矛盾。
        # 更合理理解（根据公式）：
        #   - “以源币种为固定金额” → 卖出金额固定（你付出的币固定）
        #   - “以目标币种为固定金额” → 买入金额固定（你收到的币固定）

        # 为简化，我们假设：
        #   - 若交易方向为“买入”，且 profit_ccy == right_ccy → 通常目标币是右边 → 固定目标币？
        # 但原始逻辑未明确如何判断“固定哪边”，故此处**保留两种可能，但由调用方决定场景**。
        # 为实用，我们按原始公式逻辑反推：
        #   - 场景1（源币种固定）：使用 buy_amount * (客户汇率/100 - 渠道汇率) → 目标币损益
        #   - 场景2（目标币种固定）：使用 sell_amount * (...) → 源币种损益

        # 由于缺乏“固定类型”字段，我们**默认按常见情况**：
        #   - 对于“买入”，若收益币种是目标币（右边），则视为“目标币固定”？不成立。
        # 实际上，原始文档中：
        #   - USDCNH（买入方向，源币种固定）→ 源币种是 USD？目标是 CNH？
        #   - 但 USDCNH 表示 1 USD = ? CNH，所以 USD 是 base（左边），CNH 是 quote（右边）
        #   - “买入方向”通常指买入 base（USD），但文档例子写 USDCNH 属于“源币种固定”，令人困惑。

        # 鉴于业务复杂性，此处**不自动判断固定类型**，而是要求调用方通过 method 或额外参数指定。
        # 但为兼容，我们按原始测试用例反推：
        #   - 测试用例：direction='卖出', buy_amount=706.78, sell_amount=100 → 卖出100单位（源币），买入706.78（目标币）
        #   - 货币对应为 USD/CNH，卖出 USD，买入 CNH
        #   - 所以：源币 = USD（左边），目标币 = CNH（右边）
        #   - 固定源币（卖出金额固定）→ 场景3

        # 因此，我们定义：
        #   - 源币种 = left_ccy（货币对左边）
        #   - 目标币种 = right_ccy（货币对右边）
        #   - 买入方向：买入 left_ccy（base），卖出 right_ccy？不，通常买入 base。
        # 但外汇惯例：USD/CNH 表示 1 USD = X CNH，买入 USD 需支付 CNH。
        # 所以：
        #   - 买入 USD → 卖出 CNH（源币是 CNH？）→ 混乱。

        # 为避免歧义，我们**放弃自动判断固定类型**，改为：
        #   - 总损益计算仅返回一种，由 direction 和 fee 决定，按原始公式中最常用场景：
        #       买入：使用场景1（源币种固定）→ 目标币损益
        #       卖出：使用场景3（源币种固定）→ 目标币损益
        #   - 因为测试用例是“卖出”，且使用了场景3公式。

        # 故统一按“源币种固定”处理（即卖出金额或买入金额对应源币固定）
        # 对于买入方向，源币种是付出的币（即 right_ccy），但公式中用 buy_amount（收到的币）？
        # 原始公式1：买入方向，源币种固定 → 汇兑损益 = 买入金额 * (客户汇率/100 - 渠道汇率)
        # 这里“买入金额”应为目标币金额。

        # 结论：我们按原始公式1和3实现，假设：
        #   - 买入方向 → 使用公式1（目标币损益）
        #   - 卖出方向 → 使用公式3（目标币损益）

        if is_internal_fee:
            total_profit = buy_amount * (effective_customer_rate - channel_rate)
        else:
            total_profit = buy_amount * (effective_customer_rate - channel_rate)
        scenario_desc = "买入方向，源币种固定（目标币损益）"
    else:  # 卖出
        if is_internal_fee:
            total_profit = (sell_amount - fee) * (channel_rate - effective_customer_rate)
        else:
            total_profit = sell_amount * (channel_rate - effective_customer_rate)
        scenario_desc = "卖出方向，源币种固定（目标币损益）"

    results['总损益'] = {
        'value': total_profit,
        'scenario': scenario_desc
    }

    # === 销售收益与交易员损益 ===
    sales_profit = 0.0
    trader_profit = 0.0
    total_gain = total_profit  # 总收益 = 总损益（简化）

    # 特殊情况：取消交易、GEP分发、第三方汇率为空
    if third_party_rate is None or third_party_invalid:
        sales_profit = total_gain
        trader_profit = 0.0
    elif is_usd_cnh and not (650 <= third_party_rate <= 750):
        sales_profit = 0.0
        trader_profit = total_gain
    else:
        # 判断收益币种位置
        is_profit_left = (profit_ccy == left_ccy)
        if direction == '买入':
            if is_profit_left:
                # 收益币种为左边（base）
                sales_profit = sell_amount / effective_third_rate - buy_amount
            else:
                # 收益币种为右边（quote）
                sales_profit = sell_amount - buy_amount * effective_third_rate
        else:  # 卖出
            if is_profit_left:
                sales_profit = sell_amount - buy_amount / effective_third_rate
            else:
                sales_profit = sell_amount * effective_third_rate - buy_amount
        trader_profit = total_gain - sales_profit

    results['销售收益'] = sales_profit
    results['交易员损益'] = trader_profit
    results['总收益'] = total_gain

    return results


def format_results(results: dict, direction: str, ccy_pair: str, profit_ccy: str) -> str:
    left, right = ccy_pair.split('/')
    pos = "左边" if profit_ccy == left else "右边"
    output = [
        f"\n===== {direction}方向计算结果 (货币对: {ccy_pair}, 收益币种: {profit_ccy} [{pos}]) =====",
        f"\n【总损益】{results['总损益']['scenario']}: {results['总收益']:.3f}",
        f"\n【销售收益】: {results['销售收益']:.3f}",
        f"【交易员损益】: {results['交易员损益']:.3f}"
    ]
    return '\n'.join(output)


# ===== 测试用例 =====
if __name__ == "__main__":
    # 方式1：使用数据库动态获取参数
    exchange_no = "2510212058000573965"
    
    # 获取动态参数
    dynamic_params = get_dynamic_params_from_db(exchange_no)
    
    if dynamic_params:
        # 补充必要的计算参数
        calc_params = dynamic_params.copy()
        # customer_rate已从数据库获取，不再需要硬编码
        # TODO: 查批次表动态获取渠道成交汇率
        calc_params['channel_rate'] = 7.13208955  # 渠道成交汇率-接收入参 
        calc_params['fee'] = 0
        calc_params['is_internal_fee'] = True
        
        # 计算损益
        results = calculate_forex_profits(**calc_params)
        print(format_results(results, calc_params['direction'], calc_params['ccy_pair'], calc_params['profit_ccy']))
    else:
        # 方式2：使用静态参数（备用方案）
        print("无法从数据库获取参数，使用默认参数进行计算...")
        params = {
            'sell_amount': 100.00,   # 卖出金额
            'buy_amount': 706.78,    # 买入金额
            'customer_rate': 706.7842,  # 用户汇率
            'third_party_rate': 711.160000,    # 第三方汇率
            'ccy_pair': 'USD/CNH',
            'profit_ccy': 'CNH',  # 右边
            'direction': '卖出',
            'channel_rate': 7.11109808,    # 渠道成交汇率
            'fee': 0,
            'is_internal_fee': True,
        }
        
        results = calculate_forex_profits(**params)
        print(format_results(results, params['direction'], params['ccy_pair'], params['profit_ccy']))