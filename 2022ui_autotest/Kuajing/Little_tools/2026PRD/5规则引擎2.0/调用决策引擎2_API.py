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
C_MAGENTA = Fore.MAGENTA
C_RESET = Style.RESET_ALL


# ==================== 辅助函数（无需修改） ====================
def parse_outputs(output_str):
    fields = []
    try:
        outputs = json.loads(output_str)
        for out in outputs:
            field = out.get("field", "")
            val = out.get("actualValue", "")
            fields.append(f"{field}={val}")
    except Exception:
        pass
    return fields


def risk_label(flag):
    if flag == "yes":
        return "[命中风险]"
    elif flag == "no":
        return "[无风险]"
    return "[未配置风险标识]"


def result_color(result_text):
    if result_text == "通过":
        return f"{C_GREEN}✅ {result_text}{C_RESET}"
    elif result_text == "不通过":
        return f"{C_RED}❌ {result_text}{C_RESET}"
    else:
        return f"{C_YELLOW}{result_text}{C_RESET}"


def has_error(step):
    """判断步骤是否有异常：errorMessage 非空 或 errorCode 非 000000"""
    error_msg = step.get("errorMessage", "")
    error_code = step.get("errorCode", "000000")
    return bool(error_msg) or (error_code and error_code != "000000")


def collect_end_nodes(steps, prefix="", layer=1):
    """按层级收集所有 end 节点，返回 {层级: [信息列表]}"""
    layer_map = {}
    for idx, step in enumerate(steps, 1):
        step_num = f"{prefix}{idx}" if prefix else f"{idx}"
        if step.get("nodeType") == "end":
            sub = step.get("nodeSubType", "")
            node_name = step.get("nodeName", "")
            layer_map.setdefault(layer, []).append(f"步骤{step_num}：{node_name}（{sub}）")
        for j, child in enumerate(step.get("childSteps", []), 1):
            child_num = f"{step_num}."
            child_map = collect_end_nodes([child], prefix=child_num, layer=layer + 1)
            for k, v in child_map.items():
                layer_map.setdefault(k, []).extend(v)
    return layer_map


def expect_result(steps):
    """根据 steps 判断预期决策结果，优先第一层级end节点，返回(结果名, nodeSubType, 触发步骤, 层级信息)"""
    priority_map = {
        "ABNORMAL_MANUAL": 1,
        "REJECT": 2,
        "PRE_REJECTION": 3,
        "MANUAL": 4,
        "DISMISS": 5,
        "PENDING_FEEDBACK": 6,
        "PASS": 7,
    }
    result_map = {
        "ABNORMAL_MANUAL": "异常转人工",
        "REJECT": "拒绝",
        "PRE_REJECTION": "预驳回",
        "MANUAL": "转人工",
        "DISMISS": "驳回",
        "PENDING_FEEDBACK": "待渠道反馈",
        "PASS": "通过",
    }
    # 收集层级信息
    layer_map = collect_end_nodes(steps)

    # 先检查是否有异常步骤
    for idx, step in enumerate(steps, 1):
        if step.get("nodeType") != "end":
            ec = step.get("errorCode", "000000")
            em = step.get("errorMessage", "")
            if ec and ec != "000000" or em:
                return "异常转人工", "ABNORMAL_MANUAL", f"步骤{idx}", layer_map

    # 按层级优先判断：第一层级 > 第二层级 > ...
    for layer in sorted(layer_map.keys()):
        best = None
        best_subtype = None
        best_trigger = ""
        for idx, step in enumerate(steps, 1):
            step_num = f"{idx}"
            best, best_subtype, best_trigger = _scan_end(step, step_num, layer, 1, priority_map, result_map, best, best_subtype, best_trigger)
        if best_subtype:
            return result_map.get(best_subtype, best_subtype), best_subtype, best_trigger, layer_map

    return "未知", "", "", layer_map


def _scan_end(step, step_num, target_layer, current_layer, priority_map, result_map, best, best_subtype, best_trigger):
    """递归扫描 end 节点，只在目标层级匹配"""
    if step.get("nodeType") == "end" and current_layer == target_layer:
        sub = step.get("nodeSubType", "")
        upper_sub = sub.upper()
        if upper_sub in priority_map:
            if best is None or priority_map[upper_sub] < best:
                best = priority_map[upper_sub]
                best_subtype = upper_sub
                node_name = step.get("nodeName", "")
                best_trigger = f"步骤{step_num}：{node_name}" if node_name else f"步骤{step_num}"
    for j, child in enumerate(step.get("childSteps", []), 1):
        child_num = f"{step_num}.{j}"
        best, best_subtype, best_trigger = _scan_end(child, child_num, target_layer, current_layer + 1, priority_map, result_map, best, best_subtype, best_trigger)
    return best, best_subtype, best_trigger


def find_trigger_steps(steps, final_flag):
    """查找所有匹配 finalResultFlag 的 end 步骤"""
    flag_to_subtype = {
        "reject": "REJECT",
        "dismiss": "DISMISS",
        "pre_rejection": "PRE_REJECTION",
        "manual": "MANUAL",
        "pass": "PASS",
        "pending_feedback": "PENDING_FEEDBACK",
    }
    target = flag_to_subtype.get(final_flag, final_flag).upper()
    triggers = []
    for idx, step in enumerate(steps, 1):
        if step.get("nodeType") == "end" and step.get("nodeSubType", "").upper() == target:
            node_name = step.get("nodeName", "")
            triggers.append(f"步骤{idx}：{node_name}" if node_name else f"步骤{idx}")
        for j, child in enumerate(step.get("childSteps", []), 1):
            if child.get("nodeType") == "end" and child.get("nodeSubType", "").upper() == target:
                node_name = child.get("nodeName", "")
                triggers.append(f"步骤{idx}.{j}：{node_name}" if node_name else f"步骤{idx}.{j}")
    return triggers


def result_with_error(result_text, step):
    """区分正常判定不通过 vs 异常导致不通过"""
    error_msg = step.get("errorMessage", "")
    error_code = step.get("errorCode", "000000")
    is_abnormal = bool(error_msg) or (error_code and error_code != "000000")

    if is_abnormal:
        reason = error_msg if error_msg else f"errorCode={error_code}"
        return f"{C_RED}❌ {result_text}（异常）{C_RESET}", reason
    elif result_text == "通过":
        return f"{C_GREEN}✅ {result_text}{C_RESET}", ""
    elif result_text == "不通过":
        return f"{C_RED}❌ {result_text}{C_RESET}", ""
    else:
        return f"{C_YELLOW}{result_text}{C_RESET}", ""


def error_detail(step):
    msg = step.get("errorMessage", "")
    code = step.get("errorCode", "")
    parts = []
    if msg:
        parts.append(msg)
    if code and code != "000000":
        parts.append(f"errorCode：{code}")
    return "；".join(parts) if parts else ""


def print_tree_step(step, step_num, indent=0, is_last=False):
    node_type = step.get("nodeType", "")
    node_sub_type = step.get("nodeSubType", "")
    node_name = step.get("nodeName", "")
    node_code = step.get("nodeCode", "")
    result_text = step.get("result", "未知")
    risk_flag = step.get("riskFlagHit", None)
    expands = [e for e in step.get("expands", []) if e and e != "[]"]

    # 缩进
    p = "    │   " * indent
    cur = "    └── " if is_last else "    ├── "
    bar = "    │   "

    if node_type == "end":
        print(f"{p}{cur}🔚 {step_num}：{node_name or node_code or '未知节点'}")
        print(f"{p}{bar}    nodeType：{C_CYAN}{node_type}{C_RESET}，nodeSubType：{C_CYAN}{node_sub_type}{C_RESET}")
        # end 节点没有独立 result，用 isSuccess 判断
        is_success = step.get("isSuccess", None)
        if is_success is not None:
            end_result = "通过" if is_success else "不通过"
            colored_result, error_reason = result_with_error(end_result, step)
        else:
            colored_result, error_reason = result_with_error(result_text, step)
        print(f"{p}{bar}    执行结果：{colored_result}")
        if error_reason:
            print(f"{p}{bar}    ❗异常原因：{error_reason}")
        # end 节点也打印 riskFlagHit
        if risk_flag is not None:
            flag_color = C_RED if risk_flag == "yes" else C_GREEN
            print(f"{p}{bar}    🚩 riskFlagHit：{flag_color}{risk_flag}{C_RESET} {risk_label(risk_flag)}")
        else:
            print(f"{p}{bar}    🚩 riskFlagHit：未返回")
        if expands:
            print(f"{p}{bar}    💬 expands：{' | '.join(expands)}")
    else:
        rule_id = step.get("ruleId", "") or step.get("nodeCode", "未知")
        rule_name = step.get("ruleName", "") or step.get("nodeName", "未知")
        print(f"{p}{cur}⚙️ {step_num}：{rule_id} - {rule_name}")

        if node_type == "rule_set":
            rule_set_code = step.get("ruleSetCode", "")
            rule_set_name = step.get("ruleSetName", "")
            print(f"{p}{bar}📂 规则集：{C_MAGENTA}{rule_set_code}{C_RESET} - {C_MAGENTA}{rule_set_name}{C_RESET}")
            if node_name:
                print(f"{p}{bar}    节点名称：{C_MAGENTA}{node_name}{C_RESET}")

        outputs = parse_outputs(step.get("output", "[]"))
        if outputs:
            print(f"{p}{bar}    📤 输出结果：{', '.join(outputs)}")

        # hitMappings 打印
        hit_mappings = step.get("hitMappings", {})
        if hit_mappings:
            print(f"{p}{bar}    📑 hitMappings：")
            print(f"{p}{bar}      {json.dumps(hit_mappings, indent=2, ensure_ascii=False)}")

        colored_result, error_reason = result_with_error(result_text, step)
        print(f"{p}{bar}    执行结果：{colored_result}")
        if error_reason:
            print(f"{p}{bar}    ❗异常原因：{error_reason}")

        if risk_flag is not None:
            flag_color = C_RED if risk_flag == "yes" else C_GREEN
            print(f"{p}{bar}    🚩 riskFlagHit：{flag_color}{risk_flag}{C_RESET} {risk_label(risk_flag)}")
        else:
            print(f"{p}{bar}    🚩 riskFlagHit：未返回")

        if expands:
            print(f"{p}{bar}    💬 expands：{' | '.join(expands)}")
        else:
            print(f"{p}{bar}    💬 expands：未返回")

    # 递归处理子步骤（支持多层嵌套）
    sub_steps = step.get("childSteps", [])
    for j, sub_step in enumerate(sub_steps, 1):
        is_last_sub = (j == len(sub_steps))
        print_tree_step(sub_step, f"{step_num}.{j}", indent=indent + 1, is_last=is_last_sub)


# ==================== 公共配置（无需修改） ====================
url = "http://10.254.224.216:10014/v1/decision/flow/query/api/execute"


# ==================== 发送请求（无需修改） ====================
def send_request(data):
    r = requests.post(url, json=data, headers={"Content-Type": "application/json", "accept": "*/*"})
    return r


# ==================== 响应解析（无需修改） ====================
def parse_response(r, excue_time, data=None):
    print("📋 原始响应")
    print(f"状态码: {r.status_code}")
    if r.status_code == 200:
        try:
            resp = r.json()
            print("🔍 原始响应（格式化）")
            print(json.dumps(resp, indent=2, ensure_ascii=False))
        except Exception:
            print(f"原始响应内容: {r.text}")

    print("\n📌 优化后响应")
    if r.status_code == 200:
        try:
            resp = r.json()
            result = resp.get("result", {})

            decision_flow_id = result.get("decisionFlowId", "未知")
            final_flag = result.get("finalResultFlag", "未知")
            final_flag_desc = result.get("finalResultFlagDesc", "未知")
            status = result.get("status", "未知")

            print("╔════════════════════════════════════════════════╗")
            print("║  🎯 最终决策结果                              ║")
            print(f"  决策流ID：{decision_flow_id}")
            if final_flag in ["reject", "dismiss", "fail", "pre_rejection"]:
                flag_color = C_RED
            elif final_flag in ["pass", "accept"]:
                flag_color = C_GREEN
            else:
                flag_color = C_YELLOW
            print(f"  最终结果：{flag_color}{final_flag}{C_RESET} - {final_flag_desc}")
            steps = result.get("steps", [])
            api_triggers = find_trigger_steps(steps, final_flag)
            if api_triggers:
                print(f"  {C_CYAN}📍 触发步骤：{'、'.join(api_triggers)}{C_RESET}")
            status_color = C_RED if status == "FAILURE" else C_GREEN
            print(f"  状态：{status_color}{status}{C_RESET}")

            # 预期决策结果：根据 end 节点判断
            expect_res, expect_subtype, expect_trigger, layer_map = expect_result(steps)
            # 打印每层 end 节点
            layer_names = {1: "第一层级", 2: "第二层级", 3: "第三层级", 4: "第四层级", 5: "第五层级"}
            for layer in sorted(layer_map.keys()):
                name = layer_names.get(layer, f"第{layer}层级")
                items = "、".join(layer_map[layer])
                print(f"  📂 {name} end节点：{items}")
            print(f"  预期决策结果：{C_RED}{expect_res}{C_RESET}（nodeSubType={expect_subtype}）")
            print(f"  📋 优先级：异常转人工 > 拒绝 > 预驳回 > 转人工 > 驳回 > 待渠道反馈 > 通过")
            if expect_trigger:
                print(f"  {C_RED}⚠️ 触发步骤：{expect_trigger}{C_RESET}")
            cost_time = result.get("costTime", "未知")
            cost_sec = round(float(cost_time) / 1000, 3) if cost_time != "未知" else "未知"
            print(f"  接口耗时：{cost_sec}秒")
            print("╚════════════════════════════════════════════════╝")

            print(f"\n📜 规则执行明细 共 {len(steps)} 条记录")
            print("=" * 60)
            for i, step in enumerate(steps, 1):
                is_last_step = (i == len(steps))
                print_tree_step(step, f"{i}", indent=0, is_last=is_last_step)
                print("  " + "-" * 56)

            print("=" * 60)

        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
    else:
        print(f"请求失败，状态码: {r.status_code}")


# ==================== 测试数据（按需修改） ====================
if __name__ == "__main__":

    biz_data = {
        "USD_SEA_40": "40",
		"USD_SEA_39": "39",
		"USD_SEA_38": "38",
		"USD_SEA_37": "37",
		"USD_SEA_36": "36",
		"USD_SEA_35": "35",
		"USD_SEA_34": "34",
		"USD_SEA_33": "33",
		"USD_SEA_32": "32",
		"USD_SEA_31": "31",
		"USD_SEA_30": "30",
		"USD_SEA_10": "10",
		"USD_SEA_11": "11",
		"USD_SEA_12": "12",
		"USD_SEA_13": "13",
		"USD_SEA_14": "14",
		"USD_SEA_15": "15",
		"USD_SEA_16": "16",
		"USD_SEA_17": "17",
		"USD_SEA_18": "18",
		"USD_SEA_19": "19",
		"USD_SEA_20": "20",
		"USD_SEA_21": "21",
		"USD_SEA_22": "22",
		"USD_SEA_23": "23",
		"USD_SEA_24": "24",
		"USD_SEA_25": "25",
		"USD_SEA_26": "26",
		"USD_SEA_27": "27",
		"USD_SEA_28": "28",
		"USD_SEA_29": "29",
		"USD_SEA_8": "8",
		"USD_SEA_9": "9",
		"USD_SEA_7": "7"
    }
    # SEA_NEW0003-专属
    biz_data = {
        "USD_SEA_1": "1hua",
		"USD_SEA_2": "2li",
		"USD_SEA_22": "22",
		"USD_SEA_21": "21",
        
        "USD_SEA_5": "51",

		"USD_SEA_34": "34",
		"USD_SEA_6": "6",
		"USD_SEA_24": "24",

        "USD_SEA_23": "231",
		"USD_SEA_25": "25",

        "USD_SEA_26": "26",
        
        "USD_SEA_30": "301",
		"USD_SEA_31": "311",

        "SEA_BOOLE_1": "true",

        "SEA_RATE_2_5": "3",
        "SEA_AMT": "20",  
        "USD_SEA_20": "20",
		"USD_SEA_19": "19",
		"USD_SEA_18": "18",
		"USD_SEA_17": "17",
    }
    biz_data1 ={
            "externalItemId": "9985458",
            "ABS_ORDERAMT_SUM_QTY_PRICR": "0",
            "CLIENT_90D_1000USD_ORDER_QTYAMT": "0",
            "externalOrderId": "2602091005419414115",
            "TAG_ID": "2509021003000524137",
            "FX_BD_TRANAMT": "100",
            "CLIENT_90D_1000USD_ORDER_QTY": "0",
            "FX_BD_ITEMNAME": "LV bag包",
            "FX_BD_PRICE": "25",
            "CLIENT_90D_ORDERAMT": "0",
            "CHANNEL_RATE": "0.0063864955",
            "CLIENT_LABEL": "东方红",
            "CLIENT_90D_5000USD_ORDER_QTY": "0",
            "CLIENT_90D_5000USD_ORDER_QTYAMT": "0",
            "FX_BD_QTY": "2"
    }
    # NEW_FX_BD_DIANSHANG -结汇的决策流
    # SEA_NEW0007--我的sea的
    decisionFlowCode = "SEA_NEW0007"
    data = {
        "decisionFlowCode": decisionFlowCode,
        "executeType": "SYNC",
        "requestSerialId": "uuid-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "initiatingParty": "Python-sea0604-测试决策流",
        "operator": f"测试sea-{decisionFlowCode}",
        "bizData": biz_data,
        "extensionData": {}
    }

    print("最终API地址：", url)
    print("\n📨 发送请求参数")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("-" * 50)

    excue_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'------开始执行时间：{excue_time}----开始执行打印返回结果')

    r = send_request(data)
    parse_response(r, excue_time, data)

    print(f'------开始执行时间-目前已执行结束：{C_RED}{excue_time}{C_RESET}------------------------')