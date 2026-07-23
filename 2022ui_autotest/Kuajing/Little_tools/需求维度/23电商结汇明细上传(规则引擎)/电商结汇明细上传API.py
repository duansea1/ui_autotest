import requests
import pandas as pd
import os
import json
import time

# 抑制SSL警告
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ECommerceSettlementUpload:
    def __init__(self):
        # 公共Cookie
        self.cookie = "BF-INTERNATIONAL-MEMBER-TOKEN=3eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiI1MTgzMjQwNjI4MDAwMDI0Mjc4IiwiaWF0IjoxNzY5NDE5NDI0fQ.Zxer8LvgbG5PwF6kMr1sBKb_XKlBIdOnPks7UtKiiyBeDBYuMxM0o447NDSgKrOh_Yn3kxY4vuPAG4dTvckfFA; hinasdk_crossdata=%7B%22accountId%22%3Anull%2C%22deviceId%22%3A%2242f4f6d5-901e-4fcc-9c4c-f7a032014cb3%22%2C%22anonymousId%22%3A%2242f4f6d5-901e-4fcc-9c4c-f7a032014cb3%22%2C%22sessionId%22%3A%22%22%2C%22firstVisitTime%22%3A1768788087591%2C%22props%22%3A%7B%22H_latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22H_latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22H_latest_referrer%22%3A%22%22%7D%7D"
        
        # 模板文件路径
        self.template_path = r"c:\Users\段海洋\myfiles\auto_files\ui_autotest\2022ui_autotest\Kuajing\Little_tools\需求维度\23电商结汇明细上传\2026-电商收款-通用--一列1个商品-EUR.xlsx"
        
        # 输出文件路径
        self.output_dir = r"c:\Users\段海洋\myfiles\auto_files\ui_autotest\2022ui_autotest\Kuajing\Little_tools\需求维度\23电商结汇明细上传"
        
        # 接口URLs
        self.upload_file_url = "https://fat-member.gepholding.com/api/common/file/upload"
        self.upload_detail_url = "https://fat-member.gepholding.com/api/upload-detail/upload"
        self.upload_check_url = "https://fat-member.gepholding.com/api/upload-detail/upload-loop-check/{}"
    
    def create_custom_excel(self, custom_data, file_name):
        """
        根据自定义数据创建Excel文件
        :param custom_data: 自定义数据字典，key为列索引，value为值
        :param file_name: 输出文件名
        :return: 创建的文件路径
        """
        # 读取模板文件
        df = pd.read_excel(self.template_path)
        
        # 确保至少有一行数据
        if len(df) < 2:
            # 如果只有标题行，添加一行空数据
            df.loc[1] = ["" for _ in range(len(df.columns))]
        
        # 填充自定义数据
        for col_index, value in custom_data.items():
            if col_index < len(df.columns):
                df.iloc[1, col_index] = value
        
        # 输出文件路径
        output_path = os.path.join(self.output_dir, file_name)
        
        # 保存文件
        df.to_excel(output_path, index=False, header=False)
        
        return output_path
    
    def upload_file(self, file_path):
        """
        调用文件上传接口
        :param file_path: 要上传的文件路径
        :return: fileId
        """
        headers = {

            'request-system-name': 'member-exchange-client',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookie
        }
        
        # 构造表单数据
        files = {
            'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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
        """
        调用上传详情接口
        :param file_id: 文件ID
        :param file_name: 文件名
        :return: result值
        """
        # 检查依赖参数
        if not file_id:
            print(f"❌ 第二个接口：缺少必要参数file_id，无法执行上传详情接口")
            return None
        headers = {
            
            'Accept-Language': 'zh-CN',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': self.cookie
        }
        
        # 构造请求体
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
        """
        调用上传检查接口
        :param check_id: 检查ID
        :return: 检查结果
        """
        # 检查依赖参数
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
                
                # 判断文件内容是否有问题
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
        """
        执行完整流程
        :param custom_data: 自定义数据
        :param file_name: 输出文件名
        :return: 最终结果
        """
        # 1. 创建自定义Excel文件
        print(f"\n📄 开始创建自定义Excel文件")
        excel_file_path = self.create_custom_excel(custom_data, file_name)
        print(f"🎉 自定义Excel文件创建成功！")
        print(f"   📁 文件路径: {excel_file_path}")
        
        # 2. 调用文件上传接口
        print(f"\n" + "="*50)
        print(f"📌 开始执行第一个接口(上传接口)")
        print(f"="*50)
        file_id = self.upload_file(excel_file_path)
        if not file_id:
            print(f"\n❌ 第一个接口(上传接口)调用失败，无法继续执行后续接口")
            return None
        
        # 3. 调用上传详情接口
        print(f"\n" + "="*50)
        print(f"📌 开始执行第二个接口")
        print(f"="*50)
        check_id = self.upload_detail(file_id, file_name)
        if not check_id:
            print(f"\n❌ 第二个接口调用失败，无法继续执行后续接口")
            return None
        
        # 4. 调用上传检查接口
        print(f"\n" + "="*50)
        print(f"📌 开始执行第三个接口")
        print(f"="*50)
        print(f"⏳ 等待上传检查结果...")
        final_result = self.upload_check(check_id)
        
        return final_result

if __name__ == "__main__":
    # 初始化实例
    uploader = ECommerceSettlementUpload()
    
    # 自定义数据示例 - 列索引从0开始
    # 根据模板文件结构，第0列是订单号，第1列是交易时间，第2列是店铺名称，以此类推
    custom_data = {
        0: "2026012615150007",  # 订单号
        1: "2025-12-31 15:00:00",  # 交易时间
        2: "测试店铺",  # 店铺名称
        3: "TIKTOK",  # 电商平台
        4: "EUR",  # 币种
        5: "95",  # 订单金额
        6: "5",  # 手续费
        7: "95",  # 实际收款金额
        8: "小米手机",  # 商品名称
        9: "1",  # 商品数量
        10: "95",  # 商品单价
        11: "",  # 物流单号
        12: "",  # 物流费用
        13: "",  # 买家名称
        14: "",  # 买家邮箱
        15: "",  # 收货人地址
        16: "2025-12-31"  # 发货日期
    }
    
    # 输出文件名
    output_file_name = "custom-电商收款-通用--一列1个商品-EUR.xlsx"
    
    # 执行完整流程
    print("\n" + "="*50)
    print("🚀 电商结汇明细上传流程启动")
    print("="*50)
    
    result = uploader.run(custom_data, output_file_name)
    
    print("\n" + "="*50)
    if result:
        # 判断最终结果是否真正成功
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