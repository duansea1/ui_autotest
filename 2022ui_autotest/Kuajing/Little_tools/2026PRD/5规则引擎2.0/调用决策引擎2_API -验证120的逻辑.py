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

            # 封装汇总打印逻辑，供两次调用
            def print_final_summary():
                print("╔════════════════════════════════════════════════╗")
                print("║  🎯 最终决策结果                              ║")
                print(f"  决策流ID：{decision_flow_id}")
                if final_flag in ["reject", "dismiss", "fail", "pre_rejection"]:
                    f_color = C_RED
                elif final_flag in ["pass", "accept"]:
                    f_color = C_GREEN
                else:
                    f_color = C_YELLOW
                print(f"  最终结果：{f_color}{final_flag}{C_RESET} - {final_flag_desc}")
                steps_for_trigger = result.get("steps", [])
                api_triggers = find_trigger_steps(steps_for_trigger, final_flag)
                if api_triggers:
                    print(f"  {C_CYAN}📍 触发步骤：{'、'.join(api_triggers)}{C_RESET}")
                sc = C_RED if status == "FAILURE" else C_GREEN
                print(f"  状态：{sc}{status}{C_RESET}")
                expect_res, expect_subtype, expect_trigger, layer_map = expect_result(steps_for_trigger)
                layer_names = {1: "第一层级", 2: "第二层级", 3: "第三层级", 4: "第四层级", 5: "第五层级"}
                for layer in sorted(layer_map.keys()):
                    name = layer_names.get(layer, f"第{layer}层级")
                    items = "、".join(layer_map[layer])
                    print(f"  📂 {name} end节点：{items}")
                print(f"  预期决策结果：{C_RED}{expect_res}{C_RESET}（nodeSubType={expect_subtype}）")
                print(f"  📋 优先级：异常转人工 > 拒绝 > 预驳回 > 转人工 > 驳回 > 待渠道反馈 > 通过")
                if expect_trigger:
                    print(f"  {C_RED}⚠️ 触发步骤：{expect_trigger}{C_RESET}")
                ct = result.get("costTime", "未知")
                cs = round(float(ct) / 1000, 3) if ct != "未知" else "未知"
                print(f"  接口耗时：{cs}秒")
                print("╚════════════════════════════════════════════════╝")

            # 1. 第一次打印（原有位置）
            print_final_summary()

            steps = result.get("steps", [])
            print(f"\n📜 规则执行明细 共 {len(steps)} 条记录")
            print("=" * 60)
            for i, step in enumerate(steps, 1):
                is_last_step = (i == len(steps))
                print_tree_step(step, f"{i}", indent=0, is_last=is_last_step)
                print("  " + "-" * 56)

            print("=" * 60)

            # 2. 第二次打印在末尾，方便复看
            print("\n📌 结果快速复看")
            print_final_summary()

        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
    else:
        print(f"请求失败，状态码: {r.status_code}")


# ==================== 测试数据（按需修改） ====================
if __name__ == "__main__":

    
    biz_data = {

         "TP_INDIVIDUAL_IDNUMBER": "D7BA45B94FDC6E72A98C7DFD7D348EA700C53CCE2943EA8B554304DD06C9FAA1",
  "INDIVIDUAL_IDNUMBER": "D7BA45B94FDC6E72A98C7DFD7D348EA700C53CCE2943EA8B554304DD06C9FAA1",
  "REG_STATUS_QCC": "-1",
  "AML_SCREENING_COMPANY_NAME": "-1",
  "BENEFICIARY_NAME_RATIO_CONSISTENT_QCC": "-1",
  "DIRECTOR_ADDR_HIT_RISK_AREA": "-1",
  "TP_LEGALPERSON_RATIO": "-1",
  "LEGALPERSON_NAME_QCC": "-1",
  "SHAREHOLDER_NAME_VERIFY": "-1",
  "USCC_HIT_GLOBAL_BLACKLIST": "-1",
  "PROHIBITED_COUNTRY": "朝鲜;古巴;叙利亚;伊朗;南苏丹;索马里;也门;马里;海地;刚果(金);缅甸;阿富汗;俄罗斯;白俄罗斯;苏丹;中非共和国;几内亚比绍;利比亚;委内瑞拉",
  "NATIONALITY_DIRECTOR": "-1",
  "DIRECTOR_NAME_VERIFY": "-1",
  "PERSON_NAME_HIT_GLOBAL_BLACKLIST": "'张华,HUA ZHANG',-1",
  "COMPANY_NAME": "-1",
  "INDIVIDUAL_ID_CARD_EXPIRY_DATE_VALID": "1",
  "BENEFICIARY_ADDR_HIT_RISK_AREA": "-1",
  "LEGALPERSON_ID_CARD_EXPIRY_DATE_VALID": "-1",
  "SHAREHOLDER_NAME_IDNUMBER": "-1",
  "INDIVIDUAL_NAME_VERIFY": "-1",
  "LEGALPERSON_NAME_VERIFY": "-1",
  "MERCHANT_TAGS": "1",
  "DIRECTOR_ID_CARD_2FACTOR_PASS": "-1",
  "SHAREHOLDER_AGE": "-1",
  "REGISTERED_COUNTRY": "中国",
  "TP_INDIVIDUAL_NAME": "张华",
  "DIRECTOR_EN_NAME_HIT_GLOBAL_BLACKLIST": "",
  "LEGAL_REP_ID_NO_HIT_GLOBAL_BLACKLIST": "-1",
  "DIRECTOR_NAME_IDNUMBER": "-1",
  "LEGALPERSON_NAME": "-1",
  "DIRECTOR_IDNUMBER": "-1",
  "INDIVIDUAL_IDPHOTO": "1",
  "USCC": "-1",
  "NATIONALITY_LEGALPERSON": "-1",
  "LEGAL_REP_ADDR_HIT_RISK_AREA": "-1",
  "INDIVIDUAL_IDTYPE": "1",
  "TP_LEGALPERSON_NAME": "-1",
  "NATIONALITY_SHAREHOLDER": "-1",
  "INDI_IDNUMBER_HIT_GLOBAL_BLACKLIST": "'D7BA45B94FDC6E72A98C7DFD7D348EA700C53CCE2943EA8B554304DD06C9FAA1',-1",
  "INDIVIDUAL_ID_CARD_2FACTOR_PASS": "1",
  "BENEFICIARY_NAME_RATIO_CONSISTENT": "-1",
  "INFO_TYPE": "4",
  "BRN_QCC": "-1",
  "INDIVIDUAL_AGE": "42",
  "LEGALPERSON_ID_CARD_2FACTOR_PASS": "-1",
  "INDIVIDUAL_ADDR_HIT_RISK_AREA": "'No. 100, Miaohou Zhang Village, Zhenggang Office, Xinzheng City Zhengzhou City District Zhengzhou City Henan Province CHN',-1",
  "LEGALPERSON_IDNUMBER": "-1",
  "SHAREHOLDER_IDNUMBER": "-1",
  "TP_SHAREHOLDER_IDNUMBER": "-1",
  "TP_INDIVIDUAL_RATIO": "99.80",
  "TP_SHAREHOLDER_RATIO": "-1",
  "AML_SCREENING_BENEFICIARY_NAME": "-1",
  "DIRECTOR_IDTYPE": "-1",
  "SHAREHOLDER_ID_CARD_EXPIRY_DATE_VALID": "-1",
  "SHAREHOLDER_ID_CARD_2FACTOR_PASS": "-1",
  "INDIVIDUAL_NAME_IDNUMBER": "7a34084e2d824b63bb55b495b047360ea6fce503e03144b6,张华",
  "LEGALPERSON_NAME_IDNUMBER": "-1",
  "INDIVIDUAL_NAME": "张华",
  "LEGALPERSON_IDTYPE": "-1",
  "QUALIFIED_NO": "2606131504000256990",
  "TP_SHAREHOLDER_NAME": "-1",
  "AML_SCREENING_PERSON_NAME": "疑似命中",
  "USCC_QCC": "-1",
  "TP_DIRECTOR_RATIO": "-1",
  "DIRECTOR_ID_CARD_EXPIRY_DATE_VALID": "-1",
  "work_order_no": "100002202606131709465021246",
  "COMPANY_ADDR_HIT_RISK_AREA": "-1",
  "MOBILE_NO_HIT_GLOBAL_BLACKLIST": "2710069110358DBEBF0DB780EB8B74C0,-1",
  "AML_SCREENING_DIRECTOR_NAME": "-1",
  "DIRECTOR_IDPHOTO": "-1",
  "TP_DIRECTOR_NAME": "-1",
  "SHAREHOLDER_NAME": "-1",
  "BENEFICIARY_NAME_HIT_GLOBAL_BLACKLIST": "-1",
  "AML_SCREENING_PERSON_EN_NAME": "疑似命中",
  "AML_SCREENING_LEGAL_REP_NAME": "-1",
  "BENEFICIARY_ID_NO_HIT_GLOBAL_BLACKLIST": "-1",
  "TP_LEGALPERSON_IDNUMBER": "-1",
  "COMPANY_HIT_SERIOUS_ILLEGAL": "-1",
  "MANUAL_FLAG": "false",
  "DIRECTOR_NAME_HIT_GLOBAL_BLACKLIST": "-1",
  "AGE": "-1",
  "AML_SCREENING_DIRECTOR_EN_NAME": "-1",
  "COMPANY_NAME_HIT_GLOBAL_BLACKLIST": "-1",
  "REG_NO_HIT_GLOBAL_BLACKLIST": "-1",
  "AML_SCREENING_BENEFICIARY_EN_NAME": "-1",
  "TP_DIRECTOR_IDNUMBER": "-1",
  "LEGALPERSON_IDPHOTO": "-1",
  "COMPANY_NAME_QCC": "-1",
  "BENEFICIARY_IDPHOTO": "-1",
  "DIRECTOR_ID_NO_HIT_GLOBAL_BLACKLIST": "-1",
  "AML_SCREENING_LEGAL_EN_REP_NAME": "-1",
  "LEGAL_REP_NAME_HIT_GLOBAL_BLACKLIST": "-1",
  "BENEFICIARY_EN_NAME_HIT_GLOBAL_BLACKLIST": "",
  "LEGAL_REP_EN_NAME_HIT_GLOBAL_BLACKLIST": "",
  "DIRECTOR_NAME": "-1",
  "DIRECTOR_AGE": "-1",
  "AML_SCREENING_COMPANY_EN_NAME": "-1",
  "LEGALPERSON_AGE": "-1",
  "BENEFICIARY_IDTYPE": "-1",
  "request_id": "100002202606131709465021246",
  "BRN": "-1"
    }
    # ACCOUNT_HOLDER_MAINLAND_INDIVIDUAL
    # ACCOUNT_HOLDER_MAINLAND_ENTERPRISE  -120de 
    decisionFlowCode = "ACCOUNT_HOLDER_MAINLAND_INDIVIDUAL"
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