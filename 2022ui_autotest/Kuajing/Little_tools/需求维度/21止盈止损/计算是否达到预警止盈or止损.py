import logging
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(project_root)

# 导入数据库配置模块
from Kuajing.Common.kjMysql import get_db_config
import pymysql

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_profit_loss_threshold(trader_profit_loss, profit_loss_currency, trade_amount, 
                                 # 止盈参数配置
                                 profit_type, profit_value, 
                                 # 止损参数配置
                                 loss_type, loss_value,
                                 # 固定汇率专用参数
                                 direction=None, currency_pair=None, channel_rate=None):
    """
    检查是否达到止盈或止损阈值
    
    参数:
    trader_profit_loss: float, 预计交易员损益（汇总）
    
    profit_loss_currency: str, 损益币种
    trade_amount: float, 买入或卖出金额（与损益币种一致）
    
    # 止盈参数配置
    profit_type: str, 止盈阈值类型 ('percentage' 百分比, 'fixed_amount' 固定金额, 'fixed_rate' 固定汇率)
    profit_value: float, 止盈阈值数值
    
    # 止损参数配置
    loss_type: str, 止损阈值类型 ('percentage' 百分比, 'fixed_amount' 固定金额, 'fixed_rate' 固定汇率)
    loss_value: float, 止损阈值数值
    
    # 固定汇率专用参数（仅当profit_type或loss_type为'fixed_rate'时需要）
    direction: str, 交易方向 ('buy' 买入, 'sell' 卖出)
    currency_pair: str, 货币对 (如 'USD/CNH')
    channel_rate: float, 渠道实时汇率
    
    返回:
    tuple: (是否触发止盈, 是否触发止损)
    """
    # 初始化结果
    profit_triggered = False
    loss_triggered = False
    
    # 止盈判断
    profit_reason = ""
    # 固定汇率类型：直接根据汇率判断，不需要考虑交易员收益
    if profit_type == 'fixed_rate':
        # 固定汇率止盈：根据不同方向判断汇率是否更优或一样
        # 买入方向：渠道汇率低于固定汇率，渠道汇率优
        # 卖出方向：渠道汇率高于固定汇率，渠道汇率优
        if direction and currency_pair and channel_rate is not None:
            if direction == 'buy':
                # 买入方向：渠道汇率 < 固定汇率 → 汇率更优
                if channel_rate <= profit_value:
                    profit_triggered = True
                    profit_reason = f"固定汇率止盈：{currency_pair} 买入方向，渠道汇率{channel_rate} <= 止盈阈值{profit_value}，🔍渠道汇率更优或一样🔍"
                else:
                    profit_triggered = False
                    profit_reason = f"固定汇率止盈：{currency_pair} 买入方向，渠道汇率{channel_rate} > 止盈阈值{profit_value}，🔍设置的阈值汇率更优🔍"
            elif direction == 'sell':
                # 卖出方向：渠道汇率 > 固定汇率 → 汇率更优
                if channel_rate >= profit_value:
                    profit_triggered = True
                    profit_reason = f"固定汇率止盈：{currency_pair} 卖出方向，渠道汇率{channel_rate} >= 止盈阈值{profit_value}，🔍渠道汇率更优或一样🔍"
                else:
                    profit_triggered = False
                    profit_reason = f"固定汇率止盈：{currency_pair} 卖出方向，渠道汇率{channel_rate} < 止盈阈值{profit_value}，🔍设置的阈值汇率更优🔍"
            else:
                profit_reason = f"固定汇率止盈：无效的交易方向{direction}"
        else:
            profit_reason = "固定汇率止盈：缺少必要参数（direction、currency_pair或channel_rate）"
    # 非固定汇率类型：需要考虑交易员收益为正
    elif trader_profit_loss > 0:
        if profit_type == 'percentage':
            # 百分比止盈：(损益/交易金额)*100% >= 止盈阈值
            calculation_result = (trader_profit_loss / trade_amount) * 100
            if calculation_result >= profit_value:
                profit_triggered = True
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，(预计交易员损益/交易金额)*100% = {calculation_result:.2f}% >= 止盈阈值{profit_value}%"
            else:
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，(预计交易员损益/交易金额)*100% = {calculation_result:.2f}% < 止盈阈值{profit_value}%"
        elif profit_type == 'fixed_amount':
            # 固定金额止盈：损益 >= 止盈阈值
            if trader_profit_loss >= profit_value:
                profit_triggered = True
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，预计交易员损益 >= 止盈阈值{profit_value}"
            else:
                profit_reason = f"预计交易员损益为正数({trader_profit_loss})，预计交易员损益 < 止盈阈值{profit_value}"
    else:
        profit_reason = f"预计交易员损益({trader_profit_loss})不为正数，不触发止盈"
    
    # 止损判断
    loss_reason = ""
    # 固定汇率类型：直接根据汇率判断，不需要考虑交易员收益
    if loss_type == 'fixed_rate':
        # 固定汇率止损：根据不同方向判断汇率是否更差或一样
        # 买入方向：渠道汇率高于固定汇率，渠道汇率差
        # 卖出方向：渠道汇率低于固定汇率，渠道汇率差
        if direction and currency_pair and channel_rate is not None:
            if direction == 'buy':
                # 买入方向：渠道汇率 > 固定汇率 → 阈值汇率更优
                if channel_rate >= loss_value:
                    loss_triggered = True
                    loss_reason = f"固定汇率止损：{currency_pair} 买入方向，渠道汇率{channel_rate} >= 止损阈值{loss_value}，🔍设置的阈值汇率更优🔍"
                else:
                    loss_triggered = False
                    loss_reason = f"固定汇率止损：{currency_pair} 买入方向，渠道汇率{channel_rate} < 止损阈值{loss_value}，🔍渠道汇率更优🔍"
            elif direction == 'sell':
                # 卖出方向：渠道汇率 < 固定汇率 → 阈值汇率更优
                if channel_rate <= loss_value:
                    loss_triggered = True
                    loss_reason = f"固定汇率止损：{currency_pair} 卖出方向，渠道汇率{channel_rate} <= 止损阈值{loss_value}，🔍设置的阈值汇率更优🔍"
                else:
                    loss_triggered = False
                    loss_reason = f"固定汇率止损：{currency_pair} 卖出方向，渠道汇率{channel_rate} > 止损阈值{loss_value}，🔍渠道汇率更优🔍"
            else:
                loss_reason = f"固定汇率止损：无效的交易方向{direction}"
        else:
            loss_reason = "固定汇率止损：缺少必要参数（direction、currency_pair或channel_rate）"
    # 非固定汇率类型：需要考虑交易员收益为负
    elif trader_profit_loss < 0:
        abs_profit_loss = abs(trader_profit_loss)
        if loss_type == 'percentage':
            # 百分比止损：(损益绝对值/交易金额)*100% >= 止损阈值
            calculation_result = (abs_profit_loss / trade_amount) * 100
            if calculation_result >= loss_value:
                loss_triggered = True
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，(预计交易员损益绝对值/交易金额)*100% = {calculation_result:.2f}% >= 止损阈值{loss_value}%"
            else:
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，(预计交易员损益绝对值/交易金额)*100% = {calculation_result:.2f}% < 止损阈值{loss_value}%"
        elif loss_type == 'fixed_amount':
            # 固定金额止损：损益绝对值 >= 止损阈值
            if abs_profit_loss >= loss_value:
                loss_triggered = True
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，预计交易员损益绝对值({abs_profit_loss}) >= 止损阈值{loss_value}"
            else:
                loss_reason = f"预计交易员损益为负数({trader_profit_loss})，预计交易员损益绝对值({abs_profit_loss}) < 止损阈值{loss_value}"
    else:
        loss_reason = f"预计交易员损益({trader_profit_loss})不为负数，不触发止损"
    
    # 格式化阈值显示
    def format_threshold(threshold_type, threshold_value):
        """
        根据阈值类型格式化显示
        
        :param threshold_type: 阈值类型
        :param threshold_value: 阈值数值
        :return: 格式化后的阈值字符串
        """
        if threshold_type == 'percentage':
            return f"{threshold_value}%"
        elif threshold_type == 'fixed_rate':
            return f"{threshold_value}汇率"
        elif threshold_type == 'fixed_amount':
            return f"{threshold_value}金额"
        else:
            return f"{threshold_value}"
    
    # 打印日志
    logging.info(f"交易员损益: {trader_profit_loss}, 损益币种: {profit_loss_currency}, 交易金额: {trade_amount}")
    logging.info(f"交易方向: {direction}, 货币对: {currency_pair}, 渠道汇率: {channel_rate}")
    logging.info(f"止盈配置: 类型={profit_type}, 阈值={format_threshold(profit_type, profit_value)}")
    logging.info(f"止损配置: 类型={loss_type}, 阈值={format_threshold(loss_type, loss_value)}")
    logging.info(f"📊止盈判断: {profit_reason}")
    logging.info(f"📉止损判断: {loss_reason}")
    logging.info(f"🚀止盈: {'触发' if profit_triggered else '不触发'}, 🚀止损: {'触发' if loss_triggered else '不触发'}")
    
    # 打印结果
    print(f"结果：止盈={'触发' if profit_triggered else '不触发'}, 止损={'触发' if loss_triggered else '不触发'}\n")
    
    return profit_triggered, loss_triggered

class ProfitLossConfigManager:
    """
    止盈止损配置管理器，用于查询和管理止盈止损配置
    """
    def __init__(self, env='FAT'):
        """
        初始化数据库连接
        
        :param env: 环境变量，默认FAT
        """
        # 获取数据库配置
        self.db_config = get_db_config(env)
        # 切换到止盈止损配置数据库
        self.db_config['database'] = 'BAOFU_CBCA'
        self.conn = None
        self.cursor = None
        self.connect_db()
    
    def connect_db(self):
        """
        建立数据库连接
        """
        self.conn = pymysql.connect(**self.db_config)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        print(f"成功连接到数据库：{self.db_config['host']}:{self.db_config['port']} - {self.db_config['database']}")
    
    def close_db(self):
        """
        关闭数据库连接
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def query_loss_profit_setting(self, currency_pair, monitor_period=None):
        """
        查询止盈止损配置
        
        :param currency_pair: 货币对
        :param monitor_period: 监控时段：工作日-WORKDAY，节假日-HOLIDAY，默认不限制
        :return: 止盈止损配置列表
        """
        print(f"\n===== 查询止盈止损配置 =====")
        print(f"查询条件：货币对={currency_pair}，监控时段={monitor_period if monitor_period else '不限制'}")
        
        # 构建SQL查询条件
        where_clauses = ["IS_DELETE = 'N'", "CURRENCY_PAIR = %s"]
        params = [currency_pair]
        
        if monitor_period:
            where_clauses.append("MONITOR_PERIOD = %s")
            params.append(monitor_period)
        
        # 数据库查询SQL
        sql = f"""
        SELECT 
            ID, CURRENCY_PAIR, MONITOR_PERIOD, CLOSING_TYPE,
            STOP_LOSS_STRATEGY, STOP_LOSS_TYPE, STOP_LOSS_VALUE, STOP_LOSS_CHANNEL, STOP_LOSS_CLOSING,
            STOP_PROFIT_STRATEGY, STOP_PROFIT_TYPE, STOP_PROFIT_VALUE, STOP_PROFIT_CHANNEL, STOP_PROFIT_CLOSING,
            CREATE_AT, UPDATE_AT
        FROM 
            T_STOP_PROFIT_LOSS_CONFIG
        WHERE 
            {' AND '.join(where_clauses)}
        ORDER BY 
            CREATE_AT DESC;
        """
        
        # 执行查询
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        print(f"查询结果：共找到 {len(results)} 条有效配置")
        
        # 转换配置格式，适配check_profit_loss_threshold方法
        configs = []
        for idx, result in enumerate(results, 1):
            print(f"\n{idx}. 配置详情：")
            print(f"   货币对：{result['CURRENCY_PAIR']}")
            print(f"   监控时段：{result['MONITOR_PERIOD']}")
            print(f"   交割期限：{result['CLOSING_TYPE']}")
            
            # 止损配置
            print(f"   止损配置：")
            print(f"     策略：{result['STOP_LOSS_STRATEGY']}")
            print(f"     类型：{result['STOP_LOSS_TYPE']}")
            print(f"     阈值：{result['STOP_LOSS_VALUE']}")
            print(f"     监控渠道：{result['STOP_LOSS_CHANNEL']}")
            print(f"     交割期限：{result['STOP_LOSS_CLOSING']}")
            
            # 止盈配置
            print(f"   止盈配置：")
            print(f"     策略：{result['STOP_PROFIT_STRATEGY']}")
            print(f"     类型：{result['STOP_PROFIT_TYPE']}")
            print(f"     阈值：{result['STOP_PROFIT_VALUE']}")
            print(f"     监控渠道：{result['STOP_PROFIT_CHANNEL']}")
            print(f"     交割期限：{result['STOP_PROFIT_CLOSING']}")
            
            # 转换类型映射
            type_mapping = {
                'PCT': 'percentage',
                'AMT': 'fixed_amount',
                'RATE': 'fixed_rate'
            }
            
            # 处理None值，确保类型转换安全
            def safe_float(value):
                """安全转换为float，处理None值"""
                if value is None:
                    return 0.0
                return float(value)
            
            # 转换类型映射
            def get_type_mapping(value):
                """获取类型映射，处理None值"""
                if value is None:
                    return None
                return type_mapping.get(value, value)
            
            # 构建适配check_profit_loss_threshold方法的配置
            config = {
                'currency_pair': result['CURRENCY_PAIR'],
                'monitor_period': result['MONITOR_PERIOD'],
                'closing_type': result['CLOSING_TYPE'],
                'profit_type': get_type_mapping(result['STOP_PROFIT_TYPE']),
                'profit_value': safe_float(result['STOP_PROFIT_VALUE']),
                'loss_type': get_type_mapping(result['STOP_LOSS_TYPE']),
                'loss_value': safe_float(result['STOP_LOSS_VALUE']),
                'stop_profit_strategy': result['STOP_PROFIT_STRATEGY'],
                'stop_profit_channel': result['STOP_PROFIT_CHANNEL'],
                'stop_profit_closing': result['STOP_PROFIT_CLOSING'],
                'stop_loss_strategy': result['STOP_LOSS_STRATEGY'],
                'stop_loss_channel': result['STOP_LOSS_CHANNEL'],
                'stop_loss_closing': result['STOP_LOSS_CLOSING']
            }
            
            configs.append(config)
        
        return configs

# 示例使用
if __name__ == "__main__":
    # 函数参数说明：
    # check_profit_loss_threshold(
    #     trader_profit_loss,    # 预计交易员损益
    #     profit_loss_currency,  # 损益币种
    #     trade_amount,          # 交易金额
    #     profit_type,           # 止盈类型：'percentage'/'fixed_amount'/'fixed_rate'
    #     profit_value,          # 止盈阈值
    #     loss_type,             # 止损类型：'percentage'/'fixed_amount'/'fixed_rate'
    #     loss_value,            # 止损阈值
    #     direction=None,        # 交易方向：'buy'/'sell'（固定汇率时必填）
    #     currency_pair=None,    # 货币对：如 'USD/CNH'（固定汇率时必填）
    #     channel_rate=None      # 渠道汇率（固定汇率时必填）
    # )
    
    # 示例1：百分比止盈（触发），百分比止损（不触发）- 收益为正
    # print("=== 示例1：百分比止盈（触发），百分比止损（不触发）- 收益为正 ===")
    # check_profit_loss_threshold(
    #     trader_profit_loss=1500,        # 交易员收益1500
    #     profit_loss_currency="USD",     # 损益币种USD
    #     trade_amount=10000,              # 交易金额10000
    #     profit_type="percentage",       # 止盈类型：百分比
    #     profit_value=10,                 # 止盈阈值：10%
    #     loss_type="percentage",         # 止损类型：百分比
    #     loss_value=5                     # 止损阈值：5%
    # )
    
    # # 示例6：查询止盈止损配置并使用配置调用check_profit_loss_threshold
    # print("\n" + "="*80)
    # print("示例6：查询止盈止损配置并使用配置调用check_profit_loss_threshold")
    # print("="*80)
    
    # 创建配置管理器实例
    config_manager = ProfitLossConfigManager(env='FAT')
    
    # 查询USD/CNH货币对的止盈止损配置
    currency_pair = "USD/CNH"
    monitor_period = "HOLIDAY"   # HOLIDAY  WORKDAY
    
    # 查询配置
    configs = config_manager.query_loss_profit_setting(currency_pair, monitor_period)
    
    # 如果有配置，使用第一个配置调用check_profit_loss_threshold
    if configs:
        config = configs[0]
        print(f"\n使用查询到的配置调用check_profit_loss_threshold：")
        print(f"配置信息：货币对={config['currency_pair']}, 止盈类型={config['profit_type']}, 止盈阈值={config['profit_value']}, 止损类型={config['loss_type']}, 止损阈值={config['loss_value']}")
        
        # 调用止盈止损判断方法
        check_profit_loss_threshold(
            trader_profit_loss=-242.71,          # 交易员收益1000
            profit_loss_currency="CNH",     # 损益币种USD
            trade_amount=93.86,              # 交易金额10000(与损益币种一致买入or卖出金额)
            profit_type=config['profit_type'],       # 止盈类型
            profit_value=config['profit_value'],     # 止盈阈值
            loss_type=config['loss_type'],          # 止损类型
            loss_value=config['loss_value'],        # 止损阈值
            direction="buy",                    # 交易方向：买入  这个需要取头寸的
            currency_pair=config['currency_pair'],  # 货币对
            channel_rate=7.15                   # 渠道汇率：7.15
        )
    
    # 关闭数据库连接
    config_manager.close_db()

    