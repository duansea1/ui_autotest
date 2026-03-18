---
name: "kuajing-sql-analyzer"
description: "分析跨境支付系统数据库表结构，生成SQL查询语句和对应代码。当用户需要按月查询T_TRADE_RECEIPT等表的数据时，可使用此技能快速生成分析SQL和代码。"
---

# 跨境SQL分析器技能

## 功能说明

此技能用于分析跨境支付系统的数据库表结构，生成SQL查询语句和对应代码，特别针对T_TRADE_RECEIPT表的按月查询分析。

## 使用场景

当您需要：
- 按月查询T_TRADE_RECEIPT表的数据
- 分析SQL语句的执行逻辑
- 生成对应的Python代码实现

## 支持的表

- **T_TRADE_RECEIPT**: 交易凭证表
- 其他跨境支付系统相关表

## T_TRADE_RECEIPT表结构

| 字段名 | 数据类型 | 描述 |
|-------|---------|------|
| ID | bigint(20) | 自增主键 |
| USER_NO | varchar(64) | 客户号 |
| TRADE_TYPE | tinyint(4) | 交易类型（1：付款，2：提现，3：货币兑换） |
| RECEIPT_NO | varchar(32) | 交易订单号 |
| REQUEST_NO | varchar(32) | 请求单号 |
| ORIGINAL_SALE_CURRENCY | varchar(3) | 原始币种 |
| ORIGINAL_SALE_AMOUNT | decimal(19, 2) | 原始金额 |
| SOURCE_CURRENCY | varchar(8) | 源币种 |
| TARGET_CURRENCY | varchar(255) | 目标币种 |
| TRADE_DIRECTION | tinyint(4) | 交易方向（1：买入，2：卖出） |
| EXCHANGE_RATE | decimal(19, 4) | 汇率 |
| SALE_AMOUNT | decimal(19, 2) | 卖出金额 |
| BUY_AMOUNT | decimal(19, 2) | 买入金额 |
| TRADE_DATE | date | 交易日期 |
| TRADE_TIME | timestamp | 交易时间 |
| STATUS | tinyint(4) | 关联订单交易状态（1：处理中，2：已完成） |
| CLOSING_TYPE | varchar(16) | 交割模式 |
| CLOSING_DATE | varchar(16) | 交割日期 |
| CUR_VERSION | tinyint(4) | 当前记录的版本号 |
| CHANNEL_ORDER_NO | varchar(32) | 渠道货币兑换批次单号 |
| TRADE_STATUS | tinyint(2) | 渠道交易状态（1-待交易、2-处理中、3-交易完成） |
| PROFIT_AMT | decimal(19, 2) | 损益金额 |
| SALES_PROFIT_AMT | decimal(19, 2) | 销售损益金额 |
| TRADES_PROFIT_AMT | decimal(19, 2) | 交易员损益金额 |
| PROFIT_CCY | char(3) | 损益币种 |
| PROFIT_RATIO | decimal(19, 4) | 损益比率 |
| ORDER_GEP_RATE | decimal(19, 6) | 关联订单第三方汇率 |
| ORDER_CREATE_AT | timestamp | 关联订单创建时间 |
| ORDER_AGENT_RATE | decimal(19, 6) | 关联订单代理商汇率 |
| RECEIPT_GEP_RATE | decimal(19, 6) | 凭证第三方汇率 |

## 按月查询SQL模板

### 1. 按月统计交易金额

```sql
SELECT 
    DATE_FORMAT(TRADE_DATE, '%Y-%m') AS month,
    TRADE_TYPE,
    COUNT(*) AS trade_count,
    SUM(SALE_AMOUNT) AS total_sale_amount,
    SUM(BUY_AMOUNT) AS total_buy_amount,
    AVG(EXCHANGE_RATE) AS avg_exchange_rate
FROM 
    T_TRADE_RECEIPT
WHERE 
    TRADE_DATE BETWEEN '${start_date}' AND '${end_date}'
    AND STATUS = 2 -- 已完成的交易
GROUP BY 
    DATE_FORMAT(TRADE_DATE, '%Y-%m'), TRADE_TYPE
ORDER BY 
    month, TRADE_TYPE;
```

### 2. 按月统计客户交易量

```sql
SELECT 
    DATE_FORMAT(TRADE_DATE, '%Y-%m') AS month,
    USER_NO,
    COUNT(*) AS trade_count,
    SUM(SALE_AMOUNT) AS total_sale_amount,
    SUM(BUY_AMOUNT) AS total_buy_amount
FROM 
    T_TRADE_RECEIPT
WHERE 
    TRADE_DATE BETWEEN '${start_date}' AND '${end_date}'
GROUP BY 
    DATE_FORMAT(TRADE_DATE, '%Y-%m'), USER_NO
ORDER BY 
    month, trade_count DESC;
```

### 3. 按月统计币种交易量

```sql
SELECT 
    DATE_FORMAT(TRADE_DATE, '%Y-%m') AS month,
    SOURCE_CURRENCY,
    TARGET_CURRENCY,
    COUNT(*) AS trade_count,
    SUM(SALE_AMOUNT) AS total_sale_amount,
    SUM(BUY_AMOUNT) AS total_buy_amount
FROM 
    T_TRADE_RECEIPT
WHERE 
    TRADE_DATE BETWEEN '${start_date}' AND '${end_date}'
GROUP BY 
    DATE_FORMAT(TRADE_DATE, '%Y-%m'), SOURCE_CURRENCY, TARGET_CURRENCY
ORDER BY 
    month, trade_count DESC;
```

## 生成代码示例

### Python代码实现

```python
# 导入数据库模块
from Kuajing.Common.kjMysql import execute_db

def get_monthly_trade_data(env, start_date, end_date):
    """
    按月查询交易数据
    Args:
        env: 数据库环境参数 (FAT/UAT/FAT_DATA)
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
    Returns:
        查询结果
    """
    sql = """
    SELECT 
        DATE_FORMAT(TRADE_DATE, '%Y-%m') AS month,
        TRADE_TYPE,
        COUNT(*) AS trade_count,
        SUM(SALE_AMOUNT) AS total_sale_amount,
        SUM(BUY_AMOUNT) AS total_buy_amount,
        AVG(EXCHANGE_RATE) AS avg_exchange_rate
    FROM 
        T_TRADE_RECEIPT
    WHERE 
        TRADE_DATE BETWEEN %s AND %s
        AND STATUS = 2 -- 已完成的交易
    GROUP BY 
        DATE_FORMAT(TRADE_DATE, '%Y-%m'), TRADE_TYPE
    ORDER BY 
        month, TRADE_TYPE;
    """
    params = (start_date, end_date)
    result = execute_db(env, sql, params=params)
    return result

# 示例用法
if __name__ == "__main__":
    # 可配置参数
    env = 'FAT'  # 数据库环境参数
    start_date = '2026-01-01'  # 开始日期
    end_date = '2026-01-31'  # 结束日期
    
    # 执行查询
    data = get_monthly_trade_data(env, start_date, end_date)
    
    # 打印结果
    print("按月交易统计数据:")
    for row in data:
        print(f"月份: {row['month']}, 交易类型: {row['TRADE_TYPE']}, 交易笔数: {row['trade_count']}, 总卖出金额: {row['total_sale_amount']}, 总买入金额: {row['total_buy_amount']}, 平均汇率: {row['avg_exchange_rate']}")
```

### 批量查询多个月份

```python
def get_multi_month_trade_data(env, months):
    """
    查询多个月份的交易数据
    Args:
        env: 数据库环境参数
        months: 月份列表，格式为 ['2026-01', '2026-02']
    Returns:
        按月份分组的查询结果
    """
    results = {}
    for month in months:
        start_date = f"{month}-01"
        # 计算当月最后一天
        if month.endswith('12'):
            next_month = f"{int(month[:4]) + 1}-01"
        else:
            next_month = f"{month[:4]}-{int(month[5:]) + 1:02d}"
        end_date = f"{next_month[:4]}-{next_month[5:]}-01"  # 下个月第一天
        
        # 执行查询
        month_data = get_monthly_trade_data(env, start_date, end_date)
        results[month] = month_data
    return results
```

## 使用提示

1. 当您需要按月查询T_TRADE_RECEIPT数据时，只需提供月份范围
2. 系统会自动生成相应的SQL语句和Python代码
3. 您可以根据实际需求修改SQL语句和代码
4. 对于复杂查询，建议使用参数化查询以避免SQL注入风险

## 故障排查

- 如果查询结果为空，请检查日期范围是否正确
- 如果出现SQL执行错误，请检查SQL语句是否正确
- 如果需要连接不同的数据库，请在调用execute_db时指定database参数