# -*- coding: utf-8 -*-
# ---
# 计算客买、客卖浮动值
# @Time: 2024-12-02 15:13
# ---

def calculate_exchange_rates(target_ASK_rate, target_BID_rate, float_type="百分比", 
                            trade_float_ask=0, sale_float_ask=0, agent_float_ask=0, 
                            trade_float_bid=0, sale_float_bid=0, agent_float_bid=0, 
                            merchant_type=None):
    """
    计算客卖方向和客买方向的汇率。

    参数:
    - target_ASK_rate (float): 目标汇率-客买方向
    - target_BID_rate (float): 目标汇率-客卖方向
    - float_type (str): 浮动方式，可选值为 "百分比" 或 "BP"
    - trade_float_ask-交易员设置的浮动（客买方向）
    - sale_float_ask-销售设置的浮动（客买方向）
    - agent_float_ask-代理商设置的浮动（客买方向）
    - trade_float_bid-交易员设置的浮动（客卖方向）
    - sale_float_bid-销售设置的浮动（客卖方向）
    - agent_float_bid-代理商设置的浮动（客卖方向）
    - merchant_type (str, optional): 商户类型，用于区分不同计算场景

    返回:
    - sell_rate (float): 客卖方向汇率
    - buy_rate (float): 客买方向汇率
    """
    # 确定结果前缀，区分是否有商户类型
    result_prefix = f"【{merchant_type}】" if merchant_type else ""
    
    if float_type == "百分比":
        # 客买方向汇率 - 百分比浮动
        print(f"{float_type}浮动-客买方向计算：")
        print(f"公式：target_ASK_rate * (1 + trade_float_ask / 100) * (1 + sale_float_ask / 100) * (1 + agent_float_ask / 100)")
        print(f"带入参数：{target_ASK_rate} * (1 + {trade_float_ask} / 100) * (1 + {sale_float_ask} / 100) * (1 + {agent_float_ask} / 100)")
        buy_rate = target_ASK_rate * (1 + trade_float_ask / 100) * (1 + sale_float_ask / 100) * (1 + agent_float_ask / 100)
        print(f"🚀🚀🚀{result_prefix}【客买方向】结果：{buy_rate}")
        
        # 客卖方向汇率 - 百分比浮动
        print(f"{float_type}浮动-客卖方向计算：")
        print(f"公式：target_BID_rate * (1 - trade_float_bid / 100) * (1 - sale_float_bid / 100) * (1 - agent_float_bid / 100)")
        print(f"带入参数：{target_BID_rate} * (1 - {trade_float_bid} / 100) * (1 - {sale_float_bid} / 100) * (1 - {agent_float_bid} / 100)")
        sell_rate = target_BID_rate * (1 - trade_float_bid/100)*(1 - sale_float_bid/100)*(1 - agent_float_bid/100)
        print(f"🚀🚀🚀{result_prefix}【客卖方向】结果：{sell_rate}")
    elif float_type == "BP":
        # 客买方向汇率 - BP浮动
        print(f"{float_type}浮动-客买方向计算：")
        print(f"公式：target_ASK_rate + trade_float_ask / 100 + sale_float_ask / 100 + agent_float_ask / 100")
        print(f"带入参数：{target_ASK_rate} + {trade_float_ask} / 100 + {sale_float_ask} / 100 + {agent_float_ask} / 100")
        buy_rate = target_ASK_rate + trade_float_ask/100 + sale_float_ask/100 + agent_float_ask/100
        print(f"🚀🚀🚀{result_prefix}【客买方向】结果：{buy_rate}")
        
        # 客卖方向汇率 - BP浮动
        print(f"{float_type}浮动-客卖方向计算：")
        print(f"公式：target_BID_rate - trade_float_bid / 100 - sale_float_bid / 100 - agent_float_bid / 100")
        print(f"带入参数：{target_BID_rate} - {trade_float_bid} / 100 - {sale_float_bid} / 100 - {agent_float_bid} / 100")
        sell_rate = target_BID_rate - trade_float_bid/100 - sale_float_bid/100 - agent_float_bid/100
        print(f"🚀🚀🚀{result_prefix}【客卖方向】结果：{sell_rate}")
    else:
        raise ValueError("浮动方式只能是 '百分比' 或 'BP'")

    return sell_rate, buy_rate



def calculate_merchant_rate(target_ASK_rate, target_BID_rate, merchant_type, float_type="百分比", 
                            trade_float_ask=0, sale_float_ask=0, agent_float_ask=0, 
                            trade_float_bid=0, sale_float_bid=0, agent_float_bid=0):
    """
    根据商户类型计算汇率。

    参数:
    - target_ASK_rate (float): 目标汇率-客买方向
    - target_BID_rate (float): 目标汇率-客卖方向
    - merchant_type (str): 商户类型，可选值为 "代理商角色" 或 "销售角色"
    - float_type (str): 浮动方式，可选值为 "百分比" 或 "BP"
    - trade_float_ask-交易员设置的浮动（客买方向）
    - sale_float_ask-销售设置的浮动（客买方向）
    - agent_float_ask-代理商设置的浮动（客买方向）
    - trade_float_bid-交易员设置的浮动（客卖方向）
    - sale_float_bid-销售设置的浮动（客卖方向）
    - agent_float_bid-代理商设置的浮动（客卖方向）

    返回:
    - sell_rate (float): 客卖方向汇率
    - buy_rate (float): 客买方向汇率
    """
    # 根据商户类型设置浮动值
    if merchant_type == "代理商角色":
        # 代理商角色：取当前报价源+交易员设置的bp+销售设置的bp +agent_float=0
        actual_sale_float_ask = sale_float_ask
        actual_agent_float_ask = 0
        actual_sale_float_bid = sale_float_bid
        actual_agent_float_bid = 0
    elif merchant_type == "销售角色":
        # 销售角色：取当前报价源+交易员设置的bp+代理商的bp +sale_float=0
        actual_sale_float_ask = 0
        actual_agent_float_ask = agent_float_ask
        actual_sale_float_bid = 0
        actual_agent_float_bid = agent_float_bid
    else:
        raise ValueError("商户类型只能是 '代理商角色' 或 '销售角色'")
    
    print(f"\n{merchant_type} - {float_type}浮动计算：")
    print(f"商户类型规则：")
    if merchant_type == "代理商角色":
        print(f"  代理商角色：取当前报价源+交易员设置的bp+销售设置的bp +agent_float=0")
    else:
        print(f"  销售角色：取当前报价源+交易员设置的bp+代理商的bp +sale_float=0")
    
    print(f"调整后的实际参数：")
    print(f"  客买方向：trade_float_ask={trade_float_ask}, sale_float_ask={actual_sale_float_ask}, agent_float_ask={actual_agent_float_ask}")
    print(f"  客卖方向：trade_float_bid={trade_float_bid}, sale_float_bid={actual_sale_float_bid}, agent_float_bid={actual_agent_float_bid}")
    
    print(f"\n开始计算：")
    # 调用统一计算函数，传递商户类型
    return calculate_exchange_rates(target_ASK_rate, target_BID_rate, float_type, 
                                  trade_float_ask, actual_sale_float_ask, actual_agent_float_ask, 
                                  trade_float_bid, actual_sale_float_bid, actual_agent_float_bid, 
                                  merchant_type=merchant_type)


# 示例用法
if __name__ == "__main__":
    # 提取共有参数 -gep USD/CNH
    # target_ASK = 704.08  
    # target_BID = 704.05
    # float_type = "BP"
    
    # # 浮动参数 bid-客卖-结汇   ask-客买-购汇
    # trade_ask = 0
    # sale_ask = 30 
    # agent_ask = -100
    
    # trade_bid = 0
    # sale_bid = 40   #销售浮动
    # agent_bid = 0

    #   usd/VND-百分比浮动
    # target_ASK = 2632280
    # target_BID = 2631600
    # float_type = "百分比"
    
    # # 浮动参数-ask-客买 
    # trade_ask = -3
    # sale_ask = 0
    # agent_ask = 0
    # # 浮动值-bid-客卖
    # trade_bid = 1
    # sale_bid = 0
    # agent_bid = -3


    target_ASK = 2201.0012  
    target_BID = 2200.8004
    float_type = "百分比"
    
    # 浮动参数 bid-客卖-结汇   ask-客买-购汇
    trade_ask = 0
    sale_ask = 1.06 
    agent_ask = 0
    
    trade_bid = 0
    sale_bid = 0   #销售浮动
    agent_bid = 1.9
    



    print(f"\n{float_type}")
    calculate_exchange_rates(target_ASK_rate=target_ASK, target_BID_rate=target_BID, float_type=float_type, 
                             trade_float_ask=trade_ask, sale_float_ask=sale_ask, agent_float_ask=agent_ask, 
                             trade_float_bid=trade_bid, sale_float_bid=sale_bid, agent_float_bid=agent_bid)
    
    print("\n\n=== 商户类型汇率计算示例 ===")
    # 代理商角色 - BP浮动
    print(f"\n1. 代理商角色 - {float_type}浮动")
    calculate_merchant_rate(merchant_type="代理商角色", target_ASK_rate=target_ASK, target_BID_rate=target_BID, float_type=float_type, 
                             trade_float_ask=trade_ask, sale_float_ask=sale_ask, agent_float_ask=agent_ask, 
                             trade_float_bid=trade_bid, sale_float_bid=sale_bid, agent_float_bid=agent_bid)
    
    # 销售角色 - BP浮动
    print(f"\n2. 销售角色 - {float_type}浮动")
    calculate_merchant_rate(merchant_type="销售角色", target_ASK_rate=target_ASK, target_BID_rate=target_BID, float_type=float_type, 
                             trade_float_ask=trade_ask, sale_float_ask=sale_ask, agent_float_ask=agent_ask, 
                             trade_float_bid=trade_bid, sale_float_bid=sale_bid, agent_float_bid=agent_bid)
    
    