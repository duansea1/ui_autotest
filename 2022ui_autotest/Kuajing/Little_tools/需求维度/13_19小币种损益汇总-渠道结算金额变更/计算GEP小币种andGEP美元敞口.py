def calculate_gep_small_currency_exposure(
    customer_monthly_sell_sc,  # 客户当月卖出金额（小币种）
    customer_monthly_buy_sc,   # 客户当月买入金额（小币种）
    customer_fee_sc,           # 客户手续费（小币种）
    channel_monthly_settlement_sc,  # 渠道当月结算金额（小币种）
    last_month_gep_sc_exposure  # 上月GEP小币种敞口
):
    """
    计算GEP小币种敞口
    公式：GEP小币种敞口 = 客户当月卖出金额（小币种） - 客户当月买入金额（小币种） + 客户手续费（小币种） - 渠道当月结算金额（小币种） + 上月GEP小币种敞口
    
    Args:
        customer_monthly_sell_sc: 客户当月卖出金额（小币种）
        customer_monthly_buy_sc: 客户当月买入金额（小币种）
        customer_fee_sc: 客户手续费（小币种）
        channel_monthly_settlement_sc: 渠道当月结算金额（小币种）
        last_month_gep_sc_exposure: 上月GEP小币种敞口
    
    Returns:
        float: 当月GEP小币种敞口
    """
    return (customer_monthly_sell_sc - customer_monthly_buy_sc + 
            customer_fee_sc - channel_monthly_settlement_sc + 
            last_month_gep_sc_exposure)


def calculate_gep_usd_exposure(
    channel_monthly_settlement_usd,  # 渠道当月结算金额（美元）
    customer_monthly_sell_usd,       # 客户卖出金额（美元）
    customer_monthly_buy_usd,        # 客户买入金额（美元）
    customer_fee_sc,                 # 客户手续费（小币种）
    monthly_report_system_rate,      # 当月报表系统汇率
    last_month_gep_usd_exposure      # 上月GEP美元敞口
):
    """
    计算GEP美元敞口
    公式：GEP美元敞口 = 渠道当月结算金额（美元） + 客户卖出金额（美元） - 客户买入金额（美元） - 客户手续费（小币种）*当月报表系统汇率 + 上月GEP美元敞口
    
    Args:
        channel_monthly_settlement_usd: 渠道当月结算金额（美元）
        customer_monthly_sell_usd: 客户卖出金额（美元）
        customer_monthly_buy_usd: 客户买入金额（美元）
        customer_fee_sc: 客户手续费（小币种）
        monthly_report_system_rate: 当月报表系统汇率
        last_month_gep_usd_exposure: 上月GEP美元敞口
    
    Returns:
        float: 当月GEP美元敞口
    """
    return (channel_monthly_settlement_usd + customer_monthly_sell_usd - 
            customer_monthly_buy_usd - customer_fee_sc * monthly_report_system_rate + 
            last_month_gep_usd_exposure)


if __name__ == "__main__":
    # 客户当月卖出金额（小币种）=21452
    customer_monthly_sell_sc = 18923496171
    
    # 客户当月买入金额（小币种）=165000
    customer_monthly_buy_sc = 9169005890
    
    # 客户当月手续费（小币种）=18126
    customer_fee_sc = 85193758
    
    # 渠道当月结算金额（小币种）=-10000
    channel_monthly_settlement_sc = 7084666327
    
    # 上月GEP小币种敞口=-1889380
    last_month_gep_sc_exposure = -5077046432.7
    
    # 渠道当月结算金额（美元）=-7
    channel_monthly_settlement_usd = 4943605.12
    
    # 客户当月卖出金额（美元）=110.83
    customer_monthly_sell_usd = 6263704.34
    
    # 客户当月买入金额（美元）=14.82
    customer_monthly_buy_usd = 12518391
    
    # 当月报表系统汇率=0.0006912426
    monthly_report_system_rate = 	0.0007290151
    
    # 上月GEP美元敞口=-20.63
    last_month_gep_usd_exposure =3720403.87
    
    # 计算GEP小币种敞口
    gep_small_currency_exposure = calculate_gep_small_currency_exposure(
        customer_monthly_sell_sc,
        customer_monthly_buy_sc,
        customer_fee_sc,
        channel_monthly_settlement_sc,
        last_month_gep_sc_exposure
    )
    
    # 计算GEP美元敞口
    gep_usd_exposure = calculate_gep_usd_exposure(
        channel_monthly_settlement_usd,
        customer_monthly_sell_usd,
        customer_monthly_buy_usd,
        customer_fee_sc,
        monthly_report_system_rate,
        last_month_gep_usd_exposure
    )
    
    # 输出计算结果
    print("=== GEP敞口计算结果 ===")
    print(f"GEP小币种敞口: {gep_small_currency_exposure:,.2f}")
    print(f"GEP美元敞口: {gep_usd_exposure:.6f}")
    
    # 输出计算过程，便于验证
    print("\n=== GEP小币种敞口计算过程 ===")
    print(f"公式: GEP小币种敞口 = 客户当月卖出金额（小币种） - 客户当月买入金额（小币种） + 客户手续费（小币种） - 渠道当月结算金额（小币种） + 上月GEP小币种敞口")
    print(f"计算: {customer_monthly_sell_sc} - {customer_monthly_buy_sc} + {customer_fee_sc} - ({channel_monthly_settlement_sc}) + ({last_month_gep_sc_exposure}) = {gep_small_currency_exposure:,.2f}")
    
    print("\n=== GEP美元敞口计算过程 ===")
    print(f"公式: GEP美元敞口 = 渠道当月结算金额（美元） + 客户卖出金额（美元） - 客户买入金额（美元） - 客户手续费（小币种）*当月报表系统汇率 + 上月GEP美元敞口")
    print(f"计算: ({channel_monthly_settlement_usd}) + {customer_monthly_sell_usd} - {customer_monthly_buy_usd} - ({customer_fee_sc} * {monthly_report_system_rate}) + ({last_month_gep_usd_exposure}) = {gep_usd_exposure:.6f}")
