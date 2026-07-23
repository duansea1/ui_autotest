import requests

URL = "https://ai-api.baoyun.com/v1/chat/completions"

# 免费KEY
FREE_KEY = "sk-oD3G9AYg7OQkOwcZOeQlQNp7TmWo2tijLnp2LXfcVkjRBBQC"
FREE_MODEL = "glm-5.2"

# 付费KEY
PAID_KEY = "sk-mulzHCMB8KoFwvwjuc90uBk9Hz1SlgGKvT4wnvefYaBc9B53"
PAID_MODEL = "deepseek-v4-pro"


def do_test(name, key, model):
    print(f"[{name}] KEY={key[:16]}...{key[-4:]}  模型={model}")
    try:
        r = requests.post(
            URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": "Hello!"}]},
            timeout=30,
            proxies={"http": None, "https": None},  # 不走代理
        )
        print(f"  状态码: {r.status_code}")
        if r.status_code == 200:
            print(f"  回复  : {r.json()['choices'][0]['message']['content']}")
            print(f"  => 通过")
        else:
            print(f"  响应  : {r.text[:200]}")
            print(f"  => 失败")
    except Exception as e:
        print(f"  异常  : {e}")
        print(f"  => 失败")


print("宝云AI API 测试")
print(f"地址: {URL}\n")

do_test("免费KEY", FREE_KEY, FREE_MODEL)
print()
# do_test("付费KEY", PAID_KEY, PAID_MODEL)
