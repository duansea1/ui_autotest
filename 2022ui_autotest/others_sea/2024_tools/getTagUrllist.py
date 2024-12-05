# -*- coding: utf-8 -*-
import os
import json
import requests

# 定义请求头
headers = {
    'authority': 'www.pixiv.net',
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'baggage': 'sentry-environment=production,sentry-release=ea6e64bc6ad7014a729d5fac5542f6d2ed64097c,sentry-public_key=7b15ebdd9cf64efb88cfab93783df02a,sentry-trace_id=ef692ebc5d194f9fb01d56a71eaab0b7,sentry-sample_rate=0.0001',
    'cache-control': 'no-cache',
    'cookie': 'first_visit_datetime_pc=2023-10-07%2022%3A27%3A22; p_ab_id=9; p_ab_id_2=3; p_ab_d_id=1834251666; yuid_b=FVFYgUk; _ga=GA1.1.176800063.1696685292; privacy_policy_agreement=6; c_type=30; privacy_policy_notification=0; a_type=0; b_type=1; login_ever=yes; _gcl_au=1.1.2039394013.1710328760; cc1=2024-04-22%2019%3A14%3A32; cf_clearance=OGIdfmpkB.9P.hvjX4k1cIyC409FVRXFnvn78sRd2bE-1713780873-1.0.1.1-Ot7WKrEWL3cM6wYxvsCOWqHfFUadX05lAMCDGHfUf.1imx2mkXfPcVpEKLuCVpKLYEv9vVSYLWWc.Df250m_DA; _ga_MZ1NL4PHH0=GS1.1.1713781131.4.0.1713781135.0.0.0; PHPSESSID=41531366_cGM8ty3M9ijhxr8DYM8LTAULDGZZhYZL; device_token=b11ee4d1b00852fa4a577bde29cfe0c1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _im_vid=01HW2N20P1CNCV32GMETN57SSK; __cf_bm=EbxGAzJys.CCg_.Ch9Qeo7pCSUA_ReYTY4vLEcKctmk-1713836529-1.0.1.1-bqCjYE2Qi4kKqvfnbcWm71URQ5HvuSm_wiLKsp5s2Lnji_EZ7PMD_BmBVSXCZAUkKLhYHdi2Mp2wNYgEctRED3R4T6.fz_YpNph1NGZyYxs; _ga_75BBYNYN9J=GS1.1.1713836529.7.1.1713836658.0.0.0',  # 替换为你的cookie
    'pragma': 'no-cache',
    'referer': 'https://www.pixiv.net/tags/%E5%8F%A4%E9%A3%8E/artworks?mode=safe&s_mode=s_tag',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'ef692ebc5d194f9fb01d56a71eaab0b7-9baefdce5e3c804f-0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'x-user-id': '41531366'
}

# 请求数据
response = requests.get('https://www.pixiv.net/ajax/search/artworks/%E5%8F%A4%E9%A3%8E?word=%E5%8F%A4%E9%A3%8E&order=date_d、&p=5&s_mode=s_tag&type=all&lang=zh&version=5e572d415bb6d72cfe717e676a56edc2b0a52286', headers=headers, verify=False)

# 解析JSON响应
data = response.json()

# 设置保存路径
save_path = '/Users/victor9395/Downloads/redditImg/'  # 替换为实际的保存路径

# 提取URL并下载/保存图片
if 'body' in data and 'illustManga' in data['body']:
    illust_manga_data = data['body']['illustManga']['data']
    for item in illust_manga_data:
        image_url = item['url']

        # 生成 p0~p5 的链接并保存对应图片
        for i in range(6):
            # 构造完整的图片URL
            modified_url = image_url.replace('c/250x250_80_a2/', '').replace('_p0_', f'_p{i}_')

            # 发送HTTP请求下载图片
            image_response = requests.get(modified_url, headers=headers)

            # 提取文件名
            filename = modified_url.rsplit('/', 1)[-1]

            # 设置保存文件路径
            save_file_path = os.path.join(save_path, filename)

            # 写入图片到文件
            with open(save_file_path, 'wb') as f:
                f.write(image_response.content)

            print(f"图片({filename})保存成功！")
            print("图片链接："+modified_url)
            print("==============>>>>>next>>>>>")

        # 恢复原始的图片URL，为下一次循环做准备
        image_url = item['url']

