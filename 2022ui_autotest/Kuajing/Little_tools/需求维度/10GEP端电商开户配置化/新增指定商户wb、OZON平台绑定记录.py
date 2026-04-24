import pymysql
from pymysql.cursors import DictCursor
from Kuajing.Common.kjMysql import get_db_config
import uuid
import time
from datetime import datetime

def generate_unique_back_link_url():
    """生成唯一的 BACK_LINK_URL（仍为真实 URL）"""
    return f"https://example.com/callback/{uuid.uuid4().hex[:16]}"

def generate_record_no():
    """生成唯一的 RECORD_NO"""
    return int(f"25{int(time.time() * 1000000) % 100000000000000000}")

def generate_redirect_token():
    """生成 32 位小写十六进制字符串作为 REDIRECT_URL"""
    return uuid.uuid4().hex  # 如 '14449df14602c4e58a19d923e7065500'

def insert_bind_and_request_records_auto_plat(
    env: str,
    user_no: int,
    seller_id: str,
    seller_cert_no: str,
    country: str = "CHN",
    seller_name: str = None,
    entity_type: str = "Corporate",
    store_url: str = "",
    settle_currency: str = "CNH",
    plat_name: str = None,  # 自动推断
    remarks: str = "自动化新增sea",
    config_filter: str = "OZON-CNH"
):
    """
    自动从 T_CLIENT_SYSTEM_CONFIG 获取 PLAT_USER_NO 和 PLAT_REQ_NO 并插入记录
    CONFIG_NO = PLAT_USER_NO
    CONFIG_NO = PLAT_REQ_NO
    CONFIG_VAL = 'OZON-CNH' 等
    REDIRECT_URL = 32位hex字符串（非URL）
    """
    # 获取数据库配置
    config = get_db_config(env)
    connection = pymysql.connect(**config)

    try:
        with connection.cursor() as cursor:
            # Step 1: 查询 T_CLIENT_SYSTEM_CONFIG
            query_config_sql = """
            SELECT CONFIG_NO, CONFIG_VAL 
            FROM BAOFU_CBCA.T_CLIENT_SYSTEM_CONFIG 
            WHERE CONFIG_KEY = 'STORE_PLATFORM' 
              AND CONFIG_VAL LIKE %s 
            LIMIT 1
            """
            cursor.execute(query_config_sql, (f'%{config_filter}%',))
            config_row = cursor.fetchone()

            if not config_row:
                raise ValueError(f"未找到 CONFIG_KEY='STORE_PLATFORM' 且 CONFIG_VAL 包含 '{config_filter}' 的配置")

            plat_user_no = int(config_row['CONFIG_NO'])  # ✅ CONFIG_NO 就是 PLAT_USER_NO
            plat_req_no = config_row['CONFIG_NO']         # ✅ 通常 PLAT_REQ_NO 也用 CONFIG_NO
            config_val = config_row['CONFIG_VAL']

            # 自动设置 plat_name（如 OZON、WB）
            if plat_name is None:
                plat_name = config_val.split('-')[0].upper()  # 如 'OZON-CNH' -> 'OZON'

            print(f"🔍 匹配到配置: CONFIG_NO={plat_user_no}, CONFIG_VAL='{config_val}'")
            print(f"   将用于: PLAT_USER_NO={plat_user_no}, PLAT_REQ_NO={plat_req_no}, 平台={plat_name}")

            # Step 2: 检查 (SELLER_ID, PLAT_USER_NO) 是否已存在
            check_sql = """
            SELECT COUNT(*) AS cnt 
            FROM BAOFU_CBCA.T_USER_PLATFORM_RELATION_REQUEST 
            WHERE SELLER_ID = %s AND PLAT_USER_NO = %s
            """
            cursor.execute(check_sql, (seller_id, plat_user_no))
            result = cursor.fetchone()
            if result['cnt'] > 0:
                raise ValueError(f"SELLER_ID='{seller_id}' 与 PLAT_USER_NO='{plat_user_no}' 的组合已存在。")

            # Step 3: 生成 RECORD_NO 和时间
            record_no = generate_record_no()
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            system_user = "SYSTEM"

            # ✅ 重点修改：REDIRECT_URL 是 32 位 hex token
            redirect_url = generate_redirect_token()  # 如 '14449df14602c4e58a19d923e7065500'
            back_link_url = generate_unique_back_link_url()  # 回调通知地址，仍是 URL
            seller_name = seller_name or seller_id

            # Step 4: 插入 T_USER_PLATFORM_RELATION_BIND_RECORD
            insert_bind_sql = """
            INSERT INTO BAOFU_CBCA.T_USER_PLATFORM_RELATION_BIND_RECORD 
            (USER_NO, STATUS, RECORD_NO, REMARKS, CREATE_AT, CREATE_BY, UPDATE_AT, UPDATE_BY)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_bind_sql, (
                user_no, 1, record_no, remarks,
                create_time, system_user,
                create_time, system_user
            ))

            # Step 5: 插入 T_USER_PLATFORM_RELATION_REQUEST
            insert_request_sql = """
            INSERT INTO BAOFU_CBCA.T_USER_PLATFORM_RELATION_REQUEST 
            (RECORD_NO, PLAT_USER_NO, PLAT_NAME, PLAT_REQ_NO, SELLER_ID, SELLER_NAME, ENTITY_TYPE, 
             SELLER_CERT_NO, COUNTRY, STORE_URL, SETTLE_CURRENCY, REDIRECT_URL, BIND_STATUS, 
             RESULT_MSG, RESULT_MSG_CODE, BACK_LINK_URL, ADDITIONAL1, ADDITIONAL2, REMARKS, 
             CREATE_AT, CREATE_BY, UPDATE_AT, UPDATE_BY, BUSINESS_TYPE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_request_sql, (
                record_no, plat_user_no, plat_name, plat_req_no,
                seller_id, seller_name, entity_type,
                seller_cert_no, country, store_url, settle_currency,
                redirect_url,  # ✅ 使用 hex token
                0, None, None, back_link_url,
                None, None, None,
                create_time, system_user, create_time, system_user, 'Bind'
            ))

        # 提交事务
        connection.commit()

        # ✅ 成功日志
        print(f"✅ 成功新增 {config_filter} 绑定记录")
        print(f"   平台: {plat_name}")
        print(f"   平台用户号 (PLAT_USER_NO): {plat_user_no}")
        print(f"   记录编号 (RECORD_NO): {record_no}")
        print(f"   卖家ID: {seller_id}")
        print(f"   平台请求流水号 (PLAT_REQ_NO): {plat_req_no}")
        print(f"   🔁 REDIRECT_URL (回调token): {redirect_url}")      # 强调这是 token
        print(f"   📞 BACK_LINK_URL (通知地址): {back_link_url}")     # 区分 back_link_url

    except Exception as e:
        connection.rollback()
        print(f"❌ 插入失败: {str(e)}")
        raise
    finally:
        connection.close()



"""
工具脚本：更新 T_USER_PLATFORM_RELATION_REQUEST 表中的 SELLER_CERT_NO
"""
def update_seller_cert_no_simple(env, seller_id, plat_user_no, new_seller_cert_no):
    """
    简化版：更新指定卖家在平台的证件号
    :param env: 环境名，如 'FAT', 'UAT'
    :param seller_id: 卖家ID（SELLER_ID）
    :param plat_user_no: 平台用户号（PLAT_USER_NO）
    :param new_seller_cert_no: 要更新成的新证件号
    """
    conn = None
    try:
        # 获取数据库连接
        conn = pymysql.connect(**get_db_config(env))

        with conn.cursor() as cur:
            # 执行更新 这个表可以修改绑定状态
            cur.execute("""
                UPDATE BAOFU_CBCA.T_USER_PLATFORM_RELATION_REQUEST 
                SET SELLER_CERT_NO = %s, 
                    UPDATE_AT = NOW(), 
                    UPDATE_BY = 'SYSTEM'
                WHERE SELLER_ID = %s AND PLAT_USER_NO = %s
            """, (new_seller_cert_no, seller_id, plat_user_no))

            # 检查是否更新成功
            if cur.rowcount == 0:
                print(f"❌ 未找到匹配记录：SELLER_ID={seller_id}, PLAT_USER_NO={plat_user_no}")
            else:
                conn.commit()
                print(f"✅ 成功更新 SELLER_CERT_NO")
                print(f"   SELLER_ID: {seller_id}")
                print(f"   PLAT_USER_NO: {plat_user_no}")
                print(f"   新证件号: {new_seller_cert_no}")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ 更新失败: {str(e)}")
    finally:
        if conn:
            conn.close()


"""
工具脚本：更新 T_USER_PLATFORM_RELATION_REQUEST 表中的 BIND_STATUS
"""
def update_bind_status(
    env: str,
    redirect_url: str,
    bind_status: int,
    result_msg: str = None,
    result_msg_code: str = None
):
    """
    根据REDIRECT_URL更新绑定状态
    :param env: 环境名，如 'FAT', 'UAT'
    :param redirect_url: GEP的授权绑定回调地址（REDIRECT_URL字段值）
    :param bind_status: 绑定状态：-1 已删除 0-待绑定，1-绑定中，2-成功，3-失败
    :param result_msg: 结果信息，一般是失败原因（可选）
    :param result_msg_code: 消息CODE（可选）
    """
    conn = None
    try:
        # 验证绑定状态值
        valid_statuses = [-1, 0, 1, 2, 3]
        if bind_status not in valid_statuses:
            raise ValueError(f"无效的绑定状态值: {bind_status}，有效值为: {-1, 0, 1, 2, 3}")
            
        # 获取数据库连接
        conn = pymysql.connect(**get_db_config(env))

        with conn.cursor() as cur:
            # 执行更新
            cur.execute("""
                UPDATE BAOFU_CBCA.T_USER_PLATFORM_RELATION_REQUEST 
                SET BIND_STATUS = %s, 
                    RESULT_MSG = %s, 
                    RESULT_MSG_CODE = %s,
                    UPDATE_AT = NOW(), 
                    UPDATE_BY = 'SYSTEM'
                WHERE REDIRECT_URL = %s
            """, (bind_status, result_msg, result_msg_code, redirect_url))

            # 检查是否更新成功
            if cur.rowcount == 0:
                print(f"❌ 未找到匹配记录：REDIRECT_URL={redirect_url}")
            else:
                conn.commit()
                print(f"✅ 成功更新绑定状态")
                print(f"   REDIRECT_URL: {redirect_url}")
                print(f"   新绑定状态: {bind_status}")
                
                # 根据状态值显示对应的中文说明
                status_mapping = {
                    -1: "已删除",
                    0: "待绑定",
                    1: "绑定中",
                    2: "成功",
                    3: "失败"
                }
                if bind_status in status_mapping:
                    print(f"   状态说明: {status_mapping[bind_status]}")
                    
                # 显示结果消息（如果有）
                if result_msg:
                    print(f"   结果消息: {result_msg}")
                if result_msg_code:
                    print(f"   消息CODE: {result_msg_code}")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ 更新绑定状态失败: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()




# ========================
# 使用示例
# ========================
if __name__ == "__main__":
    # insert_bind_and_request_records_auto_plat(
    #     env='UAT',
    #     user_no=5181240702000026848,
    #     seller_id="SEA20250911AUTO",    #需要修改为唯一的，不然每次会变
    #     seller_cert_no="92330483MA2JGLRF7A",
    #     country="CHN",
    #     seller_name="自动测试sea-平台",
    #     store_url="https://ozon.ru/seller/auto",
    #     settle_currency="CNH",
    #     config_filter="WB-CNH"  # 可改为 "OZON-CNH"、  WB-CNH
    # )

    # # 示例参数，请根据实际情况修改
    # update_seller_cert_no_simple(
    #     env='UAT',  # 环境：FAT/UAT/PROD
    #     seller_id="SEA20250915AUTO",  # 卖家ID
    #     plat_user_no=5181221116000508878,  # 平台用户号（即 CONFIG_NO）
    #     new_seller_cert_no="92330483MA2JGLRF7A"  # 要更新成的新证件号
    # )

    # 新增ozon或wb的绑定记录
    insert_bind_and_request_records_auto_plat(
        env='FAT',
        user_no=5181240628000024148,    # 平台用户号5181240628000024148-桐乡
        seller_id="SEA20251112AUTO-6",  # 需要修改为唯一的，不然每次会变
        seller_cert_no="92330483MA2JGLRF7A",
        country="CHN",
        seller_name="autoTest-sea-ozon0001",
        store_url="https://ozon.ru/seller/auto",
        settle_currency="CNH",
        config_filter="OZON-CNH"  # 可改为 "OZON-CNH"、  WB-CNH
    )
    
    # 更新绑定状态示例
    # 请根据实际情况修改以下参数
    # update_bind_status(
    #     env='FAT',  # 环境：FAT/UAT/PROD
    #     redirect_url="f9cbcd9aaf8d482395b249b75b821fd5",  # 32位hex token
    #     bind_status=3,  # 2-成功，可选值：-1(已删除), 0(待绑定), 1(绑定中), 2(成功), 3(失败)
    #     result_msg="绑定成功",  # 可选：结果消息
    #     result_msg_code="SUCCESS0001"  # 可选：消息CODE
    # )
