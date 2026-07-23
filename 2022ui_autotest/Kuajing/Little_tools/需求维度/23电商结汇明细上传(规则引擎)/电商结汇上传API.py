import requests
import pandas as pd
import os
import json
import time
import random

# 抑制SSL警告
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class ECommerceSettlementUpload:
    def __init__(self):
        # 公共Cookie
        self.cookie ="BF-INTERNATIONAL-MEMBER-TOKEN=3eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiI1MTgzMjQwODIzMDAwMDAwMjA4IiwiaWF0IjoxNzcwMjcyMjg2fQ.pp0aikeb7fATj7ZWuTsnjyOdXKmnAhBcrLgyX5BRmTS1JXKsONIb3mUWACraCnaISIix6HNJXqAHkBpxlzDZcg; hinasdk_crossdata=%7B%22accountId%22%3A%225181240823000000178%22%2C%22deviceId%22%3A%22f88719e3-804c-45ee-b146-1dd767ff7018%22%2C%22anonymousId%22%3A%22f88719e3-804c-45ee-b146-1dd767ff7018%22%2C%22sessionId%22%3A%221770272273460_408010%22%2C%22firstVisitTime%22%3A1770272273203%2C%22props%22%3A%7B%22H_latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22H_latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22H_latest_referrer%22%3A%22%22%7D%7D"




        # 模板文件路径
        self.template_path = r"c:\Users\段海洋\myfiles\auto_files\ui_autotest\2022ui_autotest\Kuajing\Little_tools\需求维度\23电商结汇明细上传\custom-电商收款-通用--一列1个商品-EUR.xlsx"
        
        # 输出文件路径
        self.output_dir = r"c:\Users\段海洋\myfiles\auto_files\ui_autotest\2022ui_autotest\Kuajing\Little_tools\需求维度\23电商结汇明细上传"
        
        # 接口URLs
        self.upload_file_url = "https://fat-member.gepholding.com/api/common/file/upload"
        self.upload_detail_url = "https://fat-member.gepholding.com/api/upload-detail/upload"
        self.upload_check_url = "https://fat-member.gepholding.com/api/upload-detail/upload-loop-check/{}"

    def create_custom_excel(self, custom_data, file_name):
        """
        智能生成/更新Excel文件：
        - 如果文件不存在：基于模板创建（标题行 + 表头行 + 数据行）
        - 如果文件已存在：保留前两行，仅更新第3行数据
        """
        output_path = os.path.join(self.output_dir, file_name)
        os.makedirs(self.output_dir, exist_ok=True)

        num_cols = None
        title_row = None
        header_row = None

        # === 步骤1：确定标题行和表头行 ===
        if os.path.exists(output_path):
            # 文件存在：读取前两行
            try:
                existing_df = pd.read_excel(output_path, header=None)
                if len(existing_df) >= 2:
                    title_row = existing_df.iloc[0].fillna("").tolist()
                    header_row = existing_df.iloc[1].fillna("").tolist()
                else:
                    raise ValueError("现有文件行数不足")
            except Exception:
                # 回退到模板
                template_meta = pd.read_excel(self.template_path, header=None, nrows=2)
                title_row = template_meta.iloc[0].fillna("").tolist()
                header_row = template_meta.iloc[1].fillna("").tolist()
        else:
            # 文件不存在：从模板读取前两行
            template_meta = pd.read_excel(self.template_path, header=None, nrows=2)
            title_row = template_meta.iloc[0].fillna("").tolist()
            header_row = template_meta.iloc[1].fillna("").tolist()

        num_cols = len(header_row)

        # === 步骤2：构造新数据行 ===
        data_row = [""] * num_cols
        for col_index, value in custom_data.items():
            if isinstance(col_index, int) and 0 <= col_index < num_cols:
                data_row[col_index] = value
            else:
                print(f"⚠️ 列索引 {col_index} 超出范围（总列数: {num_cols}），已跳过")

        # === 步骤3：组装完整数据 ===
        if os.path.exists(output_path):
            # 读取现有全部内容
            full_df = pd.read_excel(output_path, header=None)
            # 确保至少有3行
            while len(full_df) < 3:
                full_df.loc[len(full_df)] = [""] * num_cols
            # 替换第3行（索引2）
            full_df.iloc[2] = data_row
        else:
            # 新建：标题 + 表头 + 数据
            full_df = pd.DataFrame([title_row, header_row, data_row])

        # === 步骤4：写回文件 ===
        try:
            full_df.to_excel(output_path, index=False, header=False)
            action = "更新" if os.path.exists(output_path) else "创建"
            print(f"✅ 文件{action}成功: {output_path}")
            return output_path
        except PermissionError:
            # 权限错误：保存为带时间戳的新文件
            fallback_name = f"{os.path.splitext(file_name)[0]}_{int(time.time())}.xlsx"
            fallback_path = os.path.join(self.output_dir, fallback_name)
            full_df.to_excel(fallback_path, index=False, header=False)
            print(f"⚠️ 原文件被占用，已保存到: {fallback_path}")
            return fallback_path

    def upload_file(self, file_path):
        headers = {
            'request-system-name': 'member-exchange-client',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookie
        }
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            }
            data = {
                'type': 'file',
                'businessType': 'STORE_ORDER_FILE',
                'uploadType': 'excel'
            }

            print(f"\n" + "-"*60)
            print(f"🚀 第一个接口(上传接口)：开始调用文件上传接口")
            print(f"-"*60)
            print(f"🔍 请求URL: {self.upload_file_url}")
            print(f"📝 请求参数:")
            print(f"   - 文件名称: {os.path.basename(file_path)}")
            print(f"   - type: {data['type']}")
            print(f"   - businessType: {data['businessType']}")
            print(f"   - uploadType: {data['uploadType']}")

            response = requests.post(self.upload_file_url, headers=headers, files=files, data=data, verify=False)

        print(f"📋 响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"📊 响应数据:")
            print(f"   {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('code') == '0':
                file_id = result.get('result', {}).get('fileId')
                print(f"🎉 第一个接口(上传接口)调用成功！")
                print(f"   ✅ fileId: {file_id}")
                return file_id
            else:
                print(f"⚠️ 第一个接口(上传接口)调用失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 第一个接口(上传接口)请求失败，状态码: {response.status_code}")
            return None

    def upload_detail(self, file_id, file_name):
        if not file_id:
            print(f"❌ 第二个接口：缺少必要参数file_id，无法执行上传详情接口")
            return None
        headers = {
            'Accept-Language': 'zh-CN',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': self.cookie
        }
        payload = {
            "fileId": file_id,
            "fileName": file_name,
            "fileType": "0",
            "storePlatform": "TIKTOK-USD",
            "storeId": "",
            "industryType": "01"
        }

        print(f"\n" + "-"*60)
        print(f"🚀 第二个接口：开始调用上传详情接口")
        print(f"-"*60)
        print(f"🔍 请求URL: {self.upload_detail_url}")
        print(f"📝 请求参数:")
        print(f"   {json.dumps(payload, ensure_ascii=False, indent=2)}")

        response = requests.post(self.upload_detail_url, headers=headers, json=payload, verify=False)

        print(f"📋 响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"📊 响应数据:")
            print(f"   {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('code') == '0':
                check_id = result.get('result')
                print(f"🎉 第二个接口调用成功！")
                print(f"   ✅ check_id: {check_id}")
                return check_id
            else:
                print(f"⚠️ 第二个接口调用失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 第二个接口请求失败，状态码: {response.status_code}")
            return None

    def upload_check(self, check_id):
        if not check_id:
            print(f"❌ 第三个接口：缺少必要参数check_id，无法执行上传检查接口")
            return None
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cookie': self.cookie
        }
        url = self.upload_check_url.format(check_id)
        print(f"\n" + "-"*60)
        print(f"🚀 第三个接口：开始调用上传检查接口")
        print(f"-"*60)
        print(f"🔍 请求URL: {url}")
        print(f"📝 请求参数:")
        print(f"   - check_id: {check_id}")

        response = requests.get(url, headers=headers, verify=False)

        print(f"📋 响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"📊 响应数据:")
            print(f"   {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('code') == '0':
                check_result = result.get('result')
                print(f"🎉 第三个接口调用成功！")
                if isinstance(check_result, dict):
                    file_id = check_result.get('fileId')
                    file_url = check_result.get('fileUrl')
                    if file_id == '0' and file_url == '0':
                        print(f"⚠️ 注意：上传的文件内容可能存在问题，fileId和fileUrl都为0")
                return check_result
            else:
                print(f"⚠️ 第三个接口调用失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 第三个接口请求失败，状态码: {response.status_code}")
            return None

    def run(self, custom_data, file_name):
        print(f"\n📄 开始创建/更新Excel文件")
        excel_file_path = self.create_custom_excel(custom_data, file_name)

        print(f"\n" + "="*50)
        print(f"📌 开始执行第一个接口(上传接口)")
        print(f"="*50)
        file_id = self.upload_file(excel_file_path)
        if not file_id:
            print(f"\n❌ 第一个接口(上传接口)调用失败，无法继续执行后续接口")
            return None

        print(f"\n" + "="*50)
        print(f"📌 开始执行第二个接口")
        print(f"="*50)
        check_id = self.upload_detail(file_id, file_name)
        if not check_id:
            print(f"\n❌ 第二个接口调用失败，无法继续执行后续接口")
            return None

        print(f"\n" + "="*50)
        print(f"📌 开始执行第三个接口")
        print(f"="*50)
        print(f"⏳ 等待上传检查结果...")
        final_result = self.upload_check(check_id)

        return final_result



def generate_order_and_tracking():
    # 获取当前日期时间前缀（20260126）
    date_prefix = time.strftime("%Y%m%d", time.localtime())  # → '20260126'
    
    # 订单号：20260126 + HHMM + 4位随机数（总16位）
    time_part = time.strftime("%H%M", time.localtime())
    order_suffix = f"{random.randint(0, 9999):04d}"
    order_no = date_prefix + time_part + order_suffix
    
    # 物流单号：20260126 + 5位随机数（总13位）
    tracking_suffix = f"{random.randint(0, 99999):05d}"
    tracking_no = date_prefix + tracking_suffix
    
    return order_no, tracking_no


if __name__ == "__main__":
    uploader = ECommerceSettlementUpload()
    order_no, tracking_no = generate_order_and_tracking()

    custom_data1 = {
    0: "more20260203032",      # 订单号*
    1: "2026-01-26 10:00:00",  # 交易时间（YYYY-MM-DD HH:MM:SS）*
    2: "USD",                   # 交易币种*
    3: "20000",                    # 交易金额*
    4: "002",                   # 商品类型编码*（002=手机/数码）
    5: "delllatitude牌电脑;mac iphone19X-COMPUTER;DELL C200;hauweiMate70+;雪花秀商品;LV bag",               # 商品名称*
    6: "2;2;20;20;10;1",                     # 商品数量*
    7: "1500;2000;100;50;500;5000",                    # 商品单价*
    8: "",                      # 支付人所在国家代码
    9: "",                      # 支付人姓名
    10: "",                     # 支付人证件号
    11: "ems",                  # 物流公司编码*
    12: "ems202601290005",                 # 物流单号*
    13: "",                     # 收货人姓名
    14: "",                     # 收货人联系方式
    15: "",                     # 收货人地址
    16: "2026-01-11"           # 发货日期（YYYY-MM-DD）
}

    # 单个商品
    custom_data = {
    0: "only20260204005",      # 订单号*
    1: "2026-01-26 10:00:00",  # 交易时间（YYYY-MM-DD HH:MM:SS）*
    2: "PLN",                   # 交易币种*
    3: "2.24",                    # 交易金额*
    4: "002",                   # 商品类型编码*（002=手机/数码）
    5: "ショップジャパン-商品名称bag",               # 商品名称*
    6: "1",                     # 商品数量*
    7: "2.24",                    # 商品单价*
    8: "",                      # 支付人所在国家代码
    9: "",                      # 支付人姓名
    10: "",                     # 支付人证件号
    11: "ems",                  # 物流公司编码*
    12: "ems2026012900051",                 # 物流单号*
    13: "",                     # 收货人姓名
    14: "",                     # 收货人联系方式
    15: "",                     # 收货人地址
    16: "2026-01-12"           # 发货日期（YYYY-MM-DD）
}

    custom_data1 = {
    0: "more2026002030042",      # 订单号*
    1: "2026-01-26 10:00:00",  # 交易时间*
    2: "USD",                   # 交易币种*
    3: "48760",                 # ← 自动生成的总交易金额（见下方计算）
    4: "002",                   # 商品类型编码（统一为数码类，或可细分）
    5: (
        "Dell Latitude 7440 Laptop;"
        "Apple iPhone 19 Pro Max;"
        "Samsung Galaxy S26 Ultra;"
        "Sony WH-1000XM6 Headphones;"
        "Apple MacBook Pro M4;"
        "Canon EOS R8 Camera;"
        "DJI Mini 4 Pro Drone;"
        "iPad Air 6;"
        "Apple Watch Series 10;"
        "Bose QuietComfort Ultra;"
        "LG OLED C4 65\" TV;"
        "Nintendo Switch OLED;"
        "GoPro HERO13 Black;"
        "Microsoft Surface Pro 10;"
        "Anker 737 Power Bank;"
        "Logitech MX Master 3S;"
        "Razer Blade 16 Gaming Laptop;"
        "Kindle Paperwhite 2026;"
        "Fitbit Charge 6;"
        "JBL Flip 6 Speaker;"
        "Huawei MatePad Pro;"
        "Garmin Fenix 8;"
        "Meta Quest 3 VR Headset;"
        "Samsung T7 Shield 4TB SSD;"
        "Apple AirPods Pro (2026)"
    ),  # 商品名称*（25项，用分号分隔）
    6: (
        "1;1;1;2;1;1;1;2;3;2;"
        "1;1;1;1;3;2;1;2;2;3;"
        "1;1;1;2;2"
    ),  # 商品数量*（25项）
    7: (
        "2200;1500;1300;400;2500;1800;1200;600;450;350;"
        "2800;350;450;1600;120;100;3200;180;200;150;"
        "700;650;500;180;280"
    ),  # 商品单价*（25项，单位：USD）
    8: "",   # 支付人国家
    9: "",   # 支付人姓名
    10: "",  # 支付人证件号
    11: "ems",
    12: "ems202601290005",
    13: "",
    14: "",
    15: "",
    16: "2026-01-11"
}

    # ✅ 关键修正：使用与模板完全一致的文件名
    output_file_name = os.path.basename(uploader.template_path)

    print("\n" + "="*50)
    print("🚀 电商结汇明细上传流程启动")
    print("="*50)

    result = uploader.run(custom_data, output_file_name)

    print("\n" + "="*50)
    if result:
        is_actual_success = True
        if isinstance(result, dict):
            file_id = result.get('fileId')
            file_url = result.get('fileUrl')
            if file_id == '0' and file_url == '0':
                is_actual_success = False
                print("⚠️ 电商结汇明细上传流程执行完成，但文件内容存在问题！")
            else:
                print("🎉 电商结汇明细上传流程执行成功！")
        else:
            print("🎉 电商结汇明细上传流程执行成功！")

        print(f"📊 最终结果:")
        print(f"   {json.dumps(result, ensure_ascii=False, indent=2)}")

        if not is_actual_success:
            print(f"\n💡 提示：fileId和fileUrl都为0，可能是因为上传的文件内容不符合要求")
    else:
        print("❌ 电商结汇明细上传流程执行失败！")
    print("="*50)

    print(f"-------------订单号: {order_no}")
    