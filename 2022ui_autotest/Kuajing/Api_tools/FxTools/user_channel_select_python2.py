# -*- coding: utf-8 -*-
import pymysql
import logging
from functools import cmp_to_key


class ChannelServiceV2(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._init_db()

    def _init_db(self):
        """初始化MySQL连接（Python2需显式声明编码）"""
        self.conn = pymysql.connect(
            host='10.0.23.200',
            port=3306,
            user='BAOFOO_CBPAY',
            passwd='BAOFOO_CBPAY',
            db='BAOFU_CBCA',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def _get_agent_chain(self, user_no):
        """构建代理链路（Python2兼容写法）"""
        sql = "SELECT AGENT_NO FROM T_AGENT_USER_RELATION WHERE USER_NO = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (user_no,))
                result = cursor.fetchone()
                if result:
                    agent = result['AGENT_NO']
                    self.logger.debug("Agent  chain: %s -> %s -> 0", user_no, agent)
                    return [user_no, agent, '0']
                return [user_no, '0']
        except Exception as e:
            self.logger.error("Agent  query failed: %s", str(e), exc_info=True)
            return [user_no, '0']

    def _fetch_configs(self, targets, biz_type, ccy_pair, closing_type):
        """查询配置（Python2的in查询需处理元组）"""
        sql = """
            SELECT ID, USER_NO, BIZ_TYPE, CLOSING_TYPE, CCY_PAIR,
                   BID_CHANNEL_ID, ASK_CHANNEL_ID, QUOTE_MODE 
            FROM T_USER_CHANNEL_CONFIG 
            WHERE USER_NO IN ({0})
                AND BIZ_TYPE = %s 
                AND STATUS = '1'
                AND CLOSING_TYPE IN (%s, '0')
                AND (CCY_PAIR = %s OR CCY_PAIR = '0')
        """.format(','.join(['%s'] * len(targets)))

        try:
            with self.conn.cursor() as cursor:
                params = list(targets) + [biz_type, closing_type, ccy_pair]
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            self.logger.error("Config  query error: %s", str(e), exc_info=True)
            return []

    def _compare_priority(self, a, b):
        """自定义排序（Python2使用cmp函数）"""

        def _calc_score(record):
            level = {2: 1, 1: 2, 0: 3}.get(record['QUOTE_MODE'], 99)
            closing = 1 if record['CLOSING_TYPE'] == self.target_closing else \
                (2 if record['CLOSING_TYPE'] == '0' else 3)
            ccy = 1 if record['CCY_PAIR'] == self.target_ccy else 2
            return (level, closing, ccy)

        a_score = _calc_score(a)
        b_score = _calc_score(b)
        return cmp(a_score, b_score)

    def query_channels(self, user_no, biz_type, ccy_pair, closing_type):
        """主查询方法（Python2参数需显式声明）"""
        self.logger.info(
            u"[Query] user_no:%s biz_type:%s ccy:%s closing:%s",
            user_no, biz_type, ccy_pair, closing_type
        )

        # 参数校验 
        if not isinstance(user_no, (str, unicode)) or len(user_no) > 20:
            raise ValueError("Invalid user_no")
        if closing_type not in ('TOD', 'TOM', 'SPOT', '0'):
            raise ValueError("Unsupported closing type")

        # 动态参数传递 
        self.target_closing = closing_type
        self.target_ccy = ccy_pair

        # 获取配置 
        targets = self._get_agent_chain(user_no)
        configs = self._fetch_configs(targets, biz_type, ccy_pair, closing_type)
        if not configs:
            self.logger.warning(u"No  configs found")
            return None

            # 排序并选择最优
        sorted_configs = sorted(configs, key=cmp_to_key(self._compare_priority))
        best = sorted_configs[0]

        # 构建返回结果 
        return {
            'ID': best['ID'],
            'USER_NO': best['USER_NO'],
            'BIZ_TYPE': best['BIZ_TYPE'],
            'CLOSING_TYPE': best['CLOSING_TYPE'],
            'CCY_PAIR': best['CCY_PAIR'],
            'BID_CHANNEL_ID': best['BID_CHANNEL_ID'],
            'ASK_CHANNEL_ID': best['ASK_CHANNEL_ID']
        }


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    )

    service = ChannelServiceV2()
    result = service.query_channels(
        user_no='5181240829000137108',
        biz_type=7,
        ccy_pair='EUR/CNH',
        closing_type='TOD'
    )
    print("Result:", result )