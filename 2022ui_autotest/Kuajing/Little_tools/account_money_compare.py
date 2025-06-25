import requests

url = 'https://fat-global-ad.baofu.com/ams-api/cross-border-rmb/user-info/account/5181240821000008798'

headers = {
    'Host': 'fat-global-ad.baofu.com',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua-platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'request-system-name': 'baofu-admin-control-client',
    'sec-ch-ua-mobile': '?0',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://fat-global-ad.baofu.com/account/ams/main/global-merchant-management/merchant-management/org-hk-detail/5181240821000008798/5182240821000008968',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'Hm_lvt_4481d82590bdc2a34bde3cde07f3ef59=1743038110; HMACCOUNT=5E1725190556B2EC; Hm_lpvt_4481d82590bdc2a34bde3cde07f3ef59=1743038115; agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NDMxMjY5NTN9.a5osZuw7KSEOatAuqfU-vGrPvZtN-Wh1XuR2G6Ew-j4oiKL4a5I4X5IQcWsyNHK6qWGAmBZN8Ev9QGWggPOcpw'
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        allow_redirects=False  # 根据实际情况调整是否允许重定向
    )

    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for k, v in response.headers.items():
        print(f"{k}: {v}")
    print("\nResponse Body:")
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {str(e)}")