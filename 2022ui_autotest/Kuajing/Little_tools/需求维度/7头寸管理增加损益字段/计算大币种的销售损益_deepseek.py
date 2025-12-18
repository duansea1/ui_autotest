from decimal import Decimal
import pymysql
from Kuajing.Common.kjMysql import get_db_config
from pymysql.cursors import DictCursor
import logging
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def calculate_sales_profit(
        currency_pair: str,
        closing_date_start: str,
        closing_date_end: str,
        env: str = 'FAT',
        mode: str = 'all',
        incomeCcy: str = 'right',
        exclude_types: list = None,
        now_rate: Decimal = None
):
    """
    计算销售损益，支持动态 CREATE_AT 范围（基于 closing_date_start - 60天）
    """
    # 参数校验
    if mode not in ['all', 'noTall', 'allNew']:
        raise ValueError("mode must be 'all', 'noTall', or 'allNew'")
    if incomeCcy not in ['left', 'right']:
        raise ValueError("incomeCcy must be 'left' or 'right'")
    if mode == 'allNew' and now_rate is None:
        raise ValueError("mode='allNew' requires now_rate to be provided")

    if exclude_types is None:
        exclude_types = [5]  # 默认排除：取消交易

    valid_pairs = [
        'USD/CNH', 'EUR/CNH', 'GBP/CNH', 'CAD/CNH', 'HKD/CNH', 'SGD/CNH',
        'AUD/CNH', 'NZD/CNH', 'CNH/JPY', 'USD/JPY', 'USD/HKD', 'EUR/USD',
        'AUD/USD', 'GBP/USD', 'USD/CAD', 'USD/CHF', 'GBP/HKD', 'EUR/HKD',
        'EUR/JPY', 'HKD/JPY'
    ]

    try:
        src_ccy, tgt_ccy = currency_pair.split('/')
    except ValueError:
        raise ValueError("currency_pair must be in format 'AAA/BBB'")

    if currency_pair not in valid_pairs:
        logger.warning(f"货币对 {currency_pair} 不在有效列表中，跳过。")
        return {
            'total_sales_profit': Decimal('0.00'),
            'net_sale_amount': Decimal('0.00'),
            'net_buy_amount': Decimal('0.00'),
            'final_direction': None,
            'currency_pair': currency_pair,
            'source_currency': src_ccy,
            'target_currency': tgt_ccy
        }

    # 动态计算 CREATE_AT 范围
    try:
        start_dt = datetime.strptime(closing_date_start, '%Y-%m-%d')
        end_dt = datetime.strptime(closing_date_end, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError("closing_date_start/end must be in format 'YYYY-MM-DD'")

    create_at_start = (start_dt - timedelta(days=60)).strftime('%Y-%m-%d 00:00:00')
    create_at_end = (end_dt + timedelta(days=1) - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

    logger.info(f"CREATE_AT 范围: {create_at_start} ~ {create_at_end}")

    sql = """
    SELECT 
        RECEIPT_NO, TRADE_DIRECTION, SALE_AMOUNT, BUY_AMOUNT, 
        ORDER_GEP_RATE, PROFIT_AMT, ORIGINAL_CCY_PAIR, TRADE_TYPE, ORIGINAL_SALE_CURRENCY, 
        SOURCE_CURRENCY, TARGET_CURRENCY  
    FROM BAOFU_TRADE.T_TRADE_RECEIPT
    WHERE 
        TRADE_STATUS = '1'
        AND SOURCE_CURRENCY = %s
        AND TARGET_CURRENCY = %s
        AND TRADE_TYPE IN (1,2,3,4,5)
        AND CLOSING_DATE >= %s
        AND CLOSING_DATE <= %s
        AND CREATE_AT >= %s
        AND CREATE_AT <= %s;
    """

    db_config = get_db_config(env)
    db_config['database'] = 'BAOFU_TRADE'
    db_config['cursorclass'] = DictCursor

    total_sales_profit = Decimal('0.00')
    connection = None

    # 初始化累计变量（使用通用变量名）
    total_sell_src = Decimal('0.00')  # 卖出源币种总额
    total_buy_tgt = Decimal('0.00')  # 买入目标币种总额
    total_buy_src = Decimal('0.00')  # 买入源币种总额
    total_sell_tgt = Decimal('0.00')  # 卖出目标币种总额

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(sql, (
                src_ccy,
                tgt_ccy,
                closing_date_start,
                closing_date_end,
                create_at_start,
                create_at_end
            ))
            results = cursor.fetchall()

        if not results:
            logger.info(f"无数据：{currency_pair} 在 {closing_date_start} ~ {closing_date_end}")
            return {
                'total_sales_profit': Decimal('0.00'),
                'net_sale_amount': Decimal('0.00'),
                'net_buy_amount': Decimal('0.00'),
                'final_direction': None,
                'currency_pair': currency_pair,
                'source_currency': src_ccy,
                'target_currency': tgt_ccy
            }

        logger.info(f"开始计算 {currency_pair} 销售损益 | 模式={mode}, incomeCcy={incomeCcy} | 共 {len(results)} 条")

        for row in results:
            receipt_no = row['RECEIPT_NO']
            profit_amt = row['PROFIT_AMT'] or Decimal('0.00')
            trade_direction = row['TRADE_DIRECTION']
            order_gep_rate = row['ORDER_GEP_RATE']
            original_ccy_pair = row['ORIGINAL_CCY_PAIR']
            trade_type = row['TRADE_TYPE']
            sale_amt = row['SALE_AMOUNT'] or Decimal('0.00')
            buy_amt = row['BUY_AMOUNT'] or Decimal('0.00')

            if trade_direction == 2:  # 买入：买入目标币种，卖出源币种
                total_buy_tgt += buy_amt
                total_sell_src += sale_amt
            elif trade_direction == 1:  # 卖出：卖出目标币种，买入源币种
                total_sell_tgt += sale_amt
                total_buy_src += buy_amt

            # 确定 SALE_AMOUNT 的真实币种
            if row['ORIGINAL_SALE_CURRENCY']:
                sale_currency = row['ORIGINAL_SALE_CURRENCY']
            else:
                sale_currency = src_ccy

            buy_currency = tgt_ccy if sale_currency == src_ccy else src_ccy

            # 方向描述
            if trade_direction == 1:
                direction_str = f"买入 {src_ccy}/{tgt_ccy}"
                action_desc = f"买入 {buy_amt} {buy_currency}，卖出 {sale_amt} {sale_currency}"
            elif trade_direction == 2:
                direction_str = f"卖出 {src_ccy}/{tgt_ccy}"
                action_desc = f"卖出 {sale_amt} {sale_currency}，买入 {buy_amt} {buy_currency}"
            else:
                direction_str = "未知方向"
                action_desc = f"交易 {sale_amt} {sale_currency} ↔ {buy_amt} {buy_currency}"

            base_log = f"[{receipt_no}] {direction_str} | {action_desc} | "

            # 1. 拆分交易 → 销售损益 = 0
            if original_ccy_pair and original_ccy_pair != currency_pair:
                logger.debug(f"{base_log} 拆分交易 | 销售=0")
                continue

            # 2. 取消交易 / GEP 分发 → 销售 = PROFIT_AMT
            if trade_type in exclude_types:
                total_sales_profit += profit_amt
                logger.info(f"{base_log} 取消/GEP交易 | 销售={profit_amt:.6f}")
                continue

            # 3. USD/CNH 汇率异常检查
            if currency_pair == 'USD/CNH' and mode != 'allNew':
                if order_gep_rate is None or order_gep_rate == 0:
                    if mode == 'noTall':
                        logger.info(f"{base_log} USD/CNH 汇率为空 + noTall 模式 | 跳过")
                        continue
                    elif mode == 'all':
                        total_sales_profit += profit_amt
                        logger.info(f"{base_log} USD/CNH 汇率为空 | 销售={profit_amt:.6f}")
                        continue
                else:
                    rate_val = order_gep_rate / Decimal('100')
                    if not (Decimal('6.50') <= rate_val <= Decimal('7.50')):
                        logger.info(f"{base_log} USD/CNH 汇率异常 {rate_val} | 销售=0")
                        continue

            # 确定 use_rate
            use_rate = None
            if mode == 'allNew':
                if order_gep_rate is not None and order_gep_rate != 0:
                    use_rate = order_gep_rate
                    logger.debug(f"{base_log} allNew 模式 | 使用 ORDER_GEP_RATE={use_rate}/100")
                else:
                    if now_rate is None:
                        raise ValueError(
                            f"mode='allNew' 且 ORDER_GEP_RATE 无效，但 now_rate 未提供 | receipt_no={receipt_no}")
                    use_rate = now_rate * Decimal('100')
                    logger.info(
                        f"{base_log} allNew 模式 | ORDER_GEP_RATE 为空，使用 now_rate={now_rate} → use_rate={use_rate}/100")
            else:
                if order_gep_rate is None or order_gep_rate == 0:
                    if mode == 'noTall':
                        logger.info(f"{base_log} 汇率为空 + noTall 模式 | 跳过")
                        continue
                    elif mode == 'all':
                        total_sales_profit += profit_amt
                        logger.info(f"{base_log} 汇率为空 | 销售={profit_amt:.6f}")
                        continue
                use_rate = order_gep_rate
                logger.debug(f"{base_log} 使用 ORDER_GEP_RATE={use_rate}/100")

            # 计算销售损益
            try:
                sales_profit = Decimal('0.00')
                formula = ""

                if trade_direction == 1:  # 买入
                    if incomeCcy == 'left':
                        sales_profit = (sale_amt * Decimal('100') / use_rate) - buy_amt
                        formula = f"卖出金额*100/汇率 - 买入金额 = {sale_amt}*100/{use_rate} - {buy_amt}"
                    elif incomeCcy == 'right':
                        sales_profit = sale_amt - (buy_amt * use_rate / Decimal('100'))
                        formula = f"卖出金额 - 买入金额*汇率/100 = {sale_amt} - {buy_amt}*{use_rate}/100"
                elif trade_direction == 2:  # 卖出
                    if incomeCcy == 'left':
                        sales_profit = sale_amt - (buy_amt * Decimal('100') / use_rate)
                        formula = f"卖出金额 - 买入金额*100/汇率 = {sale_amt} - {buy_amt}*100/{use_rate}"
                    elif incomeCcy == 'right':
                        sales_profit = (sale_amt * use_rate / Decimal('100')) - buy_amt
                        formula = f"卖出金额*汇率/100 - 买入金额 = {sale_amt}*{use_rate}/100 - {buy_amt}"

                total_sales_profit += sales_profit

                logger.info(
                    f"{base_log} "
                    f"销售损益={sales_profit:.6f} | "
                    f"使用汇率={use_rate}/100 | "
                    f"计算公式：{formula}"
                )

            except Exception as e:
                logger.error(f"{base_log} 计算失败: {e}")
                if mode == 'all':
                    total_sales_profit += profit_amt

    except Exception as e:
        logger.error(f"数据库错误: {e}")
        raise
    finally:
        if connection and connection.open:
            connection.close()

    # 计算净方向（使用通用变量名）
    net_sell_src = total_sell_src - total_buy_src
    net_buy_tgt = total_buy_tgt - total_sell_tgt

    if net_sell_src > 0:
        final_direction = 2  # 净卖出源币种
        final_sale_amount = net_sell_src
        final_buy_amount = net_buy_tgt
    else:
        final_direction = 1  # 净买入源币种
        final_sale_amount = abs(net_sell_src)
        final_buy_amount = abs(net_buy_tgt)

    # 只记录最终的净方向信息
    logger.info(f"🔍 净方向: {'卖出' if final_direction == 1 else '买入'} {final_sale_amount} {src_ccy}")

    total_sales_profit = total_sales_profit.quantize(Decimal('0.00'))
    logger.info(f"✅ {currency_pair} 总销售损益: {total_sales_profit}")

    return {
        'total_sales_profit': total_sales_profit,
        'net_sale_amount': final_sale_amount,
        'net_buy_amount': final_buy_amount,
        'final_direction': final_direction,
        'currency_pair': currency_pair,
        'source_currency': src_ccy,
        'target_currency': tgt_ccy
    }


def calculate_projected_profit_simple(
    db_result: dict,
    now_rate: Decimal,
    income_ccy: str  # 'saleCcy' 或 'buyCcy'
) -> Decimal:
    """
    计算预计损益（简化版），基于净买卖方向计算

    参数:
        db_result: calculate_sales_profit 方法的返回结果
        now_rate: 第三方汇率（1单位卖出币 = ? 单位买入币）
        income_ccy: 损益留存币种，'saleCcy' 或 'buyCcy'
    """
    net_sale = db_result['net_sale_amount']
    net_buy = db_result['net_buy_amount']
    direction = db_result['final_direction']
    src_ccy = db_result['source_currency']
    tgt_ccy = db_result['target_currency']

    if direction == 2:  # 卖出
        net_sale = db_result['net_sale_amount']
        net_buy = db_result['net_buy_amount']
    if direction == 1:   # 买入
        net_sale = db_result['net_buy_amount']
        net_buy = db_result['net_sale_amount']

    logger.info(f"开始计算预计损益 | 货币对: {src_ccy}/{tgt_ccy}")
    logger.info(f"---------------------净方向: {'卖出' if direction == 2 else '买入'} {net_sale} {src_ccy}")
    logger.info(f"净买入金额: {net_buy} {tgt_ccy}")
    logger.info(f"当前汇率: {now_rate} (1 {src_ccy} = {now_rate} {tgt_ccy})")
    logger.info(f"留存币种: {income_ccy}")

    if income_ccy not in ['saleCcy', 'buyCcy']:
        error_msg = "income_ccy 必须是 'saleCcy' 或 'buyCcy'"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # 情况1: 净卖出且留存币种为买入币种（目标币种）
    if income_ccy == 'buyCcy':
        result = net_sale * now_rate - net_buy
        logger.info(
            f"预计总损益计算：卖出金额×汇率-买入金额 = {net_sale} × {now_rate} - {net_buy} = {result}"
        )
        result2 = None

    # 情况2: 净卖出且留存币种为卖出币种（源币种）
    if income_ccy == 'saleCcy':
        # 卖出金额-买入金额/第三方汇率
        division = net_buy / now_rate
        result = net_sale - division
        logger.info(
            f"预计总损益计算：卖出金额-买入金额/汇率 = {net_sale} - ({net_buy} / {now_rate}) = {result}"
        )

        # 卖出金额-买入金额*第三方汇率
        division = net_buy * now_rate
        result2 = net_sale - division
        logger.info(
            f"预计总损益计算：卖出金额-买入金额*汇率 = {net_sale} - ({net_buy} * {now_rate}) = {result2}"
        )

    logger.info(f"⏩ 预计总损益计算完成: {result}")
    if result2 is not None:
        logger.info(f"⏩ 备用预计总损益计算: {result2}")
    return result


if __name__ == '__main__':
    # 计算销售损益
    rate = '7.1934'
    db_result = calculate_sales_profit(
        currency_pair='USD/CNH',
        closing_date_start='2025-07-30',
        closing_date_end='2025-08-13',
        mode='allNew',
        now_rate=Decimal(rate),
        incomeCcy='right',
        exclude_types=[]
    )

    # 计算预计总损益损益
    projected_profit = calculate_projected_profit_simple(
        db_result=db_result,
        now_rate=Decimal(rate),
        income_ccy='saleCcy'
    )