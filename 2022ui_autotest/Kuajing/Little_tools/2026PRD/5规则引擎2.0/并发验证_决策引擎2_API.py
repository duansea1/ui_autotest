import requests
import json
from datetime import datetime
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

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
    error_msg = step.get("errorMessage", "")
    error_code = step.get("errorCode", "000000")
    return bool(error_msg) or (error_code and error_code != "000000")


def collect_end_nodes(steps, prefix="", layer=1):
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
    layer_map = collect_end_nodes(steps)

    for idx, step in enumerate(steps, 1):
        if step.get("nodeType") != "end":
            ec = step.get("errorCode", "000000")
            em = step.get("errorMessage", "")
            if ec and ec != "000000" or em:
                return "异常转人工", "ABNORMAL_MANUAL", f"步骤{idx}", layer_map

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

    p = "    │   " * indent
    cur = "    └── " if is_last else "    ├── "
    bar = "    │   "

    if node_type == "end":
        print(f"{p}{cur}🔚 {step_num}：{node_name or node_code or '未知节点'}")
        print(f"{p}{bar}    nodeType：{C_CYAN}{node_type}{C_RESET}，nodeSubType：{C_CYAN}{node_sub_type}{C_RESET}")
        is_success = step.get("isSuccess", None)
        if is_success is not None:
            end_result = "通过" if is_success else "不通过"
            colored_result, error_reason = result_with_error(end_result, step)
        else:
            colored_result, error_reason = result_with_error(result_text, step)
        print(f"{p}{bar}    执行结果：{colored_result}")
        if error_reason:
            print(f"{p}{bar}    {C_RED}❗异常原因：{error_reason}{C_RESET}")
        if risk_flag is not None:
            flag_color = C_RED if risk_flag == "yes" else C_GREEN
            print(f"{p}{bar}    🚩 riskFlagHit：{flag_color}{risk_flag}{C_RESET} {risk_label(risk_flag)}")
        else:
            print(f"{p}{bar}    🚩 riskFlagHit：{C_YELLOW}未返回{C_RESET}")
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

        hit_mappings = step.get("hitMappings", {})
        if hit_mappings:
            print(f"{p}{bar}    📑 hitMappings：")
            print(f"{p}{bar}      {json.dumps(hit_mappings, indent=2, ensure_ascii=False)}")

        colored_result, error_reason = result_with_error(result_text, step)
        print(f"{p}{bar}    执行结果：{colored_result}")
        if error_reason:
            print(f"{p}{bar}    {C_RED}❗异常原因：{error_reason}{C_RESET}")

        if risk_flag is not None:
            flag_color = C_RED if risk_flag == "yes" else C_GREEN
            print(f"{p}{bar}    🚩 riskFlagHit：{flag_color}{risk_flag}{C_RESET} {risk_label(risk_flag)}")
        else:
            print(f"{p}{bar}    🚩 riskFlagHit：{C_YELLOW}未返回{C_RESET}")

        if expands:
            print(f"{p}{bar}    💬 expands：{' | '.join(expands)}")
        else:
            print(f"{p}{bar}    💬 expands：{C_YELLOW}未返回{C_RESET}")

    sub_steps = step.get("childSteps", [])
    for j, sub_step in enumerate(sub_steps, 1):
        is_last_sub = (j == len(sub_steps))
        print_tree_step(sub_step, f"{step_num}.{j}", indent=indent + 1, is_last=is_last_sub)


# ==================== 公共配置（无需修改） ====================
url = "http://10.254.224.216:10014/v1/decision/flow/query/api/execute"


def send_request(data):
    r = requests.post(url, json=data, headers={"Content-Type": "application/json", "accept": "*/*"})
    return r


def parse_response_detail(r):
    """解析并打印响应"""
    if r.status_code != 200:
        print(f"请求失败，状态码: {r.status_code}")
        return None, None

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

        expect_res, expect_subtype, expect_trigger, layer_map = expect_result(steps)
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

        return final_flag, expect_res
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return None, None


# ==================== 测试数据（按需修改） ====================
if __name__ == "__main__":

    # ========== 并发配置 ==========
    # 方式1：持续时间模式（推荐）
    INTERVAL_SECONDS = 1          # 每隔多少秒执行一轮
    DURATION_SECONDS = 60         # 持续多少秒（0=使用MAX_ROUNDS模式）
    CONCURRENT_PER_ROUND = 100    # 每轮并发多少个请求
    
    # ========== 断言配置 ==========
    ENABLE_ASSERT = True         # True=断言失败时抛出异常，False=仅打印比对结果
    
    # 方式2：轮次模式（当DURATION_SECONDS=0时生效）
    # MAX_ROUNDS = 1000           # 0=无限循环，>0=执行指定次数后停止

    # ========== 测试用例定义 ==========
    # 用例1：Terminal#909-1023  预期 finalFlag=pass，预期决策结果=通过
    biz_data_case1 = {
        "USD_SEA_1": "1hua",
        "USD_SEA_2": "2li",
        "USD_SEA_22": "22",
        "USD_SEA_21": "21",
        "USD_SEA_5": "5",
        "USD_SEA_34": "34",
        "USD_SEA_6": "6",
        "USD_SEA_24": "241",
        "USD_SEA_23": "23",
        "USD_SEA_25": "25",
        "USD_SEA_26": "261",
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

    # 用例2：Terminal#916-1024  预期 finalFlag=pre_rejection，预期决策结果=预驳回
    biz_data_case2 = {
        "USD_SEA_1": "1hua",
        "USD_SEA_2": "2li",
        "USD_SEA_22": "22",
        "USD_SEA_21": "21",
        "USD_SEA_5": "5",
        "USD_SEA_34": "34",
        "USD_SEA_6": "6",
        "USD_SEA_24": "241",
        "USD_SEA_23": "23",
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

    test_cases = [
        {
            "name": "用例1",
            "decisionFlowCode": "SEA_NEW0007",
            "bizData": biz_data_case1,
            "expect_final_flag": "pass",
            "expect_result": "通过",
        },
        {
            "name": "用例2",
            "decisionFlowCode": "SEA_NEW0007",
            "bizData": biz_data_case2,
            "expect_final_flag": "pre_rejection",
            "expect_result": "预驳回",
        },
    ]

    # 兼容旧版MAX_ROUNDS配置
    MAX_ROUNDS = 0  # 旧版配置，0表示不启用
    
    print(f"最终API地址：{url}")
    print(f"每轮并发数：{CONCURRENT_PER_ROUND}个")
    print(f"断言模式：{'启用（失败将抛出异常）' if ENABLE_ASSERT else '禁用（仅打印比对结果）'}")
    
    if DURATION_SECONDS > 0:
        print(f"持续时间：{DURATION_SECONDS}秒")
        print(f"轮次间隔：{INTERVAL_SECONDS}秒")
        print(f"预计总请求数：约{DURATION_SECONDS // INTERVAL_SECONDS * CONCURRENT_PER_ROUND}个")
    else:
        print(f"最大执行轮次：{'无限循环' if MAX_ROUNDS == 0 else MAX_ROUNDS}轮")
        print(f"轮次间隔：{INTERVAL_SECONDS}秒")
    
    print(f"测试用例数量：{len(test_cases)}个")
    print("=" * 70)

    round_num = 0
    total_pass = 0
    total_fail = 0
    lock = threading.Lock()
    start_time = time.time()
    duration_mode = DURATION_SECONDS > 0

    while True:
        round_num += 1
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 计算已运行时间
        elapsed = time.time() - start_time
        
        print(f"\n{'=' * 70}")
        print(f"  第 {round_num} 轮  {now_str}  [已运行{int(elapsed)}秒]")
        print(f"{'=' * 70}")

        round_pass = 0
        round_fail = 0

        # 根据配置决定并发数
        if CONCURRENT_PER_ROUND > 0:
            # 使用指定并发数，每个请求轮流使用test_cases的数据
            def run_single_case(idx):
                tc = test_cases[idx % len(test_cases)]
                data = {
                    "decisionFlowCode": tc["decisionFlowCode"],
                    "executeType": "SYNC",
                    "requestSerialId": f"concurrent-{round_num}-req{idx}-" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "initiatingParty": f"Python-并发测试-第{round_num}轮",
                    "operator": f"并发测试-请求{idx}",
                    "bizData": tc["bizData"],
                    "extensionData": {}
                }
                r = send_request(data)

                # 打印请求参数
                print(f"\n  【请求{idx}】📨 发送请求参数")
                print(json.dumps(data, indent=4, ensure_ascii=False))

                actual_flag, actual_result = parse_response_detail(r)

                # 比对结果
                exp_flag = tc["expect_final_flag"]
                exp_res = tc["expect_result"]

                flag_ok = (actual_flag == exp_flag) if actual_flag else False
                res_ok = (actual_result == exp_res) if actual_result else False

                with lock:
                    if flag_ok and res_ok:
                        print(f"\n  【请求{idx}】✅ 比对通过  预期finalFlag={exp_flag} 实际={actual_flag}  预期result={exp_res} 实际={actual_result}")
                    else:
                        print(f"\n  【请求{idx}】❌ 比对失败  预期finalFlag={exp_flag} 实际={actual_flag}  预期result={exp_res} 实际={actual_result}")
                        if ENABLE_ASSERT:
                            raise AssertionError(f"【请求{idx}】断言失败！预期finalFlag={exp_flag} 实际={actual_flag}，预期result={exp_res} 实际={actual_result}")
                    return flag_ok and res_ok

            # 多线程并发执行
            with ThreadPoolExecutor(max_workers=CONCURRENT_PER_ROUND) as executor:
                futures = [executor.submit(run_single_case, i) for i in range(CONCURRENT_PER_ROUND)]
                for future in as_completed(futures):
                    if future.result():
                        round_pass += 1
                    else:
                        round_fail += 1
        else:
            # 使用test_cases的数量作为并发数
            def run_single_case(tc):
                data = {
                    "decisionFlowCode": tc["decisionFlowCode"],
                    "executeType": "SYNC",
                    "requestSerialId": f"concurrent-{round_num}-{tc['name']}-" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "initiatingParty": f"Python-并发测试-第{round_num}轮",
                    "operator": f"并发测试-{tc['name']}",
                    "bizData": tc["bizData"],
                    "extensionData": {}
                }
                r = send_request(data)

                # 打印请求参数
                print(f"\n  【{tc['name']}】📨 发送请求参数")
                print(json.dumps(data, indent=4, ensure_ascii=False))

                actual_flag, actual_result = parse_response_detail(r)

                # 比对结果
                exp_flag = tc["expect_final_flag"]
                exp_res = tc["expect_result"]

                flag_ok = (actual_flag == exp_flag) if actual_flag else False
                res_ok = (actual_result == exp_res) if actual_result else False

                with lock:
                    if flag_ok and res_ok:
                        print(f"\n  【{tc['name']}】✅ 比对通过  预期finalFlag={exp_flag} 实际={actual_flag}  预期result={exp_res} 实际={actual_result}")
                    else:
                        print(f"\n  【{tc['name']}】❌ 比对失败  预期finalFlag={exp_flag} 实际={actual_flag}  预期result={exp_res} 实际={actual_result}")
                        if ENABLE_ASSERT:
                            raise AssertionError(f"【{tc['name']}】断言失败！预期finalFlag={exp_flag} 实际={actual_flag}，预期result={exp_res} 实际={actual_result}")
                    return flag_ok and res_ok

            # 多线程并发执行所有用例
            with ThreadPoolExecutor(max_workers=len(test_cases)) as executor:
                futures = {executor.submit(run_single_case, tc): tc for tc in test_cases}
                for future in as_completed(futures):
                    if future.result():
                        round_pass += 1
                    else:
                        round_fail += 1

        with lock:
            total_pass += round_pass
            total_fail += round_fail

        print(f"\n{'=' * 70}")
        print(f"  第 {round_num} 轮汇总  ✅通过={round_pass}  ❌失败={round_fail}  累计通过={total_pass}  累计失败={total_fail}")
        print(f"{'=' * 70}")

        if duration_mode:
            # 按时间停止
            if elapsed >= DURATION_SECONDS:
                print(f"\n已达到指定时间 {DURATION_SECONDS}秒，退出。")
                break
        else:
            # 按轮次停止
            if MAX_ROUNDS > 0 and round_num >= MAX_ROUNDS:
                print(f"\n已达到指定轮次 {MAX_ROUNDS}，退出。")
                break
        
        time.sleep(INTERVAL_SECONDS)
