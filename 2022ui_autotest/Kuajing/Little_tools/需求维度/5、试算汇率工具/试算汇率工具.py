"""
@Author    : duansea
@Date      : 2025/7/29 17:05
@Description: 汇率试算工具 - 支持查询渠道汇率、计算浮动后新汇率、计算买入金额
"""

import logging
from decimal import Decimal
from Kuajing.Common.kjMysql import get_db_config
from pymysql import connect
from pymysql.cursors import DictCursor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def query_channel_rate(env: str, channel_id: str, closing_type: str, source_ccy: str, dest_ccy: str,
                       trade_direction: int = None, limit: int = 1000):
    """
    查询渠道汇率信息（仅生效状态）

    🔔 重要说明：
    - trade_direction 传入的是【客户角度】：
        - 1: 客户买入 SOURCE_CCY
        - 2: 客户卖出 SOURCE_CCY
    - 但数据库中 TRADE_DIRECTION 是【平台角度】，与客户相反：
        - 1: 平台买入（客户卖出）
        - 2: 平台卖出（客户买入）
    - 所以：
        - 客户买入 (1) → 查数据库 direction=2
        - 客户卖出 (2) → 查数据库 direction=1

    本函数自动完成视角转换，并按客户视角输出日志和结果。
    """
    print(f"🔍 正在查询环境[{env}]中渠道[{channel_id}]的汇率")
    print(f"📊 货币对：{source_ccy}/{dest_ccy}，交割类型：{closing_type}")

    if trade_direction is not None:
        direction_str = "买入" if trade_direction == 1 else "卖出"
        print(f"🎯 目标方向：客户{direction_str} {source_ccy}")
    else:
        print("🎯 目标方向：所有方向")

    config = get_db_config(env)
    config['database'] = 'BAOFU_CGW'

    connection = None
    try:
        connection = connect(**config)
        with connection.cursor(DictCursor) as cursor:
            # 查询所有方向（STATUS=1）
            sql = """
            SELECT * FROM `T_CHANNEL_RATE_REAL`
            WHERE `CHANNEL_ID` = %s
              AND `CLOSING_TYPE` = %s
              AND `SOURCE_CCY` = %s
              AND `DEST_CCY` = %s
              AND `STATUS` = 1
            ORDER BY `ID` DESC 
            LIMIT %s
            """
            params = [channel_id, closing_type, source_ccy, dest_ccy, limit]
            cursor.execute(sql, params)
            result = cursor.fetchall()

        if not result:
            logger.warning("⚠️ 未查询到符合条件的汇率数据")
            return []

        # 按【客户视角】分类（关键：方向反转）
        client_buy_rates = [r for r in result if r['TRADE_DIRECTION'] == 2]  # 客户买入 = 平台卖出
        client_sell_rates = [r for r in result if r['TRADE_DIRECTION'] == 1]  # 客户卖出 = 平台买入

        # 📊 日志输出：完整统计（客户视角）
        print(f"✅ 共查询到 {len(result)} 条有效汇率（客户买入 {len(client_buy_rates)} 条，客户卖出 {len(client_sell_rates)} 条）")

        # 🔽 客户买入 SOURCE_CCY（对应数据库 TRADE_DIRECTION = 2）
        if client_buy_rates:
            print("🔽 客户买入方向汇率（客户买入 SOURCE_CCY）：")
            for row in client_buy_rates:
                print(
                    f"   🟢 [买入方向（购汇/客买）] {source_ccy}/{dest_ccy} = {row['TRADE_RATE']:.6f} "
                    f"(ID: {row['ID']}, 批次号: {row['QUERY_BATCH_NO']})"
                )
        else:
            print("🔽 客户买入方向：无数据")

        # 🔼 客户卖出 SOURCE_CCY（对应数据库 TRADE_DIRECTION = 1）
        if client_sell_rates:
            print("🔼 客户卖出方向汇率（客户卖出 SOURCE_CCY）：")
            for row in client_sell_rates:
                print(
                    f"   🔴 [卖出方向（结汇/客卖）] {source_ccy}/{dest_ccy} = {row['TRADE_RATE']:.6f} "
                    f"(ID: {row['ID']}, 批次号: {row['QUERY_BATCH_NO']})"
                )
        else:
            print("🔼 客户卖出方向：无数据")

        # ✅ 根据 trade_direction 返回对应客户视角的数据
        if trade_direction == 1:
            filtered_result = client_buy_rates
            print(f"🎯 返回结果：客户买入 {source_ccy} 方向（共 {len(filtered_result)} 条）")
        elif trade_direction == 2:
            filtered_result = client_sell_rates
            print(f"🎯 返回结果：客户卖出 {source_ccy} 方向（共 {len(filtered_result)} 条）")
        else:
            # 若不指定方向，返回原始数据（或也可返回客户视角合并？这里保持原结构）
            filtered_result = result
            print(f"🎯 返回结果：所有方向（共 {len(filtered_result)} 条）")

        return filtered_result

    except Exception as e:
        logger.error(f"❌ 数据库查询出错: {e}")
        return []
    finally:
        if connection:
            connection.close()



def new_rate(trade_rate: Decimal, direction: str, fluctuation: float = 0.0):
    """
    根据原始汇率和浮动比例计算新的汇率
    direction: 'BUY' 表示客户买入 SOURCE_CCY (购汇), 'SELL' 表示客户卖出 SOURCE_CCY (结汇)
    """
    # 确保 trade_rate 是 Decimal
    if not isinstance(trade_rate, Decimal):
        trade_rate = Decimal(str(trade_rate))

    fluctuation_decimal = Decimal(str(fluctuation)) / Decimal('100')  # 转为小数，如 1% → 0.01
    direction_upper = direction.upper()

    print(f"📊 --------------------------------------------开始计算新汇率：原始汇率={trade_rate:.6f}, 方向={direction_upper}, 浮动比例={fluctuation}%")

    if direction_upper == 'BUY':
        # 客户买入 SOURCE_CCY（购汇）：价格应上浮 → 汇率变大
        new_exchange_rate = trade_rate * (Decimal(1) + fluctuation_decimal)
        print(f"📈 客户买入（购汇）：汇率上浮 {fluctuation}%，新汇率 = {new_exchange_rate:.6f}")

    elif direction_upper == 'SELL':
        # 客户卖出 SOURCE_CCY（结汇）：价格应下调 → 汇率变小
        if fluctuation_decimal >= 1:
            raise ValueError("卖出方向浮动比例不能 >= 100%")
        new_exchange_rate = trade_rate * (Decimal(1) - fluctuation_decimal)
        print(f"📉 客户卖出（结汇）：汇率下调 {fluctuation}%，新汇率 = {new_exchange_rate:.6f}")

    else:
        logger.error("❌ 方向参数错误，仅支持 'BUY' 或 'SELL'")
        raise ValueError("direction 必须是 'BUY' 或 'SELL'")

    return new_exchange_rate.quantize(Decimal('0.000000'))


def calculate_buy_amount(new_exchange_rate: Decimal, direction: str, sell_amount: float, sell_ccy: str, buy_ccy: str):
    """
    计算买入金额
    """
    sell_amount_decimal = Decimal(str(sell_amount))
    direction_upper = direction.upper()

    print(f"💰 计算交易金额：客户{direction_upper}，卖出 {sell_amount_decimal} {sell_ccy}")

    if direction_upper == 'BUY':
        # 客户买入 buy_ccy，意味着他卖出 sell_ccy
        # 汇率：750.5 PHP = 100 USD → rate = 750.5
        # 公式：buy_amount = sell_amount / (rate / 100)
        buy_amount = sell_amount_decimal / (new_exchange_rate / Decimal(100))
        print(f"🔁 购汇计算：{sell_amount_decimal} {sell_ccy} ÷ ({new_exchange_rate}/100) = {buy_amount:.4f} {buy_ccy}")

    elif direction_upper == 'SELL':
        # 客户卖出 sell_ccy，获得 buy_ccy
        buy_amount = sell_amount_decimal * (new_exchange_rate / Decimal(100))
        print(f"🔁 结汇计算：{sell_amount_decimal} {sell_ccy} × ({new_exchange_rate}/100) = {buy_amount:.4f} {buy_ccy}")

    else:
        logger.error("❌ 方向参数错误")
        raise ValueError("direction 必须是 'BUY' 或 'SELL'")

    buy_amount_rounded = buy_amount.quantize(Decimal('0.0000'))
    print(f"🎯 最终到账的金额和币种：{buy_amount_rounded} {buy_ccy}")

    return {
        'buy_amount': float(buy_amount_rounded),
        'buy_ccy': buy_ccy
    }



if __name__ == '__main__':
    # 参数设置
    env = 'FAT'
    channel_id = '1200923069'
    closing_type = 'TOD'
    source_ccy = 'EUR'   # 客户关注的币种
    dest_ccy = 'USD'
    trade_direction = 2  # 1: 客户买入 SOURCE_CCY；2: 客户卖出 SOURCE_CCY
    fluctuation = -10    # 浮动百分比
    sell_amount = 100000000  # 客户卖出的金额（单位：支付(卖出)币种）

    print("=" * 50)
    print("🔁 开始执行汇率试算流程")
    print("=" * 50)

    # 步骤1：查询汇率（注意：trade_direction=1 表示客户买入 SOURCE_CCY）
    rates = query_channel_rate(
        env=env,
        channel_id=channel_id,
        closing_type=closing_type,
        source_ccy=source_ccy,
        dest_ccy=dest_ccy,
        trade_direction=trade_direction,
        limit=10
    )

    if not rates:
        logger.error("❌ 汇率查询失败，终止流程")
    else:
        rate_info = rates[0]
        original_rate = rate_info['TRADE_RATE']  # Decimal 类型

        # 根据 trade_direction 推断客户行为
        if trade_direction == 1:
            # 客户买入 SOURCE_CCY（如 USD），所以：
            sell_ccy = dest_ccy    # 客户支付(卖出) dest_ccy（如 PHP）
            buy_ccy = source_ccy   # 客户买入 source_ccy（如 USD）
            direction_label = 'BUY'  # 客户买入动作
            print(f"🎯 客户行为：买入 {buy_ccy}，支付(卖出) {sell_amount} {sell_ccy}")

        elif trade_direction == 2:
            # 客户卖出 SOURCE_CCY（如 USD），所以：
            sell_ccy = source_ccy  # 客户支付(卖出) source_ccy
            buy_ccy = dest_ccy     # 客户获得 dest_ccy
            direction_label = 'SELL' # 客户卖出动作
            print(f"🎯 客户行为：卖出 {sell_ccy}，获得 {sell_amount} {sell_ccy}")

        else:
            raise ValueError("trade_direction 必须是 1 或 2")

        # 步骤2：计算新汇率（基于客户行为方向）
        new_rate_val = new_rate(trade_rate=original_rate, direction=direction_label, fluctuation=fluctuation)

        # 步骤3：计算买入金额（客户最终到账金额）
        result = calculate_buy_amount(
            new_exchange_rate=new_rate_val,
            direction=direction_label,
            sell_amount=sell_amount,
            sell_ccy=sell_ccy,
            buy_ccy=buy_ccy
        )

        print("=" * 50)
        print(f"✅ 汇率试算完成！客户将获得 {result['buy_amount']} {result['buy_ccy']}")
        print("=" * 50)