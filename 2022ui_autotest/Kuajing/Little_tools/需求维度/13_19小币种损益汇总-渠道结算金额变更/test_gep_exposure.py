#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from 计算GEP小币种andGEP美元敞口 import calculate_gep_small_currency_exposure, calculate_gep_usd_exposure

# 测试数据
test_data = {
    "customer_monthly_sell_sc": 10000.0,  # 客户当月卖出金额（小币种）
    "customer_monthly_buy_sc": 5000.0,    # 客户当月买入金额（小币种）
    "customer_fee_sc": 500.0,             # 客户手续费（小币种）
    "channel_monthly_settlement_sc": 3000.0,  # 渠道当月结算金额（小币种）
    "last_month_gep_sc_exposure": 1000.0,  # 上月GEP小币种敞口
    "channel_monthly_settlement_usd": 2000.0,  # 渠道当月结算金额（美元）
    "customer_monthly_sell_usd": 8000.0,   # 客户卖出金额（美元）
    "customer_monthly_buy_usd": 4000.0,    # 客户买入金额（美元）
    "monthly_report_system_rate": 6.5,     # 当月报表系统汇率
    "last_month_gep_usd_exposure": 2000.0  # 上月GEP美元敞口
}

# 计算结果
small_currency_exposure = calculate_gep_small_currency_exposure(
    test_data["customer_monthly_sell_sc"],
    test_data["customer_monthly_buy_sc"],
    test_data["customer_fee_sc"],
    test_data["channel_monthly_settlement_sc"],
    test_data["last_month_gep_sc_exposure"]
)

usd_exposure = calculate_gep_usd_exposure(
    test_data["channel_monthly_settlement_usd"],
    test_data["customer_monthly_sell_usd"],
    test_data["customer_monthly_buy_usd"],
    test_data["customer_fee_sc"],
    test_data["monthly_report_system_rate"],
    test_data["last_month_gep_usd_exposure"]
)

# 输出结果
print("=== GEP敞口计算测试结果 ===")
print(f"GEP小币种敞口: {small_currency_exposure:.2f}")
print(f"GEP美元敞口: {usd_exposure:.2f}")

# 验证计算过程
print("\n=== 计算过程验证 ===")
print("GEP小币种敞口计算过程:")
print(f"客户当月卖出金额（小币种）: {test_data['customer_monthly_sell_sc']}")
print(f"- 客户当月买入金额（小币种）: {test_data['customer_monthly_buy_sc']}")
print(f"+ 客户手续费（小币种）: {test_data['customer_fee_sc']}")
print(f"- 渠道当月结算金额（小币种）: {test_data['channel_monthly_settlement_sc']}")
print(f"+ 上月GEP小币种敞口: {test_data['last_month_gep_sc_exposure']}")
print(f"= {test_data['customer_monthly_sell_sc']} - {test_data['customer_monthly_buy_sc']} + {test_data['customer_fee_sc']} - {test_data['channel_monthly_settlement_sc']} + {test_data['last_month_gep_sc_exposure']} = {small_currency_exposure:.2f}")

print("\nGEP美元敞口计算过程:")
print(f"渠道当月结算金额（美元）: {test_data['channel_monthly_settlement_usd']}")
print(f"+ 客户卖出金额（美元）: {test_data['customer_monthly_sell_usd']}")
print(f"- 客户买入金额（美元）: {test_data['customer_monthly_buy_usd']}")
print(f"- 客户手续费（小币种）*当月报表系统汇率: {test_data['customer_fee_sc']} * {test_data['monthly_report_system_rate']} = {test_data['customer_fee_sc'] * test_data['monthly_report_system_rate']:.2f}")
print(f"+ 上月GEP美元敞口: {test_data['last_month_gep_usd_exposure']}")
print(f"= {test_data['channel_monthly_settlement_usd']} + {test_data['customer_monthly_sell_usd']} - {test_data['customer_monthly_buy_usd']} - ({test_data['customer_fee_sc']} * {test_data['monthly_report_system_rate']:.2f}) + {test_data['last_month_gep_usd_exposure']} = {usd_exposure:.2f}")
