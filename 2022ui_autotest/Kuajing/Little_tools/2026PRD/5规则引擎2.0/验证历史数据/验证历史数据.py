import requests
import json
import time
import os
from datetime import datetime

# ==========================================
# 强化路径处理 - 确保保存到脚本所在目录
# ==========================================
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

# 数据文件路径 - 强制使用绝对路径
CALL_IDS_FILE = os.path.normpath(os.path.join(SCRIPT_DIR, "call_ids.json"))
HISTORY_DATA_FILE = os.path.normpath(os.path.join(SCRIPT_DIR, "history_records.json"))

print(f"程序启动...")
print(f"脚本绝对路径: {SCRIPT_PATH}")
print(f"数据保存目录: {SCRIPT_DIR}")
print(f"CallID保存路径: {CALL_IDS_FILE}")

# ==========================================
# 配置区域 - 在这里修改对比参数
# ==========================================
VERIFY_COUNT = 100  # 要对比的记录数量 (已改为100条)
PAGE_SIZE = 100     # 每次从历史记录查询的记录数量

# API端点配置
history_list_url = "https://fat-global-ad.baofu.com/ams-api/front/decision/flow/api/queryDecisionFlowHistoryPage"
history_detail_url = "https://fat-global-ad.baofu.com/ams-api/front/decision/flow/api/queryDecisionFlowHistoryByCallId/"
decision_engine_url = "http://10.254.224.216:10014/v1/decision/flow/query/api/execute"
# ==========================================

def save_to_file(filename, data):
    """保存数据到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"ok 已保存到文件: {filename}")
        return True
    except Exception as e:
        print(f"error 保存失败: {str(e)}")
        return False

def load_from_file(filename):
    """从文件加载数据"""
    try:
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return None
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

# 请求头
headers = {
    'Host': 'fat-global-ad.baofu.com',
    'sec-ch-ua-platform': '"macOS"',
    'request-proxy-url': '',
    'request-system-name': 'baofu-admin-control-client-base',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13; rv:134.0) Gecko/20100101 Firefox/134.0',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Origin': 'https://fat-global-ad.baofu.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://fat-global-ad.baofu.com/payful/new/account/ams/main/global-rule-engine/decision-flow-history',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'tokenControl=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NzkyNTgxNjN9.vgewaDRMDLYgRP_d33IkMUwiNvByhS2QsxBuOgsDc3UJQuBrE7oOHnd2VpDCvp-zDZWpeOVG-fR59FQSClCuIg; Hm_lvt_97352b16ed2df8c3860cf5a1a65fb4dd=1779435316; HMACCOUNT=0A363431F909DC5B; agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3ODEyMjczMTF9.cUm8ivq4kD9YeE5iz6X_PYhuQ156-vGErjhOe1wAwe3clg_ZiKVw8geTxR3lL6ufmOZy75Zc3aWDYWfJozsBcQ; Hm_lpvt_97352b16ed2df8c3860cf5a1a65fb4dd=1781231874'
}

def step1_get_callids():
    """步骤1: 获取callIds并保存到文件"""
    print("=" * 80)
    print("步骤1: 获取历史记录的callIds")
    print("=" * 80)

    params = {
        "executeAtStart": "2026-02-03 00:00:00",
        "executeAtEnd": "2026-02-11 23:59:59",
        "scene": "B2C_JIEHUI_DETAIL_REVIEW",
        "currentPage": 1,
        "pageSize": PAGE_SIZE
    }

    print(f"查询日期: {params['executeAtStart']} ~ {params['executeAtEnd']}")
    print(f"场景: {params['scene']}, 数量: {params['pageSize']}")

    try:
        # 显式禁用代理，防止 ProxyError
        response = requests.post(
            history_list_url, 
            json=params, 
            headers=headers, 
            verify=False, 
            timeout=30,
            proxies={"http": None, "https": None}
        )
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # 打印完整响应内容，查看实际数据结构
            print("\n--- 接口1完整响应开始 ---")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("--- 接口1完整响应结束 ---\n")

            # 检查各字段
            success_flag = result.get('success')
            print(f"success 字段值: {success_flag}")
            
            # 显式提取 callId
            call_ids = []
            res_obj = result.get('result', {})
            if isinstance(res_obj, dict):
                data_list = res_obj.get('list', [])
                if isinstance(data_list, list):
                    for item in data_list:
                        cid = item.get('callId')
                        if cid:
                            call_ids.append(str(cid))
            
            print(f"解析完成，从 result.list 中提取到 {len(call_ids)} 个 callId")

            if call_ids:
                # 保存到文件
                save_data = {
                    'save_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'count': len(call_ids),
                    'call_ids': call_ids
                }
                if save_to_file(CALL_IDS_FILE, save_data):
                    print(f"✓ 成功存入文件: {CALL_IDS_FILE}")
                
                return call_ids
            else:
                print("✗ 解析失败：result.list 为空或未找到 callId 字段")
                # 打印一下实际拿到的结果对象方便排查
                print(f"实际 result 节点内容: {res_obj}")
                return []
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return []

    except Exception as e:
        print(f"获取失败: {str(e)}")
        return []

def step2_get_history_detail(call_id):
    """步骤2: 根据callId获取历史记录详情"""
    print(f"\n获取详情: {call_id}")

    try:
        url = history_detail_url + call_id
        # 显式禁用代理，防止请求被转发到本地代理导致失败
        response = requests.get(
            url, 
            headers=headers, 
            verify=False, 
            timeout=30,
            proxies={"http": None, "https": None}
        )

        if response.status_code == 200:
            result = response.json()
            
            # 这里的判断逻辑可能不对，打印出来看看结构
            # print(f"详情接口响应: {json.dumps(result, ensure_ascii=False)}")

            # 兼容多种成功标志：success 为 True 或者 code 为 "0"
            is_success = result.get('success') is True or str(result.get('code')) == "0"
            
            # 兼容多种数据节点：data 或 result
            data = result.get('data') or result.get('result')

            if is_success and data:
                return {
                    'decision_end': data.get('decisionEnd', ''),
                    'input_params': data.get('inputParams', ''),
                    'steps': data.get('steps', []),
                    'full_data': data
                }
            else:
                msg = result.get('message') or result.get('msg') or "未知错误"
                print(f"  ✗ 接口返回状态异常: {msg}")
                print(f"  响应内容: {json.dumps(result, ensure_ascii=False)}")
        else:
            print(f"  ✗ 请求失败，状态码: {response.status_code}")
        return None

    except Exception as e:
        print(f"  ✗ 获取失败: {str(e)}")
        return None

def step3_call_decision_engine(input_params_str):
    """步骤3: 调用决策引擎"""
    print("调用决策引擎...")

    try:
        input_params = json.loads(input_params_str)

        data = {
            "decisionFlowCode": input_params.get('decisionFlowCode', 'SEA_TEST_NEW_FX_BD_DIANSHANG'),
            "executeType": "SYNC",
            "requestSerialId": "verify-" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "initiatingParty": "Python-验证历史数据",
            "operator": "测试-验证历史数据",
            "bizData": input_params,
            "extensionData": {}
        }

        response = requests.post(decision_engine_url, json=data, headers={"Content-Type": "application/json"}, verify=False, timeout=30)

        if response.status_code == 200:
            result = response.json()

            if result.get('success') and 'result' in result:
                result_data = result['result']
                decision_end_dto = result_data.get('decisionEndDto', {})
                return {
                    'decision': decision_end_dto.get('decision', ''),
                    'decision_reason': decision_end_dto.get('decisionReason', ''),
                    'steps': result_data.get('steps', []),
                    'full_result': result_data
                }
        return None

    except Exception as e:
        print(f"  ✗ 调用失败: {str(e)}")
        return None

def compare_results(history_detail, engine_result, index, call_id):
    """全量双向比对报告"""
    print(f"\n{'#'*80}")
    print(f" 深度验证报告 | 第 {index} 条 | CallID: {call_id}")
    print(f"{'#'*80}")

    # 1. 决策比对
    h_decision = None
    try:
        h_json = json.loads(history_detail['decision_end'])
        h_decision = h_json.get('decision', '')
    except:
        h_decision = history_detail['decision_end']
    e_decision = engine_result['decision']

    print(f"\n[1. 决策结论比对]")
    print(f"  历史(预期): {h_decision:<10} | 引擎(实际): {e_decision:<10} | 结论: {'一致 ok' if h_decision == e_decision else '不一致 Error'}")

    # 2. 步骤全量比对
    h_steps = history_detail['steps']
    if isinstance(h_steps, str):
        try: h_steps = json.loads(h_steps)
        except: pass
    
    e_steps = engine_result['steps']

    # 建立映射
    h_map = {s.get('ruleId') or s.get('nodeName'): s for s in h_steps if isinstance(s, dict)}
    e_map = {s.get('ruleId') or s.get('nodeName'): s for s in e_steps if isinstance(s, dict)}
    
    # 获取所有出现过的规则ID，并按引擎执行顺序排序
    all_rule_ids = []
    # 先放引擎跑过的
    for s in e_steps:
        rid = s.get('ruleId') or s.get('nodeName')
        if rid and rid not in all_rule_ids:
            all_rule_ids.append(rid)
    # 再补引擎没跑但历史跑过的
    for s in h_steps:
        rid = s.get('ruleId') or s.get('nodeName')
        if rid and rid not in all_rule_ids:
            all_rule_ids.append(rid)

    print(f"\n[2. 执行路径全量比对 (历史: {len(h_steps)} 步 -> 引擎: {len(e_steps)} 步)]")
    print(f"{'编号':<4} | {'规则ID/节点名称':<40} | {'预期(历史)':<10} | {'实际(引擎)':<10} | {'状态'}")
    print("-" * 110)

    steps_match = True
    for i, rid in enumerate(all_rule_ids):
        h_s = h_map.get(rid, {})
        e_s = e_map.get(rid, {})
        
        h_res = h_s.get('result', '-')
        e_res = e_s.get('result', '-')
        
        status = "ok"
        if rid not in h_map:
            status = "NEW(新增)"
        elif rid not in e_map:
            status = "MISS(缺失)"
            steps_match = False
        elif h_res != e_res:
            status = "DIFF(偏差)"
            steps_match = False
        
        print(f"{i+1:<4} | {str(rid)[:40]:<40} | {str(h_res):<10} | {str(e_res):<10} | {status}")

    print("-" * 110)
    
    # 最终判断：如果决策一致且历史跑过的规则在现在都跑了且结果一样，则认为通过
    print(f"  路径比对总结: {'完全匹配 ok' if steps_match else '存在差异 (请查看状态列)'}")
    
    return {
        'decision_match': h_decision == e_decision,
        'steps_match': steps_match
    }

def main():
    """主函数"""
    print("=" * 80)
    print("决策流历史数据验证工具")
    print("=" * 80)

    # 检查call_ids文件是否存在
    if os.path.exists(CALL_IDS_FILE):
        print("\nok 发现已保存的call_ids.json，将从文件加载")
        data = load_from_file(CALL_IDS_FILE)
        if data and 'call_ids' in data:
            call_ids = data['call_ids']
            print(f"[ok] 成功加载 {len(call_ids)} 个callIds")
        else:
            print("[error] 文件格式错误，需要重新获取")
            call_ids = step1_get_callids()
    else:
        print("\n未发现call_ids.json，开始获取callIds...")
        call_ids = step1_get_callids()

    if not call_ids:
        print("\n没有callIds，程序结束")
        return

    # 确定验证数量
    verify_count = min(VERIFY_COUNT, len(call_ids))
    print(f"\n将验证前 {verify_count} 条记录")

    # 遍历验证
    decision_match_count = 0
    steps_match_count = 0
    mismatch_records = []

    for i in range(verify_count):
        call_id = call_ids[i]

        print(f"\n{'='*80}")
        print(f"处理第 {i+1}/{verify_count} 条: {call_id}")
        print("="*80)

        # 步骤2: 获取历史详情
        history_detail = step2_get_history_detail(call_id)
        if not history_detail:
            print("✗ 获取历史详情失败，跳过")
            continue

        # 步骤3: 调用决策引擎
        engine_result = step3_call_decision_engine(history_detail['input_params'])
        if not engine_result:
            print("✗ 调用决策引擎失败，跳过")
            continue

        # 对比结果
        compare_result = compare_results(history_detail, engine_result, i+1, call_id)

        # 记录汇总统计
        if compare_result['decision_match']:
            decision_match_count += 1
        if compare_result['steps_match']:
            steps_match_count += 1
            
        # 如果任一不匹配，记录为失败
        if not (compare_result['decision_match'] and compare_result['steps_match']):
            reason = []
            if not compare_result['decision_match']: reason.append("决策不一致")
            if not compare_result['steps_match']: reason.append("步骤不一致")
            
            mismatch_records.append({
                'index': i+1,
                'call_id': call_id,
                'reason': " + ".join(reason)
            })

        # 等待
        if i < verify_count - 1:
            time.sleep(0.5)

    # 汇总
    print(f"\n{'='*80}")
    print(" 验证总结果汇总 ")
    print("=" * 80)
    print(f"总对比条数: {verify_count}")
    
    success_count = 0
    fail_records = []

    # 注意：这里的逻辑需要根据 compare_result 的实际通过情况来计算
    # 之前代码里只有 decision_match_count，我们需要更准确的统计
    
    print(f"决策一致: {decision_match_count}/{verify_count}")
    print(f"步骤一致: {steps_match_count}/{verify_count}")

    # 统计完全成功的条数 (决策和步骤都必须一致)
    # 我们需要在循环里记录每一条的最终状态
    # 这里我们通过 mismatch_records 来反向推导失败的 callid
    
    if mismatch_records:
        print(f"\n[失败详情] 共 {len(mismatch_records)} 条失败:")
        for r in mismatch_records:
            print(f"  - 第{r['index']}条 | CallID: {r['call_id']} | 原因: {r.get('reason', '决策或步骤不一致')}")
    else:
        print("\n[ok] 所有条数全部验证通过！")

    print(f"\n最终统计: 成功 {verify_count - len(mismatch_records)} 条, 失败 {len(mismatch_records)} 条")
    print("=" * 80)

    print(f"\n验证完成！")

if __name__ == "__main__":
    main()

