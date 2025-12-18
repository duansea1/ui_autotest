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
        return Decimal('0.00')

    # ----------------------------
    # 动态计算 CREATE_AT 范围
    # ----------------------------
    try:
        start_dt = datetime.strptime(closing_date_start, '%Y-%m-%d')
        end_dt = datetime.strptime(closing_date_end, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError("closing_date_start/end must be in format 'YYYY-MM-DD'")

    # CREATE_AT >= closing_date_start - 60天
    create_at_start = (start_dt - timedelta(days=60)).strftime('%Y-%m-%d 00:00:00')
    # CREATE_AT <= closing_date_end 当天最后一秒
    create_at_end = (end_dt + timedelta(days=1) - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

    logger.info(f"CREATE_AT 范围: {create_at_start} ~ {create_at_end}")

    sql = """
    SELECT 
        RECEIPT_NO, TRADE_DIRECTION, SALE_AMOUNT, BUY_AMOUNT, 
        ORDER_GEP_RATE, PROFIT_AMT, ORIGINAL_CCY_PAIR, TRADE_TYPE,ORIGINAL_SALE_CURRENCY , SOURCE_CURRENCY, TARGET_CURRENCY  
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

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 传入所有参数
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
            return Decimal('0.00')

        logger.info(f"开始计算 {currency_pair} 销售损益 | 模式={mode}, incomeCcy={incomeCcy} | 共 {len(results)} 条")

        # 后续处理逻辑保持不变...
        # （此处省略，使用之前修复后的正确计算逻辑）
        for row in results:
            receipt_no = row['RECEIPT_NO']
            profit_amt = row['PROFIT_AMT'] or Decimal('0.00')
            trade_direction = row['TRADE_DIRECTION']
            order_gep_rate = row['ORDER_GEP_RATE']

            original_ccy_pair = row['ORIGINAL_CCY_PAIR']
            trade_type = row['TRADE_TYPE']
            # buy_amount_all = row['buy_amount_all']
            # sale_amount_all = row['sale_amount_all']


            # ----------------------------
            # 特殊情况处理
            # 获取币种
            src_ccy = row['SOURCE_CURRENCY']
            tgt_ccy = row['TARGET_CURRENCY']
            sale_amt = row['SALE_AMOUNT'] or Decimal('0.00')
            buy_amt = row['BUY_AMOUNT'] or Decimal('0.00')

            # 确定 SALE_AMOUNT 的真实币种
            if row['ORIGINAL_SALE_CURRENCY']:
                sale_currency = row['ORIGINAL_SALE_CURRENCY']
            else:
                sale_currency = src_ccy

            # BUY_AMOUNT 是另一个币种
            buy_currency = tgt_ccy if sale_currency == src_ccy else src_ccy

            # 根据 TRADE_DIRECTION 确定方向描述
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
            # ----------------------------
            # 特殊情况处理 + 动态汇率选择（allNew 核心逻辑）
            # ----------------------------

            # 1. 拆分交易 → 销售损益 = 0
            if original_ccy_pair and original_ccy_pair != currency_pair:
                logger.debug(f"{base_log} 拆分交易 | 销售=0")
                continue

            # 2. 取消交易 / GEP 分发 → 销售 = PROFIT_AMT
            if trade_type in exclude_types:
                total_sales_profit += profit_amt
                logger.info(f"{base_log} 取消/GEP交易 | 销售={profit_amt:.6f}")
                continue

            # 3. USD/CNH 汇率异常检查（仅限 all / noTall 模式）
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

            # ----------------------------
            # 【核心】确定 use_rate：allNew 模式优先用 ORDER_GEP_RATE，空则用 now_rate
            # ----------------------------
            use_rate = None

            if mode == 'allNew':
                # allNew 模式：优先使用 ORDER_GEP_RATE（若有效），否则 fallback 到 now_rate
                if order_gep_rate is not None and order_gep_rate != 0:
                    use_rate = order_gep_rate
                    logger.debug(f"{base_log} allNew 模式 | 使用 ORDER_GEP_RATE={use_rate}/100")
                else:
                    if now_rate is None:
                        raise ValueError(f"mode='allNew' 且 ORDER_GEP_RATE 无效，但 now_rate 未提供 | receipt_no={receipt_no}")
                    use_rate = now_rate * Decimal('100')
                    logger.info(f"{base_log} allNew 模式 | ORDER_GEP_RATE 为空，使用 now_rate={now_rate} → use_rate={use_rate}/100")

            else:
                # all / noTall 模式：使用 ORDER_GEP_RATE
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




            # ----------------------------
            # 根据 incomeCcy 和 trade_direction 计算销售损益（原逻辑不变）
            # ----------------------------
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

                # ✅ 优化日志：包含金额币种、公式、汇率
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

    total_sales_profit = total_sales_profit.quantize(Decimal('0.00'))
    logger.info(f"✅ {currency_pair} 总销售损益: {total_sales_profit}")
    return total_sales_profit


# 预计总损益计算
def calculate_projected_profit_simple(
    sale_amount: Decimal,
    buy_amount: Decimal,
    now_rate: Decimal,
    income_ccy: str  # 'saleccy' 或 'buyccy'
) -> Decimal:
    """
    计算预计损益（简化版），包含日志输出

    :param sale_amount: 卖出金额
    :param buy_amount: 买入金额
    :param now_rate: 第三方汇率（1单位卖出币 = ? 单位买入币）
    :param income_ccy: 损益留存币种，'saleccy' 或 'buyccy'
    :return: 预计损益
    """
    logger.info(f"开始计算预计损益 | 卖出金额={sale_amount}, 买入金额={buy_amount}, "
                f"当前汇率={now_rate}, 留存币种={income_ccy}")

    if income_ccy == 'buyCcy':
        # 留存币种为买入币：卖出金额 * 汇率 - 买入金额
        result = sale_amount * now_rate - buy_amount
        logger.info(f"计算方式: 卖出金额 × 汇率 - 买入金额 = {sale_amount} × {now_rate} - {buy_amount} = {result}")
    elif income_ccy == 'saleCcy':
        # 留存币种为卖出币：卖出金额 - 买入金额 * 汇率
        division = buy_amount * now_rate
        division2 = buy_amount / now_rate
        result2 = sale_amount - division2
        result = sale_amount - division
        logger.info(f"计算方式: 卖出金额 - (买入金额 * 汇率) = {sale_amount} - ({buy_amount} * {now_rate}) = {sale_amount} - {division} = {result}")
        logger.info(
            f"卖出金额-买入金额/第三方汇率--计算方式: 卖出金额 - (买入金额 / 汇率) = {sale_amount} - ({buy_amount} / {now_rate}) = {sale_amount} - {division2} = {result2}")
    else:
        error_msg = "income_ccy 必须是 'saleCcy' 或 'buyCcy'"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"⏩预计总损益计算完成: {result}")
    return result






if __name__ == '__main__':
    now_rate = '7.1934'
    total = calculate_sales_profit(
        currency_pair='USD/CNH',
        closing_date_start='2025-07-30',
        closing_date_end='2025-08-13',
        mode='allNew',   # 使用新汇率计算
        now_rate=Decimal(now_rate),   # 第三方汇率
        incomeCcy='right',   # 收益币种在左边
        exclude_types=[]   # 排除 6--GEP 分发、拆分交易
    )

    # # # 预计总损益计算
    # now_rate = '0.6476'
    # result2 = calculate_projected_profit_simple(
    #     sale_amount=Decimal('20001'),
    #     buy_amount=Decimal('12978.19'),
    #     now_rate=Decimal(now_rate),
    #     income_ccy='saleCcy')
    
    # now_rate='0.6505'
    # result2 = calculate_projected_profit_simple(
    #     sale_amount=Decimal('2472.62'),
    #     buy_amount=Decimal('3741.7'),
    #     now_rate=Decimal(now_rate),
    #     income_ccy='buyCcy')

