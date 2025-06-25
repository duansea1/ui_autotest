# 2025-3-11 14:45

import pymysql
import logging
from typing import Optional, Dict, List


class ChannelQueryService:
    def __init__(self, env: str = 'uat'):
        self.logger  = logging.getLogger(__name__)
        self.env  = env.upper()   # 统一转为大写
        self._init_db_connection()



    def _get_db_config(self) -> dict:
        """多环境数据库配置中心"""
        configs = {
            'FAT': {
                'host': '10.0.19.206',
                'port': 3306,
                'user': 'GEPHOLDING',
                'password': 'GEPHOLDING',
                'database': 'BAOFU_CBCA',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            },
            'UAT': {
                'host': '10.0.23.200',  #
                'port': 3306,
                'user': 'BAOFOO_CBPAY',
                'password': 'BAOFOO_CBPAY',
                'database': 'BAOFU_CBCA',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
        }
        return configs.get(self.env,  configs['UAT'])

    def _init_db_connection(self):
        """动态初始化数据库连接"""
        try:
            db_config = self._get_db_config()
            self.conn  = pymysql.connect(**db_config)
            self.logger.info(f" 成功连接 {self.env}  环境数据库")
        except Exception as e:
            self.logger.error(f" 数据库连接失败: {str(e)}")
            raise

    def _validate_parameters(self, user_no: str, biz_type: int, closing_type: str):
        """参数校验防御层"""
        if not user_no or len(user_no) > 22:
            raise ValueError("用户号格式异常")
        if biz_type not in (0, 7, 8, 9):  # 根据业务实际值调整
            raise ValueError("非法的业务类型")
        if closing_type not in {'TOD', 'TOM', 'SPOT', 'FORWARD', '0'}:
            raise ValueError("非法的交割类型")

    def _get_agent_chain(self, user_no: str) -> List[str]:
        """构建查询链路：用户->代理->全局"""
        agent_sql = """SELECT AGENT_NO FROM T_AGENT_USER_RELATION WHERE USER_NO = %s"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(agent_sql, (user_no,))
                if agent := cursor.fetchone():
                    self.logger.info(f" 代理链路构建: 用户-{user_no}->代理商-{agent['AGENT_NO']}->GLOBAL")
                    return [user_no, agent['AGENT_NO'], '0']
                self.logger.info(f" 独立用户链路: {user_no}->GLOBAL")
                return [user_no, '0']
        except Exception as e:
            self.logger.error(f" 代理查询失败: {str(e)}", exc_info=True)
            return [user_no, '0']

    def _fetch_configurations(self, targets: List[str], biz_type: int,
                              ccy_pair: str, closing_type: str) -> List[dict]:
        """批量获取配置数据（包含ID字段）"""
        config_sql = """
            SELECT 
                ID, USER_NO, BIZ_TYPE, CLOSING_TYPE,
                CCY_PAIR, BID_CHANNEL_ID, ASK_CHANNEL_ID, QUOTE_MODE 
            FROM T_USER_CHANNEL_CONFIG 
            WHERE USER_NO IN %s 
                AND BIZ_TYPE  IN (%s, '0')
                AND STATUS = '1'
                AND CLOSING_TYPE IN (%s, '0')
                AND (CCY_PAIR = %s OR CCY_PAIR = '0')
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(config_sql, (targets, biz_type, closing_type, ccy_pair))
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f" 配置查询异常: {str(e)}", exc_info=True)
            return []

    def _calculate_match_score(self, record: dict, closing_type: str, ccy_pair: str) -> tuple:
        """计算匹配度评分元组（用于排序）"""
        level_score = {2: 1, 1: 2, 0: 3}.get(record['QUOTE_MODE'], 99)
        closing_score = 1 if record['CLOSING_TYPE'] == closing_type else \
            (2 if record['CLOSING_TYPE'] == '0' else 3)
        ccy_score = 1 if record['CCY_PAIR'] == ccy_pair else 2
        print(f"计算匹配度评分元组（用于排序）::{(level_score, closing_score, ccy_score)}")
        return (level_score, closing_score, ccy_score)

    def query_channel_config(self, user_no: str, biz_type: int,
                             ccy_pair: str, closing_type: str) -> Optional[Dict]:
        """新版查询入口"""
        self._validate_parameters(user_no, biz_type, closing_type)
        self.logger.info(f" 【查询启动】用户:{user_no} 业务类型:{biz_type} 货币对:{ccy_pair} 交割类型:{closing_type}")

        try:
            # 构建查询链路
            query_targets = self._get_agent_chain(user_no)

            # 批量获取配置
            configs = self._fetch_configurations(query_targets, biz_type, ccy_pair, closing_type)
            if not configs:
                self.logger.warning(" 【空结果】未找到有效配置")
                return None

                # 优先级排序
            sorted_configs = sorted(
                configs,
                key=lambda x: self._calculate_match_score(x, closing_type, ccy_pair)
            )

            # 获取最佳匹配
            best_match = sorted_configs[0]
            self._log_success_match(best_match)

            return self._build_result(best_match)
        except Exception as e:
            self.logger.error(f" 查询流程异常: {str(e)}", exc_info=True)
            return None

    def _log_success_match(self, record: dict):
        """结构化日志记录"""
        log_data = {
            "配置ID": record['ID'],
            "用户层级": ['用户','代理商','全局',  ][record['QUOTE_MODE']],
            "业务类型": record['BIZ_TYPE'],
            "实际交割类型": record['CLOSING_TYPE'],
            "货币对匹配": '精准' if record['CCY_PAIR'] != '0' else '全局',
            "买入渠道": record['BID_CHANNEL_ID'],
            "卖出渠道": record['ASK_CHANNEL_ID']
        }
        self.logger.info(f" 【命中配置】{log_data}")

    def _build_result(self, record: dict) -> Dict:
        """构建标准化返回结果"""
        return {
            'ID': record['ID'],
            'USER_NO': record['USER_NO'],
            'BIZ_TYPE': record['BIZ_TYPE'],
            'CLOSING_TYPE': record['CLOSING_TYPE'],
            'CCY_PAIR': record['CCY_PAIR'],
            'BID_CHANNEL_ID': record['BID_CHANNEL_ID'],
            'ASK_CHANNEL_ID': record['ASK_CHANNEL_ID'],
        }


# 使用示例
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    service = ChannelQueryService((env:='fat'))

    # 5181240829000137108-丝丝 5181240702000026848-桐乡
    result = service.query_channel_config(
        user_no='5181240821000008798',
        biz_type=7,
        ccy_pair='USD/CNH',
        closing_type='FORWARD'
    )
    print("最终结果:", result)

# TODO： 1、将获取的渠道ID映射到具体的渠道名称
# TODO： 2、获取对应渠道的汇率 最近2条汇率
# TODO： 3、配置渠道如果没有汇率，获取默认渠道id的汇率。若默认渠道没有汇率，则返回无汇率
# TODO： 4、获取交易员的浮动--->销售的浮动----》代理商的浮动