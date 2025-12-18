# 该文件用于处理回调通知，并将信息推送到企业微信群。
# 请根据实际情况修改相关配置。
# 配置如下
# WEIXIN_WEBHOOK_ENABLED: 是否启用企业微信群推送
# WEIXIN_WEBHOOK_URL: 企业微信群 webhook 地址
# 监听回调通知的信息


from flask import Flask, request
import logging
from datetime import datetime
import os
import json
import requests

# 数据库相关
import pymysql
from pymysql.cursors import DictCursor

from Kuajing.Common.kjMysql import get_db_config  # 你的数据库配置

app = Flask(__name__)
app.config['DEBUG'] = False

# 创建日志目录
os.makedirs("logs", exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/webhook.log", encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========================
# 🔧 配置区
# ========================
WEIXIN_WEBHOOK_ENABLED = True
WEIXIN_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e9694ba4-7833-433f-b470-32129bb4567b"

CLOSING_STATUS_MAP = {0: "待交割", 1: "交割处理中", 2: "交割完成", 3: "交割失败", 4: "已违约", 5: "部分交割成功", 6: "已取消"}
ORDER_STATE_MAP = {0: "待确认", 1: "已确认", 2: "已取消", 3: "已过期"}

TRADE_MODEL_MAP = {
    1: "实时兑换",
    2: "预约兑换",
    3: "挂单换汇"
}
env = "UAT"   # 环境变量，可根据需要改为 UAT 或 FAT
user_key_info="uat-sea-agent-hzl-yi"

def send_to_wechat_group(content: str):
    """发送消息到企业微信群"""
    if not WEIXIN_WEBHOOK_ENABLED:
        return

    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {
            "content": content.strip(),
            "mentioned_list": []
        }
    }

    try:
        resp = requests.post(
            WEIXIN_WEBHOOK_URL,
            data=json.dumps(payload),
            headers=headers,
            timeout=5
        )
        result = resp.json()
        if result.get("errcode") == 0:
            logger.info("✅ 企业微信消息发送成功")
        else:
            logger.error(f"❌ 企业微信发送失败: {result.get('errmsg', 'unknown')}")
    except Exception as e:
        logger.error(f"❌ 发送企业微信消息异常: {str(e)}")


def get_trade_model(exchange_id: str) -> str:
    """
    查询交割模式 TRADE_MODEL
    :param exchange_id: 汇兑单号
    :return: 格式化字符串，如 "实时兑换(1)" 或 "未获取到"
    """
    if not exchange_id:
        return "未获取到"

    connection = None
    try:
        # 使用你的 get_db_config，假设环境是 FAT

        config = get_db_config(env)  # 可根据需要改为 UAT 或通过环境变量控制

        connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            cursorclass=DictCursor,
            autocommit=True,
            connect_timeout=5,
            read_timeout=5,
            write_timeout=5
        )

        with connection.cursor() as cursor:
            sql = "SELECT TRADE_MODEL FROM `BAOFU_CBCA`.`T_EXCHANGE_ORDER_APPLY` WHERE `EXCHANGE_ID` = %s"
            cursor.execute(sql, (exchange_id,))
            result = cursor.fetchone()

            if result and result.get('TRADE_MODEL') is not None:
                model_val = int(result['TRADE_MODEL'])
                model_name = TRADE_MODEL_MAP.get(model_val, "未知模式")
                return f"{model_name}({model_val})"
            else:
                return "未获取到"

    except Exception as e:
        logger.warning(f"⚠️ 查询 TRADE_MODEL 失败: {str(e)}")
        return "未获取到"
    finally:
        if connection:
            connection.close()


@app.route('/notify/sea', methods=['POST'])
def notify_sea():
    try:
        # 1. 获取原始请求
        raw_bytes = request.get_data()
        if not raw_bytes:
            return "OK", 200, {'Content-Type': 'text/plain; charset=utf-8'}

        try:
            raw_body = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raw_body = raw_bytes.decode('latin1', errors='replace')

        logger.info(f"📥 原始请求: {raw_body[:200]}...")

        # 2. 解析外层数据
        outer_data = request.get_json(silent=True) or request.form.to_dict() or {}
        encrypted_data = outer_data.get('dataContent', '').strip()

        if not encrypted_data:
            logger.warning("⚠️ dataContent 为空")
            return "OK", 200, {'Content-Type': 'text/plain; charset=utf-8'}

        # 3. RSA 解密
        try:
            from Common import publicTools as p
            rsa_utils = p.rsa_generate_tool(user_key_info)
            decrypted_raw = rsa_utils.pub_decrypt(encrypted_data)
            data = json.loads(decrypted_raw) if decrypted_raw.strip().startswith('{') else {"raw": decrypted_raw}
        except Exception as e:
            logger.error(f"❌ 解密失败: {str(e)}")
            return "OK", 200, {'Content-Type': 'text/plain; charset=utf-8'}

        # 4. 提取字段
        exchange_id = str(data.get("exchangeId", ""))  # 转为字符串，避免类型问题
        user_no = data.get("userNo", "")
        user_req_no = data.get("userReqNo", "")
        buy_ccy = data.get("buyCcy", "")
        sell_ccy = data.get("sellCcy", "")
        buy_amount = data.get("buyAmount", 0)
        sell_amount = data.get("sellAmount", 0)
        closing_date = data.get("closingDate", "")
        closing_status = data.get("closingStatus", 0)
        order_state = data.get("orderState", 0)
        trade_rate = data.get("tradeRate", 0)
        closing_success_date = data.get("closingSuccessDate", None)

        # 转换时间戳
        success_time_str = (
            datetime.fromtimestamp(closing_success_date / 1000).strftime('%Y-%m-%d %H:%M:%S')
            if closing_success_date else "—"
        )

        trade_model_display = get_trade_model(exchange_id)

        # 5. 构造中文日志 & 企微消息
        message = f"""
✅【{env}-汇兑回调通知】✅
────────────────────────
单号：{exchange_id}
用户号：{user_no}
商户订单号：{user_req_no}
交易方向：{'买入' if data.get('direction') == 1 else '卖出'}
金额：{sell_amount}{sell_ccy} → {buy_amount}{buy_ccy}
汇率：{trade_rate:.6f}
交割日期：{closing_date}
交割状态：【{CLOSING_STATUS_MAP.get(closing_status, '未知')}】
订单状态：【{ORDER_STATE_MAP.get(order_state, '未知')}】
交割模式：{trade_model_display}
交割成功时间：{success_time_str}
────────────────────────
"""

        # 打印日志
        logger.info(message.strip())

        # 发送到企业微信群（根据开关）
        if WEIXIN_WEBHOOK_ENABLED:
            send_to_wechat_group(message)

        return "OK", 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        logger.error(f"【严重】处理回调异常: {str(e)}", exc_info=True)
        return "OK", 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/health', methods=['GET'])
def health():
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)