import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

# 颜色定义
C_GREEN = Fore.GREEN
C_RED = Fore.RED
C_RESET = Style.RESET_ALL


# ==================== 公共配置 ====================
BASE_URL = "https://fat-global-ad.baofu.com"
ADD_RULE_API = f"{BASE_URL}/ams-api/front/rule/engine/api/add"


# ==================== 新增脚本规则API ====================
def create_script_rule(rule_number):
    """
    调用决策引擎2.0新增脚本规则API

    参数说明:
        rule_number: 规则编号尾号 (如: 26 表示 USD_SEA_26)

    返回:
        requests.Response 对象
    """
    url = ADD_RULE_API

    param_code = f"USD_SEA_{rule_number}"

    # Groovy脚本内容（动态替换参数）
    script_content = f'''import cn.hutool.core.convert.Convert
import java.math.*
import java.util.*
import com.gepholding.user.flow.service.rule.engine.context.RuleContext
import com.gepholding.user.flow.service.rule.engine.func.FunctionInvoker
import com.system.commons.exception.BizServiceException
import com.gepholding.user.flow.service.enums.ErrorCodeEnum

if (ruleContext == null) {{
    throw new BizServiceException(ErrorCodeEnum.DATA_NOT_EXIST, "未获取到上下文")
}}
ruleContext.setSuccess(false)
def functionInvoker = ruleContext.getFunctionInvoker()

// 核心逻辑：将 {param_code} 转为字符串并判断是否等于 {rule_number}（使用 BigDecimal 保证精确比对）
def amtStr = Convert.toStr(@{param_code}@)
def condition = (amtStr != null && new BigDecimal(amtStr).compareTo(new BigDecimal("{rule_number}")) == 0)

try {{
    if (condition) {{
        ruleContext.setStatus("SUCCESS")
        ruleContext.setErrorCode("000000")
        ruleContext.setSuccess(true)

        for (RuleContext.RelationParams relationParam : ruleContext.getRelationParams()) {{
            if ("RULE_RESULT".equalsIgnoreCase(relationParam.getField())) {{
                relationParam.setActualValue(true)
                ruleContext.addOutputParam(relationParam.getField(), true)
            }}
        }}
    }}

}} catch (Exception e) {{
    ruleContext.setError(e.getMessage()).setThrowable(e).addLog("condition failed: " + e.getMessage())
}}'''

    # inputParamsType 配置
    input_params_type = [{
        "field": param_code,
        "type": "java.lang.Number",
        "source": "manual"
    }]

    # outputParamsType 配置
    output_params_type = [{
        "field": "RULE_RESULT",
        "result": "",
        "type": "java.lang.Boolean"
    }]

    # relationCodeParams 配置
    relation_code_params = [{
        "code": param_code,
        "source": "manual"
    }]

    payload = {
        "ruleType": "script",
        "scriptLanguage": "groovy",
        "scriptConfig": "",
        "scriptContent": script_content,
        "inputParamsType": json.dumps(input_params_type, ensure_ascii=False),
        "ruleName": f"[脚本]{param_code}={rule_number}",
        "ruleDesc": f"[脚本]{param_code}={rule_number}",
        "version": "",
        "riskFlagHit": "0",
        "outputParamsType": json.dumps(output_params_type, ensure_ascii=False),
        "relationCodeParams": relation_code_params
    }

    headers = {
        "Host": "fat-global-ad.baofu.com",
        "sec-ch-ua-platform": '"Linux"',
        "Accept-Language": "zh-CN",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Wayland like X11; Linux x86_64; rv:136.0) Gecko/20222614 Firefox/136.0",
        "Origin": f"{BASE_URL}",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"{BASE_URL}/infrastructure/global-rule-engine/rule-engine-config-list",
        "Cookie": "tokenControl=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NzkyNTgxNjN9.vgewaDRMDLYgRP_d33IkMUwiNvByhS2QsxBuOgsDc3UJQuBrE7oOHnd2VpDCvp-zDZWpeOVG-fR59FQSClCuIg; Hm_lvt_97352b16ed2df8c3860cf5a1a65fb4dd=1779435316; HMACCOUNT=0A363431F909DC5B; Hm_lpvt_97352b16ed2df8c3860cf5a1a65fb4dd=1780925818; agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3ODA5Njc3NDh9.0x4cJNIkWVHcBbXvq6OkcI84OEWcW5agzvwZFni6YRHT0E5StPWEsNwdsne5ucIQrT0uPcLSiG5PR9weI-EU0Q"
    }

    r = requests.post(url, json=payload, headers=headers, verify=False)
    return r


# ==================== 批量新增脚本规则 ====================
def batch_create_script_rules(start_num, end_num, prefix="USD_SEA"):
    """
    批量新增脚本规则

    参数说明:
        start_num: 起始编号
        end_num: 结束编号
        prefix: 参数前缀，默认 USD_SEA

    返回:
        成功数量, 失败数量
    """
    success_count = 0
    fail_count = 0

    print(f"\n🚀 开始批量新增脚本规则 {prefix}_{start_num} ~ {prefix}_{end_num}")
    print("=" * 60)

    for i in range(start_num, end_num + 1):
        print(f"\n[{i}/{end_num}] 正在创建 [脚本]{prefix}_{i}...")

        r = create_script_rule(i)

        if r.status_code == 200:
            try:
                resp = r.json()
                code = resp.get("code", "")
                msg = resp.get("msg", "")
                data = resp.get("data", {})

                # 判断成功：code为000000 或者 data中有ruleId
                if code == "000000" or data.get("ruleId"):
                    print(f"{C_GREEN}✅ [脚本]{prefix}_{i} 创建成功{C_RESET}")
                    success_count += 1
                else:
                    print(f"{C_RED}❌ [脚本]{prefix}_{i} 创建失败: code={code}, msg={msg}{C_RESET}")
                    print(f"   完整响应: {json.dumps(resp, ensure_ascii=False)}")
                    fail_count += 1
            except Exception as e:
                print(f"{C_RED}❌ [脚本]{prefix}_{i} 响应解析失败: {e}{C_RESET}")
                fail_count += 1
        else:
            print(f"{C_RED}❌ [脚本]{prefix}_{i} 请求失败，状态码: {r.status_code}{C_RESET}")
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"📊 批量新增完成: 成功 {success_count} 个, 失败 {fail_count} 个")
    print("=" * 60)

    return success_count, fail_count


# ==================== 示例测试 ====================
if __name__ == "__main__":

    print("=" * 60)
    print("🔧 决策引擎2.0 - 新增脚本规则API测试")
    print("=" * 60)

    # ==================== 配置区（按需修改） ====================
    start_num = 27
    end_num = 40
    prefix = "USD_SEA"
    # ==================== 配置区结束 ====================

    print(f"\n📊 配置信息")
    print(f"  将新增脚本规则: {prefix}_{start_num} ~ {prefix}_{end_num}")
    print("-" * 60)

    batch_create_script_rules(start_num=start_num, end_num=end_num, prefix=prefix)

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
