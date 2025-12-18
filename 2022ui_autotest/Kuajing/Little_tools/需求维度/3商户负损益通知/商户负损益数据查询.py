"""
@Author    : duansea
@Date      : 2025/7/18 15:22
@Description: [文件功能的简要描述]
"""
import pymysql

from Kuajing.Common.kjMysql import get_db_config

from collections import defaultdict


def little_ccy_fetch_trade_data(env: str, start_time: str, end_time: str):


    db_config = get_db_config(env)

    currency_pairs_condition = "CONCAT(d.SOURCE_CURRENCY, '/', d.TARGET_CURRENCY) IN " \
                               "('USD/PLN', 'USD/DKK', 'USD/MYR', 'USD/IDR', 'USD/PHP', " \
                               "'USD/VND', 'USD/INR', 'USD/THB', 'USD/KRW')"

    sql = f"""
        SELECT 
            d.RECEIPT_NO AS receiptNo,
            d.USER_NO AS userNo, 
            e.USER_NAME AS userName, 
            e.SALE_NO AS saleNo, 
            f.AGENT_NAME AS saleName, 
            IF(d.TRADE_DIRECTION = 1, d.TARGET_CURRENCY, d.SOURCE_CURRENCY) AS sellCcy, 
            d.SALE_AMOUNT AS sellAmt, 
            IF(d.TRADE_DIRECTION = 1, d.SOURCE_CURRENCY, d.TARGET_CURRENCY) AS buyCcy, 
            d.PROFIT_CCY AS profitCcy, 
            NULL AS profitAmt, 
            NULL AS tradeProfit, 
            d.SALES_PROFIT_AMT AS saleProfitAmt 
        FROM BAOFU_TRADE.T_TRADE_RECEIPT d 
        LEFT JOIN BAOFU_CRM.T_USER_INFO e ON d.USER_NO = e.USER_NO 
        LEFT JOIN BAOFU_CBCA.T_AGENT_INFO f ON e.SALE_NO = f.AGENT_NO AND f.AGENT_TYPE = 3 
        WHERE d.STATUS = 2 
          AND d.TRADE_STATUS IN (1, 2) 
          AND d.CREATE_AT >= '{start_time}' 
          AND d.CREATE_AT < '{end_time}' 
          AND d.PROFIT_CCY IS NOT NULL 
          
          AND ({currency_pairs_condition});
    """
    # # AND d.SALES_PROFIT_AMT < 0

    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            # 汇总数据结构：按商户+销售+币种方向分组
            amount_summary = defaultdict(lambda: {
                'totalSellAmt': 0.0,
                'totalSaleProfit': 0.0,
                'profitCcy': None,
                'saleName': None,
                'buyCcy': None,
                'sellCcy': None
            })

            # 打印表头 - 明细
            print("=== 明细数据 ===")
            print(f"{'交易单号':<15}\t{'商户号/商户名称':<40}\t{'销售':<30}\t{'买入币种':<6}\t{'卖出币种':<6}\t"
                  f"{'卖出金额':<10}\t{'总损益/币种':<12}\t{'销售损益/币种':<12}\t{'外汇交易员损益/币种':<12}")

            for row in rows:
                receipt_no = row['receiptNo']
                user_info = f"{row['userNo']}/{row['userName']}"
                sale_info = f"{row['saleNo']}/{row['saleName']}"
                buy_ccy = row['buyCcy']
                sell_ccy = row['sellCcy']
                sell_amt = float(row['sellAmt']) if row['sellAmt'] else 0.0
                profit_ccy = row['profitCcy']
                sale_profit_amt = float(row['saleProfitAmt']) if row['saleProfitAmt'] else 0.0

                # 打印明细数据
                print(f"{receipt_no:<15}\t{user_info:<40}\t{sale_info:<30}\t{buy_ccy:<6}\t{sell_ccy:<6}\t"
                      f"{sell_amt:<10.2f}\t{'-':<12}\t{sale_profit_amt:.2f}/{profit_ccy:<12}\t{'-':<12}")

                # 汇总 key
                key = (row['userNo'], row['userName'], row['saleNo'], row['saleName'], buy_ccy, sell_ccy)

                # 累计金额
                amount_summary[key]['totalSellAmt'] += sell_amt
                amount_summary[key]['totalSaleProfit'] += sale_profit_amt
                amount_summary[key]['profitCcy'] = profit_ccy
                amount_summary[key]['saleName'] = row['saleName']
                amount_summary[key]['buyCcy'] = buy_ccy
                amount_summary[key]['sellCcy'] = sell_ccy

            # 打印汇总数据 - 累计卖出金额和销售损益
            print("\n=== 汇总数据（累计卖出金额 > 0） ===")
            print(f"🚀{'商户号/商户名称':<40}\t{'销售':<30}\t{'买入币种':<6}\t{'卖出币种':<6}\t"
                  f"{'卖出金额':<19}\t{'总损益/币种':<19}\t{'销售损益/币种':<19}\t{'外汇交易员损益/币种':<12}")

            for key, data in amount_summary.items():
                user_no, user_name, sale_no, sale_name, buy_ccy, sell_ccy = key
                total_sell_amt = data['totalSellAmt']
                total_sale_profit = data['totalSaleProfit']
                profit_ccy = data['profitCcy']

                if total_sell_amt > 0:  # 只打印有交易金额的组合
                    user_info = f"{user_no}/{user_name}"
                    sale_info = f"{sale_no}/{sale_name}"
                    print(f"{user_info:<40}\t{sale_info:<30}\t{buy_ccy:<6}\t{sell_ccy:<6}\t"
                          f"{total_sell_amt:<10.2f}\t{'----':<19}\t{total_sale_profit:.2f}/{profit_ccy:<19}\t{'----':<19}")

def big_ccy_fetch_trade_data(env: str, start_time: str, end_time: str):
    """
    查询并打印大币种交易数据（排除小币种）
    """
    import pymysql
    from collections import defaultdict

    db_config = get_db_config(env)

    # 排除的小币种对
    excluded_pairs = (
        "'USD/PLN', 'USD/DKK', 'USD/MYR', 'USD/IDR', 'USD/PHP', "
        "'USD/VND', 'USD/INR', 'USD/THB', 'USD/KRW'"
    )

    sql = f"""
        SELECT 
        receipt_no,
            a.USER_NO AS userNo, 
            b.USER_NAME AS userName, 
            b.SALE_NO AS saleNo, 
            c.AGENT_NAME AS saleName, 
            IF(a.TRADE_DIRECTION = 1, a.TARGET_CURRENCY, a.SOURCE_CURRENCY) AS sellCcy, 
            a.SALE_AMOUNT AS sellAmt, 
            IF(a.TRADE_DIRECTION = 1, a.SOURCE_CURRENCY, a.TARGET_CURRENCY) AS buyCcy, 
            a.PROFIT_CCY AS profitCcy, 
            a.PROFIT_AMT AS profitAmt, 
            a.TRADES_PROFIT_AMT AS tradeProfit, 
            a.SALES_PROFIT_AMT AS saleProfitAmt 
        FROM BAOFU_TRADE.T_TRADE_RECEIPT a 
        LEFT JOIN BAOFU_CRM.T_USER_INFO b ON a.USER_NO = b.USER_NO 
        LEFT JOIN BAOFU_CBCA.T_AGENT_INFO c ON b.SALE_NO = c.AGENT_NO AND c.AGENT_TYPE = 3 
        WHERE a.STATUS IN (1, 2) 
          AND a.TRADE_STATUS = 3 
          AND a.CREATE_AT >= '{start_time}' 
          AND a.CREATE_AT < '{end_time}' 
          AND CONCAT(a.SOURCE_CURRENCY, '/', a.TARGET_CURRENCY) NOT IN ({excluded_pairs});
    """

    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            # 用于汇总：按商户+销售+币种方向分组，统计累计卖出金额、销售损益、总损益
            amount_summary = defaultdict(lambda: {
                'totalSellAmt': 0.0,
                'totalSaleProfit': 0.0,
                'totalProfitAmt': 0.0,
                'profitCcy': None,
                'saleName': None,
                'buyCcy': None,
                'sellCcy': None,
                'tradeProfit': 0.0
            })

            # 打印表头 - 明细
            print("=== 大币种明细数据 ===")
            print(f"{'交易单号':<15}\t{'商户号/商户名称':<40}\t{'销售':<30}\t{'买入币种':<6}\t{'卖出币种':<6}\t"
                  f"{'卖出金额':<10}\t{'总损益/币种':<12}\t{'销售损益/币种':<12}\t{'外汇交易员损益/币种':<12}")

            for row in rows:
                receipt_no = row.get('receipt_no', '')  # 假设没有receiptNo，可以留空或使用其他字段替代
                user_info = f"{row['userNo']}/{row['userName']}"
                sale_info = f"{row['saleNo']}/{row['saleName']}"
                buy_ccy = row['buyCcy']
                sell_ccy = row['sellCcy']
                sell_amt = float(row['sellAmt']) if row['sellAmt'] else 0.0
                profit_ccy = row['profitCcy']
                sale_profit_amt = float(row['saleProfitAmt']) if row['saleProfitAmt'] else 0.0
                profit_amt = float(row['profitAmt']) if row['profitAmt'] else 0.0  # 新增字段
                tradeProfit = float(row['tradeProfit']) if row['tradeProfit'] else 0.0  # 新增字段

                # 打印明细数据
                print(f"{receipt_no:<15}\t{user_info:<40}\t{sale_info:<30}\t{buy_ccy:<6}\t{sell_ccy:<6}\t"
                      f"{sell_amt:<10.2f}\t{profit_amt:.2f}/{profit_ccy:<12}\t{sale_profit_amt:.2f}/{profit_ccy:<12}\t{tradeProfit:<12.2f}")

                # 汇总 key
                key = (row['userNo'], row['userName'], row['saleNo'], row['saleName'], buy_ccy, sell_ccy)

                # 累计金额
                amount_summary[key]['totalSellAmt'] += sell_amt
                amount_summary[key]['totalSaleProfit'] += sale_profit_amt
                amount_summary[key]['totalProfitAmt'] += profit_amt
                amount_summary[key]['tradeProfit'] += tradeProfit
                amount_summary[key]['profitCcy'] = profit_ccy
                amount_summary[key]['saleName'] = row['saleName']
                amount_summary[key]['buyCcy'] = buy_ccy
                amount_summary[key]['sellCcy'] = sell_ccy

            # 打印汇总数据 - 累计卖出金额 > 0 的组合
            print("\n=== 大币种汇总数据（累计卖出金额 > 0） ===")
            print(f"🚀{'商户号/商户名称':<40}\t{'销售':<30}\t{'买入币种':<6}\t{'卖出币种':<6}\t"
                  f"{'卖出金额':<10}\t{'总损益/币种':<12}\t{'销售损益/币种':<12}\t{'外汇交易员损益/币种':<12}")

            for key, data in amount_summary.items():
                user_no, user_name, sale_no, sale_name, buy_ccy, sell_ccy = key
                total_sell_amt = data['totalSellAmt']
                total_sale_profit = data['totalSaleProfit']
                total_profit_amt = data['totalProfitAmt']
                profit_ccy = data['profitCcy']
                tradeProfit = data['tradeProfit']

                if total_sell_amt > 0:
                    user_info = f"{user_no}/{user_name}"
                    sale_info = f"{sale_no}/{sale_name}"
                    print(f"{user_info:<40}\t{sale_info:<30}\t{buy_ccy:<6}\t{sell_ccy:<6}\t"
                          f"{total_sell_amt:<10.2f}\t{total_profit_amt:.2f}/{profit_ccy:<12}\t"
                          f"{total_sale_profit:.2f}/{profit_ccy:<12}\t{tradeProfit:<12.2f}")

if __name__ == '__main__':
    # 小币种数据
    little_ccy_fetch_trade_data('UAT', '2025-07-23 00:00:00', '2025-07-24 00:00:00')

    # 大币种数据
    big_ccy_fetch_trade_data('UAT', '2025-07-23 00:00:00', '2025-07-24 00:00:00')