import time
import requests
import json
import os
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# ========== 全局 token 缓存 ==========
_token_cache = {
    "token": None,
    "env": None,
    "last_login_time": None,
    "max_age": 60 * 60
}

# 缓存文件路径
CACHE_FILE = os.path.join(os.path.dirname(__file__), '.token_cache.json')

def _load_token_cache():
    """从文件加载缓存的token"""
    global _token_cache
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cached_data = json.load(f)
                # 验证缓存数据的有效性
                if all(key in cached_data for key in ["token", "env", "last_login_time", "max_age"]):
                    _token_cache = cached_data
                    log(f"[INFO] 从文件加载缓存的token，环境: {_token_cache['env']}")
    except Exception as e:
        log(f"[ERROR] 加载token缓存失败: {e}")

def _save_token_cache():
    """将token缓存保存到文件"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(_token_cache, f)
        log(f"[INFO] Token缓存已保存到文件: {CACHE_FILE}")
    except Exception as e:
        log(f"[ERROR] 保存token缓存失败: {e}")

# 在模块加载时加载缓存
_load_token_cache()

def _is_token_expired():
    if not _token_cache["token"]:
        return True
    if _token_cache["last_login_time"] is None:
        return True
    return (time.time() - _token_cache["last_login_time"]) > _token_cache["max_age"]

def login(env="fat", login_no="13166210870", password="uKXPzIcL55uI1IUq0yGrMw=="):
    base_url = {
        "fat": "https://fat-global-ad.baofu.com",
        "uat": "https://uat-global-ad.baofu.com"
    }
    url = f"{base_url.get(env)}/oms-roleApi/login"
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
    }
    payload = {
        "loginNo": login_no,
        "password": password,
        "picCode": ""
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                _token_cache["token"] = data["token"]
                _token_cache["env"] = env
                _token_cache["last_login_time"] = time.time()
                # 保存到文件
                _save_token_cache()
                log(f"🎉 [INFO] {env}环境 - 登录成功，获取新 token")
                return data["token"]
            else:
                log("[ERROR] 登录成功但未返回 token")
                return None
        else:
            log(f"[ERROR] 登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        log(f"[ERROR] 请求登录接口异常: {e}")
        return None

def query_redis_key(redis_key, env="fat", max_retries=1):
    """
    查询redis key对应的value
    :param redis_key: redis key
    :param env: 环境，如 "fat", "uat"
    :param max_retries: 最大重试次数（不含首次）
    :return: Response or None
    """
    global _token_cache

    session = requests.Session()
    session.verify = False

    url = f"https://{env}-global-ad.baofu.com/ams-api/cache/redis/query"

    data = {
        "redisKey": redis_key
    }

    log(f"[INFO] 查询Redis key: {redis_key}")
    
    for attempt in range(max_retries + 1):
        if _token_cache["env"] != env or _is_token_expired():
            log(f"[INFO] Token 缓存失效，重新登录...")
            token = login(env=env)
            if not token:
                log("[FATAL] 登录失败，终止请求")
                return None
        else:
            token = _token_cache["token"]
            log(f"[INFO] 使用缓存中的 token")

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": f"https://{env}-global-ad.baofu.com",
            "Referer": f"https://{env}-global-ad.baofu.com/payful/new/account/ams/main/global-sys-management/redis-cache",
            "Cookie": f"agent-control-core-token={token}",
        }

        try:
            log(f"[INFO] 发送请求到 {url} (attempt {attempt + 1})")
            response = session.post(url, headers=headers, json=data)

            log(f"Status Code: {response.status_code}")
            try:
                resp_json = response.json()
                # log(f"Response JSON: {resp_json}")

                if response.status_code != 401:
                    # 解析响应数据
                    if "result" in resp_json:
                        try:
                            # 解析result字段中的JSON字符串
                            result_json = json.loads(resp_json["result"])
                            # 提取需要的字段
                            user_name = result_json.get("userName", "")
                            operator_id = result_json.get("operatorId", "")
                            free_login_expire_time = result_json.get("freeLoginExpireTime")
                            
                            # 格式化freeLoginExpireTime为指定格式
                            if free_login_expire_time:
                                # 转换为时间对象
                                expire_time = time.localtime(free_login_expire_time)
                                # 格式化为2026-4-20 14:00:00格式
                                formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", expire_time)
                            else:
                                formatted_time = ""
                            
                            # 只打印这三个字段
                            log(f"✅ userName: {user_name}")
                            log(f"✅ operatorId: {operator_id}")
                            log(f"✅ freeLoginExpireTime: {free_login_expire_time}({formatted_time})")
                        except Exception as e:
                            log(f"[ERROR] 解析result字段失败: {e}")
                    return response

                if response.status_code == 401 and attempt < max_retries:
                    log("[WARNING] 401 Unauthorized，尝试重新登录...")
                    _token_cache["token"] = None
                    continue
                else:
                    return response
            except Exception as e:
                log(f"Error parsing JSON: {e}")
                log(f"Response Text: {response.text}")
                return response

        except Exception as e:
            log(f"[ERROR] 请求异常: {e}")
            return None

    return None

def edit_redis_value(redis_key, redis_value=None, env="fat", max_retries=1, new_time=None):
    """
    修改redis key的value
    :param redis_key: redis key
    :param redis_value: redis value
    :param env: 环境，如 "fat", "uat"
    :param max_retries: 最大重试次数（不含首次）
    :param new_time: 新的过期时间，格式如 "5min", "1min", "7days"
    :return: Response or None
    """
    # 如果提供了new_time参数，需要先查询当前值并更新freeLoginExpireTime
    if new_time:
        # 先查询当前的redis value
        response = query_redis_key(redis_key, env=env, max_retries=max_retries)
        if response:
            try:
                resp_json = response.json()
                if "result" in resp_json:
                    # 解析result字段中的JSON字符串
                    result_json = json.loads(resp_json["result"])
                    # 获取当前的freeLoginExpireTime
                    current_expire_time = result_json.get("freeLoginExpireTime")
                    if current_expire_time:
                        # 计算新的过期时间
                        # 解析new_time参数
                        import re
                        match = re.match(r'(\d+)([a-zA-Z]+)', new_time)
                        if match:
                            amount = int(match.group(1))
                            unit = match.group(2).lower()
                            
                            # 计算时间增量（秒）
                            if unit == "min":
                                delta = amount * 60
                            elif unit == "hours":
                                delta = amount * 3600
                            elif unit == "days":
                                delta = amount * 86400
                            else:
                                log(f"[ERROR] 不支持的时间单位: {unit}")
                                return None
                            
                            # 计算新的过期时间戳（基于当前时间）
                            new_expire_time = int(time.time()) + delta
                            
                            # 更新result_json中的freeLoginExpireTime
                            result_json["freeLoginExpireTime"] = new_expire_time
                            
                            # 重新生成redis_value
                            redis_value = json.dumps(result_json)
                            
                            # 格式化时间
                            current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_expire_time))
                            new_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_expire_time))
                            
                            # 打印更换前后的时间
                            log(f"🚀 更换前的时间戳{current_expire_time}({current_time_str}) --更换后的时间戳{new_expire_time}({new_time_str})")
                        else:
                            log(f"[ERROR] 无效的new_time格式: {new_time}")
                            return None
                    else:
                        log("[ERROR] 当前Redis值中没有freeLoginExpireTime字段")
                        return None
            except Exception as e:
                log(f"[ERROR] 处理new_time参数失败: {e}")
                return None
        else:
            log("[ERROR] 查询Redis key失败")
            return None
    
    # 如果没有提供redis_value且没有new_time参数，返回错误
    if not redis_value:
        log("[ERROR] 必须提供redis_value或new_time参数")
        return None
    global _token_cache

    session = requests.Session()
    session.verify = False

    url = f"https://{env}-global-ad.baofu.com/ams-api/cache/redis/edit"

    data = {
        "redisKey": redis_key,
        "redisValue": redis_value
    }

    log(f"[INFO] 修改Redis key: {redis_key}")
    
    for attempt in range(max_retries + 1):
        if _token_cache["env"] != env or _is_token_expired():
            log(f"[INFO] Token 缓存失效，重新登录...")
            token = login(env=env)
            if not token:
                log("[FATAL] 登录失败，终止请求")
                return None
        else:
            token = _token_cache["token"]
            log(f"[INFO] 使用缓存中的 token")

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": f"https://{env}-global-ad.baofu.com",
            "Referer": f"https://{env}-global-ad.baofu.com/payful/new/account/ams/main/global-sys-management/redis-cache",
            "Cookie": f"agent-control-core-token={token}",
        }

        try:
            log(f"[INFO] 发送请求到 {url} (attempt {attempt + 1})")
            response = session.post(url, headers=headers, json=data)

            log(f"Status Code: {response.status_code}")
            try:
                resp_json = response.json()
                log(f"Response JSON: {resp_json}")

                if response.status_code != 401:
                    return response

                if response.status_code == 401 and attempt < max_retries:
                    log("[WARNING] 401 Unauthorized，尝试重新登录...")
                    _token_cache["token"] = None
                    continue
                else:
                    return response
            except Exception as e:
                log(f"Error parsing JSON: {e}")
                log(f"Response Text: {response.text}")
                return response

        except Exception as e:
            log(f"[ERROR] 请求异常: {e}")
            return None

    return None

if __name__ == '__main__':
    pass
    # 示例：查询redis key  # 五五
    query_redis_key("B:I:GLOGIN_TOKEN:GEP-B2B-MINI:5183240821000008828", env="fat")  
    
    
    
    # 示例：使用new_time参数修改过期时间（5分钟后）
    # edit_redis_value("B:I:GLOGIN_TOKEN:GEP-B2B-MINI:5183240821000008828", env="fat", new_time="1min")

    # 桐乡-fat
    query_redis_key("B:I:GLOGIN_TOKEN:GEP-B2B-MINI:5183240628000024278", env="fat")  
    # edit_redis_value("B:I:GLOGIN_TOKEN:GEP-B2B-MINI:5183240628000024278", env="fat", new_time="1min")
