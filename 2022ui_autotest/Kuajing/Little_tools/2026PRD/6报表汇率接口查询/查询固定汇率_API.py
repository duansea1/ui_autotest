import requests
import json
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# 颜色定义
C_GREEN = Fore.GREEN
C_RED = Fore.RED
C_YELLOW = Fore.YELLOW
C_CYAN = Fore.CYAN
C_RESET = Style.RESET_ALL


# ==================== 公共配置（按需修改） ====================
# 服务地址列表
URLS = [
    "http://10.254.8.236:2014",
    "http://10.254.8.236:5005",
]

# API路径
API_PATH = "/rate-fixed-detail/queryFixedRate"


# ==================== 发送请求 ====================
def send_request(data, base_url):
    url = f"{base_url}{API_PATH}"
    headers = {"Content-Type": "application/json", "accept": "*/*"}
    r = requests.post(url, json=data, headers=headers)
    return r


# ==================== 响应解析 ====================
def parse_response(r, base_url):
    print(f"\n📋 原始响应 (来源: {base_url})")
    print(f"状态码: {r.status_code}")

    if r.status_code == 200:
        try:
            resp = r.json()
            print("🔍 原始响应（格式化）")
            print(json.dumps(resp, indent=2, ensure_ascii=False))

            # 解析关键字段 - 优先检查 success 字段
            print("\n📌 关键信息")
            is_success = resp.get("success", False)
            code = resp.get("code", resp.get("status", "未知"))
            msg = resp.get("msg", resp.get("message", resp.get("info", "")))

            # 判断成功：success=true 或 code 在成功列表中
            if is_success or code in ["000000", "200", "00", 0, "0", "success", "SUCCESS"]:
                print(f"  请求状态：{C_GREEN}成功{C_RESET}")
            else:
                print(f"  请求状态：{C_RED}失败{C_RESET}")

            print(f"  响应码：{code}")
            print(f"  响应信息：{msg}")

            # 解析数据 - 优先从 result 获取，其次从 data 获取
            result_data = resp.get("result", resp.get("data", {}))
            if result_data:
                print("\n📊 数据详情")
                for key, value in result_data.items():
                    print(f"  {key}：{value}")

        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            print(f"原始响应内容: {r.text}")
    else:
        print(f"请求失败，状态码: {r.status_code}")


# ==================== 测试数据（按需修改） ====================
if __name__ == "__main__":

    # 测试参数
    biz_data = {
        "originalCcy": "HKD",
        "targetCcy": "JPY",
        "rateQueryDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    print("=" * 60)
    print("📌 汇率查询 API")
    print("=" * 60)
    print(f"API路径: {API_PATH}")
    print(f"服务名: baofu-channel-center")
    print(f"\n📨 请求参数:")
    print(json.dumps(biz_data, indent=2, ensure_ascii=False))

    print("\n" + "-" * 60)
    print("开始执行...")

    # 遍历所有地址尝试调用
    for base_url in URLS:
        try:
            print(f"\n{'=' * 60}")
            print(f"🔄 尝试访问: {base_url}")
            print(f"{'=' * 60}")

            excue_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"执行时间: {excue_time}")

            r = send_request(biz_data, base_url)

            if r.status_code == 200:
                try:
                    resp = r.json()
                    # 如果返回成功则停止尝试 - 优先检查 success 字段
                    is_success = resp.get("success", False)
                    code = resp.get("code", resp.get("status", ""))
                    if is_success or code in ["000000", "200", "00", 0, "0", "success", "SUCCESS"]:
                        parse_response(r, base_url)
                        print(f"\n{C_GREEN}✅ 成功连接到: {base_url}{C_RESET}")
                        break
                    else:
                        parse_response(r, base_url)
                except:
                    parse_response(r, base_url)
            else:
                print(f"状态码: {r.status_code}")
                print(f"响应内容: {r.text[:500] if r.text else '无'}")

        except Exception as e:
            print(f"❌ 请求异常: {e}")
            continue

    print(f"\n{'=' * 60}")
    print(f"执行结束 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)