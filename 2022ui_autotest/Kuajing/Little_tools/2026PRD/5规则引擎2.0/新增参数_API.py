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


# ==================== 公共配置 ====================
BASE_URL = "https://fat-global-ad.baofu.com"
CREATE_PARAM_API = f"{BASE_URL}/ams-api/front/param/api/create"


# ==================== 新增参数API ====================
def create_param(param_code, param_name, param_desc, reference_value,
                 param_source="manual", status="normal", param_type="in",
                 data_type="java.lang.Number"):
    """
    调用决策引擎2.0新增参数API

    参数说明:
        param_code: 参数编码 (如: USD_SEA_1)
        param_name: 参数名称 (如: USD_SEA_1)
        param_desc: 参数描述 (如: 1)
        reference_value: 参考值 (如: 1)
        param_source: 参数来源，默认 manual
        status: 状态，默认 normal
        param_type: 参数类型，默认 in
        data_type: 数据类型，默认 java.lang.Number

    返回:
        requests.Response 对象
    """
    url = CREATE_PARAM_API

    payload = {
        "paramSource": param_source,
        "status": status,
        "paramType": param_type,
        "paramCode": param_code,
        "paramName": param_name,
        "paramDesc": param_desc,
        "referenceValue": reference_value,
        "dataType": data_type
    }

    headers = {
        "Host": "fat-global-ad.baofu.com",
        "sec-ch-ua-platform": '"macOS"',
        "request-proxy-url": "",
        "request-system-name": "baofu-admin-control-client-base",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:135.0) Gecko/20000101 Firefox/135.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": f"{BASE_URL}",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"{BASE_URL}/payful/new/account/ams/main/global-rule-engine/parameter-config",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "tokenControl=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NzkyNTgxNjN9.vgewaDRMDLYgRP_d33IkMUwiNvByhS2QsxBuOgsDc3UJQuBrE7oOHnd2VpDCvp-zDZWpeOVG-fR59FQSClCuIg; Hm_lvt_97352b16ed2df8c3860cf5a1a65fb4dd=1779435316; HMACCOUNT=0A363431F909DC5B; agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3ODA4ODIyNDZ9.YR8T34sSdA5_tWVSpemR9Ezys17J2nAZACz3Fsc4ujaSrjpi5ww9-uxZcTiS90VoZtKafePKL4AtYpF3h00lvw; Hm_lpvt_97352b16ed2df8c3860cf5a1a65fb4dd=1780925818"
    }

    r = requests.post(url, json=payload, headers=headers, verify=False)
    return r


def parse_create_response(r):
    """解析新增参数API响应"""
    print("📋 API响应")
    print(f"状态码: {r.status_code}")

    if r.status_code == 200:
        try:
            resp = r.json()
            print("🔍 响应内容（格式化）")
            print(json.dumps(resp, indent=2, ensure_ascii=False))

            code = resp.get("code", "")
            msg = resp.get("msg", "")

            if code == "000000":
                print(f"{C_GREEN}✅ 新增参数成功{C_RESET}")
            else:
                print(f"{C_RED}❌ 新增参数失败: {msg}{C_RESET}")

            return resp
        except json.JSONDecodeError as e:
            print(f"{C_RED}JSON解析失败: {e}{C_RESET}")
            return None
    else:
        print(f"{C_RED}请求失败，状态码: {r.status_code}{C_RESET}")
        return None


# ==================== 批量新增参数 ====================
def batch_create_params(start_num=1, end_num=60, prefix="USD_SEA"):
    """
    批量新增参数

    参数说明:
        start_num: 起始编号，默认1
        end_num: 结束编号，默认60
        prefix: 参数前缀，默认 USD_SEA

    返回:
        成功数量, 失败数量
    """
    success_count = 0
    fail_count = 0

    print(f"\n� 开始批量新增参数 {prefix}_{start_num} ~ {prefix}_{end_num}")
    print("=" * 60)

    for i in range(start_num, end_num + 1):
        param_code = f"{prefix}_{i}"
        param_name = f"{prefix}_{i}"
        param_desc = str(i)
        reference_value = str(i)

        print(f"\n[{i}/{end_num}] 正在创建 {param_code}...")

        r = create_param(
            param_code=param_code,
            param_name=param_name,
            param_desc=param_desc,
            reference_value=reference_value
        )

        if r.status_code == 200:
            try:
                resp = r.json()
                code = resp.get("code", "")
                msg = resp.get("msg", "")

                if code == "000000":
                    print(f"{C_GREEN}✅ {param_code} 创建成功{C_RESET}")
                    success_count += 1
                else:
                    print(f"{C_RED}❌ {param_code} 创建失败: {msg}{C_RESET}")
                    fail_count += 1
            except:
                print(f"{C_RED}❌ {param_code} 响应解析失败{C_RESET}")
                fail_count += 1
        else:
            print(f"{C_RED}❌ {param_code} 请求失败，状态码: {r.status_code}{C_RESET}")
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"📊 批量新增完成: 成功 {success_count} 个, 失败 {fail_count} 个")
    print("=" * 60)

    return success_count, fail_count


# ==================== 示例测试 ====================
if __name__ == "__main__":

    print("=" * 60)
    print("🔧 决策引擎2.0 - 新增参数API测试")
    print("=" * 60)

    # ==================== 配置区（按需修改） ====================
    # 当前已有参数的最大编号
    current_max_num = 59
    # 本次新增数量
    add_count = 3
    # 参数前缀
    prefix = "USD_SEA"

    start_num = current_max_num + 1
    end_num = current_max_num + add_count
    # ==================== 配置区结束 ====================

    print(f"\n📊 配置信息")
    print(f"  当前最大编号: {prefix}_{current_max_num}")
    print(f"  本次新增数量: {add_count} 个")
    print(f"  将新增: {prefix}_{start_num} ~ {prefix}_{end_num}")
    print("-" * 60)

    batch_create_params(start_num=start_num, end_num=end_num, prefix=prefix)

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
