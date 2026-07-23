# -*- coding: utf-8 -*-
"""
测试宝云AI API各模型的可用性
"""

import requests
import time
import urllib3

# 禁用SSL警告（宝云API使用自签名证书）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API配置
URL = "https://ai-api.baoyun.com/v1/chat/completions"
API_KEY = "sk-oD3G9AYg7OQkOwcZOeQlQNp7TmWo2tijLnp2LXfcVkjRBBQC"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
# 
# 可用的模型 (3/8):
#   [OK] gemini-3.1-pro-preview
#   [OK] Qwen/Qwen3-Coder
#   [OK] glm-5.1
# 待测试的模型列表
MODELS = [
    "deepseek-v4-pro",
    
]

TEST_MESSAGE = "Hello! 请用中文回复：你好，介绍一下你自己。"


def test_model(model_name: str) -> dict:
    """测试单个模型是否可用"""
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": TEST_MESSAGE}
        ],
    }

    try:
        resp = requests.post(
            URL,
            headers=HEADERS,
            json=data,
            timeout=60,
            proxies={"http": None, "https": None},
            verify=False,
        )
        result = resp.json()
        return {
            "model": model_name,
            "status_code": resp.status_code,
            "success": resp.status_code == 200,
            "response": result,
        }
    except requests.exceptions.Timeout:
        return {
            "model": model_name,
            "status_code": None,
            "success": False,
            "response": "请求超时",
        }
    except Exception as e:
        return {
            "model": model_name,
            "status_code": None,
            "success": False,
            "response": str(e),
        }


def main():
    print("=" * 60)
    print("宝云AI API 模型可用性测试")
    print("=" * 60)

    results = []

    for i, model in enumerate(MODELS, 1):
        print(f"\n[{i}/{len(MODELS)}] 测试模型: {model}")
        print("-" * 40)

        result = test_model(model)

        if result["success"]:
            resp_data = result["response"]
            # 尝试提取回复内容
            try:
                content = resp_data["choices"][0]["message"]["content"]
                # 截取前200字符显示
                display_content = content[:200] + "..." if len(content) > 200 else content
                print(f"  [OK] 状态: 可用")
                print(f"  模型: {resp_data.get('model', 'N/A')}")
                print(f"  回复: {display_content}")
            except (KeyError, IndexError):
                print(f"  [OK] 状态: 可用 (HTTP 200)")
                print(f"  原始响应: {resp_data}")
        else:
            print(f"  [FAIL] 状态: 不可用")
            print(f"  HTTP状态码: {result['status_code']}")
            print(f"  响应: {result['response']}")

        results.append(result)

        # 避免请求过于频繁
        if i < len(MODELS):
            time.sleep(1)

    # 汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    available = [r["model"] for r in results if r["success"]]
    unavailable = [r["model"] for r in results if not r["success"]]

    print(f"可用的模型 ({len(available)}/{len(MODELS)}):")
    for m in available:
        print(f"  [OK] {m}")

    if unavailable:
        print(f"\n不可用的模型 ({len(unavailable)}/{len(MODELS)}):")
        for m in unavailable:
            print(f"  [FAIL] {m}")
    else:
        print("\n所有模型均可正常使用!")


if __name__ == "__main__":
    main()
