# -*- coding: utf-8 -*-
# ---
# 计算客买、客卖浮动值
# @Time: 2024-12-02 15:13
# ---

def calculate_exchange_rates(target_ASK_rate, target_BID_rate, float_type="百分比", 
                            trade_float_ask=0, sale_float_ask=0, agent_float_ask=0, 
                            trade_float_bid=0, sale_float_bid=0, agent_float_bid=0, 
                            merchant_type="当前用户"):
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
    - merchant_type (str): 商户类型，可选值为 "当前用户"、"代理商角色"、"销售角色"、"代理商的商户"、"销售的商户"

    返回:
    - sell_rate (float): 客卖方向汇率
    - buy_rate (float): 客买方向汇率
    """
    # 先计算当前用户汇率（基于所有浮动值）
    if float_type == "百分比":
        current_buy_rate = target_ASK_rate * (1 + trade_float_ask / 100) * (1 + sale_float_ask / 100) * (1 + agent_float_ask / 100)
        current_sell_rate = target_BID_rate * (1 - trade_float_bid/100)*(1 - sale_float_bid/100)*(1 - agent_float_bid/100)
    elif float_type == "BP":
        current_buy_rate = target_ASK_rate + trade_float_ask/100 + sale_float_ask/100 + agent_float_ask/100
        current_sell_rate = target_BID_rate - trade_float_bid/100 - sale_float_bid/100 - agent_float_bid/100
    else:
        raise ValueError("浮动方式只能是 '百分比' 或 'BP'")
    
    # 根据商户类型调整浮动值
    if merchant_type == "当前用户":
        # 当前用户：使用所有浮动值
        actual_trade_float_ask = trade_float_ask
        actual_sale_float_ask = sale_float_ask
        actual_agent_float_ask = agent_float_ask
        actual_trade_float_bid = trade_float_bid
        actual_sale_float_bid = sale_float_bid
        actual_agent_float_bid = agent_float_bid
        
        print(f"\n{float_type}浮动-{merchant_type}汇率计算：")
        result_prefix = f"【{merchant_type}】"
    else:
        # 特定角色：根据角色调整浮动值
        if merchant_type == "代理商的商户" or merchant_type == "代理商角色":
            # 代理商角色：取当前报价源+交易员设置的bp+销售设置的bp +agent_float=0
            actual_trade_float_ask = trade_float_ask
            actual_sale_float_ask = sale_float_ask
            actual_agent_float_ask = 0
            actual_trade_float_bid = trade_float_bid
            actual_sale_float_bid = sale_float_bid
            actual_agent_float_bid = 0
            rule_desc = "代理商角色：取当前报价源+交易员设置的bp+销售设置的bp +agent_float=0"
        elif merchant_type == "销售的商户" or merchant_type == "销售角色":
            # 销售角色：取当前报价源+交易员设置的bp+代理商的bp +sale_float=0
            actual_trade_float_ask = trade_float_ask
            actual_sale_float_ask = 0
            actual_agent_float_ask = agent_float_ask
            actual_trade_float_bid = trade_float_bid
            actual_sale_float_bid = 0
            actual_agent_float_bid = agent_float_bid
            rule_desc = "销售角色：取当前报价源+交易员设置的bp+代理商的bp +sale_float=0"
        else:
            raise ValueError(f"不支持的商户类型：{merchant_type}")
        
        # 显示角色信息
        print(f"\n{float_type}浮动-{merchant_type}汇率计算：")
        # print(f"商户类型规则：")
        # print(f"  {rule_desc}")
        
        # print(f"调整后的实际参数：")
        # print(f"  客买方向：trade_float_ask={trade_float_ask}, sale_float_ask={actual_sale_float_ask}, agent_float_ask={actual_agent_float_ask}")
        # print(f"  客卖方向：trade_float_bid={trade_float_bid}, sale_float_bid={actual_sale_float_bid}, agent_float_bid={actual_agent_float_bid}")
        
        print(f"\n开始计算：")
        result_prefix = f"【{merchant_type}】"
    
    # 计算最终汇率
    if float_type == "百分比":
        # 客买方向汇率 - 百分比浮动
        print(f"{float_type}浮动-客买方向计算：")
        print(f"公式：target_ASK_rate * (1 + trade_float_ask / 100) * (1 + sale_float_ask / 100) * (1 + agent_float_ask / 100)")
        print(f"带入参数：{target_ASK_rate} * (1 + {actual_trade_float_ask} / 100) * (1 + {actual_sale_float_ask} / 100) * (1 + {actual_agent_float_ask} / 100)")
        buy_rate = target_ASK_rate * (1 + actual_trade_float_ask / 100) * (1 + actual_sale_float_ask / 100) * (1 + actual_agent_float_ask / 100)
        
        # 客卖方向汇率 - 百分比浮动
        print(f"{float_type}浮动-客卖方向计算：")
        print(f"公式：target_BID_rate * (1 - trade_float_bid / 100) * (1 - sale_float_bid / 100) * (1 - agent_float_bid / 100)")
        print(f"带入参数：{target_BID_rate} * (1 - {actual_trade_float_bid} / 100) * (1 - {actual_sale_float_bid} / 100) * (1 - {actual_agent_float_bid} / 100)")
        sell_rate = target_BID_rate * (1 - actual_trade_float_bid/100)*(1 - actual_sale_float_bid/100)*(1 - actual_agent_float_bid/100)
    elif float_type == "BP":
        # 客买方向汇率 - BP浮动
        print(f"{float_type}浮动-客买方向计算：")
        print(f"公式：target_ASK_rate + trade_float_ask / 100 + sale_float_ask / 100 + agent_float_ask / 100")
        print(f"带入参数：{target_ASK_rate} + {actual_trade_float_ask} / 100 + {actual_sale_float_ask} / 100 + {actual_agent_float_ask} / 100")
        buy_rate = target_ASK_rate + actual_trade_float_ask/100 + actual_sale_float_ask/100 + actual_agent_float_ask/100
        
        # 客卖方向汇率 - BP浮动
        print(f"{float_type}浮动-客卖方向计算：")
        print(f"公式：target_BID_rate - trade_float_bid / 100 - sale_float_bid / 100 - agent_float_bid / 100")
        print(f"带入参数：{target_BID_rate} - {actual_trade_float_bid} / 100 - {actual_sale_float_bid} / 100 - {actual_agent_float_bid} / 100")
        sell_rate = target_BID_rate - actual_trade_float_bid/100 - actual_sale_float_bid/100 - actual_agent_float_bid/100
    
    # 打印结果，包含当前用户汇率对比
    print(f"当前用户汇率【客买方向】：{current_buy_rate}  ----🚀🚀🚀{result_prefix}【客买方向】结果：{buy_rate}")
    print(f"当前用户汇率【客卖方向】：{current_sell_rate}  ----🚀🚀🚀{result_prefix}【客卖方向】结果：{sell_rate}")
    
    return sell_rate, buy_rate


# 示例用法
if __name__ == "__main__":
    # 提取共有参数 -gep USD/CNH
    target_ASK = 2198.2614 
    target_BID = 2198.0002
    float_type = "百分比"
    
    # 浮动参数 bid-客卖-结汇   ask-客买-购汇
    trade_ask = 0
    sale_ask = -0.1 
    agent_ask = 0
    
    trade_bid = 0
    sale_bid = -1.39   #销售浮动
    agent_bid = 1.9

    
    print("\n\n=== 商户类型汇率计算示例 ===")
    # 代理商角色 - 百分比浮动
    print(f"\n1. 代理商角色 - {float_type}浮动")
    calculate_exchange_rates(target_ASK_rate=target_ASK, target_BID_rate=target_BID, float_type=float_type, 
                             trade_float_ask=trade_ask, sale_float_ask=sale_ask, agent_float_ask=agent_ask, 
                             trade_float_bid=trade_bid, sale_float_bid=sale_bid, agent_float_bid=agent_bid, 
                             merchant_type="代理商角色")
    
    # 销售角色 - 百分比浮动
    print(f"\n2. 销售角色 - {float_type}浮动")
    calculate_exchange_rates(target_ASK_rate=target_ASK, target_BID_rate=target_BID, float_type=float_type, 
                             trade_float_ask=trade_ask, sale_float_ask=sale_ask, agent_float_ask=agent_ask, 
                             trade_float_bid=trade_bid, sale_float_bid=sale_bid, agent_float_bid=agent_bid, 
                             merchant_type="销售角色")
    
    
