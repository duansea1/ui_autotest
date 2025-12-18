from Kuajing.Common.kjMysql import get_db_config
import pymysql.cursors
import logging
from typing import List, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_user_recent_applied_platforms(user_no: int, env: str = 'FAT') -> List[Dict[str, Any]]:
    """
    获取用户最近申请的平台（最多6个），按以下规则：
      - T_USER_STORE.STORE_PLATFORM 关联 T_STORE_PLATFORM_CONFIG.PLATFORM_SUB_CODE
      - 获取对应的主平台 PLATFORM_CODE
      - 主平台和子站都必须处于 ENABLE 状态
      - 按用户申请时间倒序排序，去重取最多6个主平台

    :param user_no: 用户号
    :param env: 环境 ('FAT', 'UAT')
    :return: 包含平台code、名称、申请时间的结果列表
    """
    config = get_db_config(env)

    conn = pymysql.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        charset=config['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            # --- 日志增强：阶段1 - 所有已启用的主平台 ---
            cursor.execute("""
                SELECT PLATFORM_CODE, PLATFORM_NAME 
                FROM BAOFU_CBCA.T_PLATFORM_CONFIG 
                WHERE STATUS = 'ENABLE'
                ORDER BY PLATFORM_CODE
            """)
            all_enabled_platforms = cursor.fetchall()

            if all_enabled_platforms:
                logger.info("=" * 60)
                logger.info("✅ 系统中所有已启用的主平台：")
                for p in all_enabled_platforms:
                    logger.info(f"   主平台开启 → 平台ID: {p['PLATFORM_CODE']}, 平台名称: {p['PLATFORM_NAME']}")
                logger.info("=" * 60)
            else:
                logger.warning("⚠️  系统中没有任何已启用的主平台！")

            # --- 阶段2: 找出主平台开启但无任何启用子站的平台 ---
            enabled_main_codes = {p['PLATFORM_CODE']: p['PLATFORM_NAME'] for p in all_enabled_platforms}

            cursor.execute("""
                SELECT DISTINCT b.PLATFORM_CODE, c.PLATFORM_NAME, b.PLATFORM_SUB_CODE, b.PLATFORM_SUB_NAME
                FROM BAOFU_CBCA.T_STORE_PLATFORM_CONFIG b
                INNER JOIN BAOFU_CBCA.T_PLATFORM_CONFIG c ON b.PLATFORM_CODE = c.PLATFORM_CODE
                WHERE b.STATUS = 'ENABLE' AND c.STATUS = 'ENABLE'
            """)
            enabled_subsites = cursor.fetchall()

            # 提取所有拥有启用子站的主平台
            has_enabled_subsite_codes = set(row['PLATFORM_CODE'] for row in enabled_subsites)

            # 差集：主平台开启，但没有启用的子站
            no_subsite_enabled = {code: name for code, name in enabled_main_codes.items() if
                                  code not in has_enabled_subsite_codes}

            if no_subsite_enabled:
                logger.warning("=" * 60)
                logger.warning("⚠️  主平台已开启但无任何启用子站：")
                for code, name in no_subsite_enabled.items():
                    logger.warning(f"   ❌ 主平台开启但无启用站点 → 平台ID: {code}, 平台名称: {name}")
                logger.warning("=" * 60)
            else:
                logger.info("✅ 所有已启用主平台均有至少一个启用的子站。")

            # --- 阶段3: 打印主平台开启且有启用子站的平台 + 子站详情 ---
            if enabled_subsites:
                logger.info("=" * 60)
                logger.info("✅ 主平台开启且有启用子站的平台（用户可申请）：")

                # 按主平台分组
                from collections import defaultdict
                platform_sub_map = defaultdict(list)
                for row in enabled_subsites:
                    platform_sub_map[row['PLATFORM_CODE']].append(row)

                for main_code, subs in platform_sub_map.items():
                    main_name = subs[0]['PLATFORM_NAME']
                    logger.info(f"   🔹 主平台开启且有启用站点 → 平台ID: {main_code}, 平台名称: {main_name}")
                    for sub in subs:
                        logger.info(f"        ↳ 站点ID: {sub['PLATFORM_SUB_CODE']}, 站点名称: {sub['PLATFORM_SUB_NAME']}")
                logger.info("=" * 60)
            else:
                logger.error("❌ 当前系统中没有任何主平台与子站同时处于启用状态！")


            # --- 核心逻辑：获取用户最近申请的主平台（最多6个）---
            sql = """
                SELECT 
                    c.PLATFORM_CODE AS platform_code,
                    c.PLATFORM_NAME AS platform_name,
                    MAX(a.CREATE_AT) AS latest_create_at
                FROM BAOFU_CBCA.T_USER_STORE a
                INNER JOIN BAOFU_CBCA.T_STORE_PLATFORM_CONFIG b 
                    ON a.STORE_PLATFORM = b.PLATFORM_SUB_CODE
                INNER JOIN BAOFU_CBCA.T_PLATFORM_CONFIG c 
                    ON b.PLATFORM_CODE = c.PLATFORM_CODE
                WHERE 
                    a.USER_NO = %s
                    AND c.STATUS = 'ENABLE'
                    AND b.STATUS = 'ENABLE'
                GROUP BY 
                    c.PLATFORM_CODE, c.PLATFORM_NAME
                ORDER BY 
                    latest_create_at DESC
                LIMIT 6
            """

            cursor.execute(sql, (user_no,))
            rows = cursor.fetchall()

            if not rows:
                logger.info(f"用户号 {user_no} 没有符合条件的已启用平台记录。")
                return []

            result = []
            for row in rows:
                record = {
                    'user_no': user_no,
                    'platform_code': row['platform_code'],
                    'platform_name': row['platform_name'],
                    'create_at': row['latest_create_at'].strftime('%Y-%m-%d %H:%M:%S')
                }
                result.append(record)

                # 原始日志格式保持不变
                logger.info(
                    f"用户号: {user_no} | "
                    f"平台code: {record['platform_code']} | "
                    f"平台名称: {record['platform_name']} | "
                    f"店铺申请时间: {record['create_at']}"
                )

            return result

    except Exception as e:
        logger.error(f"查询用户 {user_no} 的平台信息时发生异常: {e}", exc_info=True)
        return []
    finally:
        conn.close()


# 测试入口
if __name__ == '__main__':
    # 将最近使用的平台名称改为其他平台：OZON-CNH    WB-CNH
    # user_no = 5181240821000008798
    user_no = 5181240628000024148
    # user_no = 5181240827000021548
    platforms = get_user_recent_applied_platforms(user_no=user_no, env='FAT')
    print("\n最终结果:")
    for p in platforms:
        print(p)