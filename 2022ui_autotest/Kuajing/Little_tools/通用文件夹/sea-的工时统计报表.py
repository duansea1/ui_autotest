import requests
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import argparse
import urllib3
import requests  # 添加requests库的导入

# ================== 精确配置（与 curl 一致） ==================
BASE_URL = "https://p.baofu.com/plugins/servlet/streams"

# 确保用户名格式正确，使用原始格式保留反斜杠
RAW_USERNAME = r"haiyang\_duan@baofu.com"

REFERER_URL = (
    "https://p.baofu.com/plugins/servlet/gadgets/ifr?"
    "container=atlassian&mid=1&country=CN&lang=zh&view=default"
    "&view-params=%7B%22writable%22%3A%22false%22%7D"
    "&st=atlassian%3AiivyWhIZfxKJBtWMjOHInIA3YYeWAZGoVkM9%2FoK2PY4rjnm9I5s63wld2%2FA5q5oNiSToJeLUED4RJHmArf1NPfyRNj7g665Ip7fJ3fb3Wd3KkscXvVQUWqFBW5Vjpwl5ML6zgK6QxbivM7aQv5qLH1V%2BeqB2VM3vmB1FHaeKnQypj3tgzgT4mb%2FhC7k0heAhjEeZTW%2Bx8GrNUtq8i2BDEnrA4Sk%2Fvag%2F3hvA9eBh5z3DCxPOdW2gyYg3vGvwqz9Z1IQDqrzY6rpp%2BmzC28ZJb%2FLF35dNcMwmf%2BnXE9mv52guWUAxrOmFODYBNQTbDwJbv6%2BL6w%3D%3D"
    "&up_isConfigured=true&up_isReallyConfigured=false"
    "&up_title=__MSG_gadget.activity.stream.title__"
    "&up_titleRequired=false&up_numofentries=10&up_refresh=false"
    "&up_maxProviderLabelCharacters=50&up_rules=&up_renderingContext="
    "&up_keys=&up_itemKeys="
    "&up_username=haiyang%5C_duan%40baofu.com"
    "&url=https%3A%2F%2Fp.baofu.com%2Frest%2Fgadgets%2F1.0%2Fg%2Fcom.atlassian.streams.streams-jira-plugin%2Fgadgets%2Factivitystream-gadget.xml"
    "&libs=auth-refresh"
)

# 更新为用户提供的curl请求中的Cookie值
COOKIE_STR = "atlassian.xsrf.token=BS68-2N0Q-9ZGE-PHY3_b3d84b4518b64c53375c3d87cd0c1208c11e77c2_lin; jira.editor.user.mode=wysiwyg; JSESSIONID=FA3714975B40167C89F51BCB6889318F"



HEADERS = {
    'Host': 'p.baofu.com',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua-platform': '"Windows"',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'Accept': 'application/xml, text/xml, */*; q=0.01',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': REFERER_URL,
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': COOKIE_STR
}

NAMESPACES = {
    'atom': 'http://www.w3.org/2005/Atom',
    'activity': 'http://activitystrea.ms/spec/1.0/'
}


# ================== 工具函数 ==================

def extract_logged_time(title_html, content_html):
    """
    从 title 和 content 中提取工时记录。
    返回 (issue_summary, logged_time_str) 或 None
    """
    # 统一搜索“记录了”，支持多种引号格式和HTML实体编码
    time_match = None
    
    # 首先在title中查找
    if '记录了' in title_html:
        time_match = re.search(r'记录了\s*[“"”]([^“"”]+)[“"”]', title_html)
    
    # 如果在title中没找到，在content中查找，使用更通用的正则表达式
    if not time_match and '记录了' in content_html:
        # 支持多种引号格式和HTML实体编码
        time_match = re.search(r'记录了\s*(?:&ldquo;|&rdquo;|&quot;|"|\'|“|”|'')([^"\'“”&]+)(?:&ldquo;|&rdquo;|&quot;|"|\'|“|”|'')', content_html)
    
    # 如果还是没找到，尝试直接提取数字+单位的模式
    if not time_match and '记录了' in content_html:
        time_match = re.search(r'记录了\s*([\d.]+\s+hours?)', content_html)

    if not time_match:
        return None

    logged_time = time_match.group(1).strip()

    # 改进任务信息提取，支持多种格式
    # 格式1: <a href="/browse/KJBG-705">KJBG-705 - 前端-首页</a>
    # 格式2: <a href="/browse/KJBG-717"><span class='resolved-link'>KJBG-717</span> - 【前端】继续申请电商账户优化</a>
    
    # 先尝试匹配格式2（包含span标签）
    issue_match = re.search(r'<a[^>]*href=["\']/browse/([A-Z]+-\d+)["\'][^>]*><span[^>]*>[^<]*</span>\s*-\s*([^<]+)</a>', title_html)
    if issue_match:
        issue_id = issue_match.group(1)
        description = issue_match.group(2).strip()
        summary = f"{issue_id} - {description}"
    else:
        # 尝试匹配格式1（标准格式）
        issue_match = re.search(r'<a[^>]*href=["\']/browse/([A-Z]+-\d+)["\'][^>]*>([A-Z]+-\d+\s*-\s*[^<]+)</a>', title_html)
        if issue_match:
            summary = issue_match.group(2).strip()
        else:
            # 尝试直接从title中提取任务编号和名称，不依赖完整的HTML结构
            # 匹配类似: KJBG-705 - 前端-首页
            simple_match = re.search(r'([A-Z]+-\d+\s*-\s*[^<]+)', title_html)
            if simple_match:
                summary = simple_match.group(1).strip()
            else:
                # 尝试只提取任务编号
                issue_id_match = re.search(r'KJBG-\d+', title_html)
                if issue_id_match:
                    # 如果content中有描述，可以尝试从中获取摘要信息
                    if content_html:
                        # 从blockquote中提取内容
                        quote_match = re.search(r'<blockquote>\s*<p>([^<]+)</p>\s*</blockquote>', content_html)
                        if quote_match:
                            summary = f"{issue_id_match.group(0)} - {quote_match.group(1).strip()}"
                        else:
                            # 提取content中的纯文本
                            content_text = re.sub(r'<[^>]+>', ' ', content_html)
                            content_text = re.sub(r'\s+', ' ', content_text).strip()
                            if content_text:
                                summary = f"{issue_id_match.group(0)} - {content_text[:50]}"  # 限制长度
                            else:
                                summary = f"{issue_id_match.group(0)} - 未知摘要"
                    else:
                        summary = f"{issue_id_match.group(0)} - 未知摘要"
                else:
                    summary = "未知任务"

    return summary, logged_time


def parse_datetime_zulu(zulu_str):
    """将 '2025-10-17T08:43:00.000Z' 转为本地日期字符串 YYYY-MM-DD"""
    dt = datetime.strptime(zulu_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%Y-%m-%d")


def fetch_and_parse(max_results):
    params = {
        'maxResults': max_results,
        'relativeLinks': 'true',
        'streams': f'user IS {RAW_USERNAME}',
        '_': str(int(datetime.now().timestamp() * 1000))
    }

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        params=params,
        verify=False
    )
    
    print(f"状态码: {response.status_code}")
    print(f"请求 URL: {response.url}")
    
    # 尝试解析XML，如果失败则打印内容的前500个字符用于调试
    try:
        root = ET.fromstring(response.content)
        entries = root.findall('atom:entry', NAMESPACES)
        results = []
    except ET.ParseError:
        print("\n=== XML解析失败，返回内容预览（前500字符） ===")
        print(response.content[:500].decode('utf-8', errors='replace'))
        # 如果返回的是登录页面，说明需要重新登录获取Cookie
        if b'<form' in response.content or b'login' in response.content.lower():
            print("\n错误原因：会话已过期，返回了登录页面")
        raise

    for entry in entries:
        title_elem = entry.find('atom:title', NAMESPACES)
        content_elem = entry.find('atom:content', NAMESPACES)
        published_elem = entry.find('atom:published', NAMESPACES)

        title_html = title_elem.text if title_elem is not None else ""
        content_html = content_elem.text if content_elem is not None else ""
        published = published_elem.text if published_elem is not None else ""

        extracted = extract_logged_time(title_html, content_html)
        if extracted:
            summary, logged_time = extracted
            date_str = parse_datetime_zulu(published)
            results.append((date_str, summary, logged_time))

    return results


# ================== 主程序 ==================
def main():
    parser = argparse.ArgumentParser(description="提取 Jira 中段海洋的工时记录")
    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="最大返回结果数（默认: 10）"
    )
    args = parser.parse_args()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print(f"正在获取最多 {args.max_results} 条记录...")
    try:
        logs = fetch_and_parse(args.max_results)
    except Exception as e:
        print(f"请求失败: {e}")
        # 我们需要更详细地调试这个问题
        print("\n=== 调试信息 ===")
        print("可能的问题：")
        print("1. Cookie已过期，需要更新")
        print("2. 用户名格式有问题")
        print("3. 返回的内容不是有效的XML")
        print("\n请检查Cookie是否过期，并更新到最新值")
        return

    # 去重（按完整元组）
    seen = set()
    unique_logs = []
    for log in logs:
        if log not in seen:
            seen.add(log)
            unique_logs.append(log)

    # 按天分组并计算总工时
    daily_logs = {}
    for date_str, summary, logged_time in unique_logs:
        if date_str not in daily_logs:
            daily_logs[date_str] = []
        daily_logs[date_str].append((summary, logged_time))
    
    # 输出按天分组的结果
    print("\n=== 提取的日志 ===")
    if not unique_logs:
        print("未找到任何工时记录。请检查 Cookie 是否有效或用户名是否正确。")
    else:
        # 按日期降序排列
        sorted_dates = sorted(daily_logs.keys(), reverse=True)
        
        for date in sorted_dates:
            # 计算当天总工时
            total_hours = 0
            records = daily_logs[date]
            
            for summary, logged_time in records:
                # 提取数字部分和单位，支持 1 hour, 7 hours, 1 day, 2 days, 30 minutes 等格式
                # 使用findall匹配所有时间段，支持"7 hours, 30 minutes"这样的格式
                matches = re.findall(r'(\d+(?:\.\d+)?)\s*(hour|day|minute)s?', logged_time.lower())
                
                for match in matches:
                    value = float(match[0])
                    unit_base = match[1]  # 去掉可能的复数结尾's'
                    
                    # 转换单位
                    if unit_base == 'day':
                        total_hours += value * 8
                    elif unit_base == 'hour':
                        total_hours += value
                    elif unit_base == 'minute':
                        # 将分钟转换为小时
                        total_hours += value / 60
            
            # 格式化日期显示（如：2025年 10.17日（周五））
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            # 星期几的中文表示
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday_text = weekdays[date_obj.weekday()]
            
            # 获取当前执行时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建格式化的日期输出
            full_formatted_date = f"{date_obj.year}年 {date_obj.month}.{date_obj.day}日（{weekday_text}）"
            short_formatted_date = f"{date_obj.month}.{date_obj.day}日"
            
            # 构建完整的汇总行文本（包含执行时间）
            summary_line = f"{full_formatted_date}：共记录工时📝 {total_hours:.1f}h：{short_formatted_date}明细如下（写入时间：{current_time}）："
            
            # 输出日期汇总信息
            print(f"{summary_line}")
            
            # 输出当天的所有记录
            for summary, logged_time in records:
                print(f"{date} 段海洋 {summary} 记录了 {logged_time}")
            print()
            
            # 检查并写入汇总行到日志文件
            log_file_path = "c:/Users/段海洋/myfiles/auto_files/ui_autotest/2022ui_autotest/Kuajing/Little_tools/通用文件夹/工时记录日志表.text"
            try:
                # 读取现有内容（如果存在）
                existing_content = []
                try:
                    with open(log_file_path, 'r', encoding='utf-8') as f:
                        existing_content = f.readlines()
                except FileNotFoundError:
                    print(f"日志文件不存在，将创建新文件: {log_file_path}")
                except Exception as read_error:
                    print(f"读取日志文件时出错: {read_error}")
                
                # 构建新的日志内容块（包含日期汇总和详细记录）
                new_log_block = []
                new_log_block.append(summary_line + '\n')
                for summary_item, logged_time in records:
                    detail_line = f"{date} 段海洋 {summary_item} 记录了 {logged_time}"
                    new_log_block.append(detail_line + '\n')
                new_log_block.append('\n')
                
                # 检查是否已存在相同日期的记录块，忽略写入时间
                # 提取日期标识（不包含写入时间）
                date_identifier = f"{date_obj.year}年 {date_obj.month}.{date_obj.day}日"
                
                # 找出所有包含相同日期的记录块的起始和结束位置
                record_blocks = []
                i = 0
                while i < len(existing_content):
                    if existing_content[i].strip().startswith(date_identifier):
                        # 找到记录块的起始位置
                        start = i
                        # 寻找记录块的结束位置（空行）
                        end = start + 1
                        while end < len(existing_content) and (existing_content[end].strip() or end <= start + 1):
                            end += 1
                        record_blocks.append((start, end))
                        i = end
                    else:
                        i += 1
                
                # 如果存在相同日期的记录块，移除它们
                if record_blocks:
                    # 按索引从大到小排序，从后往前删除
                    record_blocks.sort(reverse=True, key=lambda x: x[0])
                    
                    # 创建新的内容列表，不包含已存在的相同日期记录块
                    new_content = existing_content.copy()
                    for start, end in record_blocks:
                        # 删除从start到end（不包含end）的行
                        del new_content[start:end]
                    
                    existing_content = new_content
                
                # 将新的记录块添加到文件开头
                with open(log_file_path, 'w', encoding='utf-8') as f:
                    # 先写入新的记录块
                    f.writelines(new_log_block)
                    # 再写入剩余的现有内容
                    f.writelines(existing_content)
                
                print(f"成功写入日志: {summary_line}")
            except Exception as e:
                print(f"写入日志文件时出错: {e}")


if __name__ == "__main__":
    main()