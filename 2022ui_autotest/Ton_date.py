from datetime import datetime, timedelta

from icecream import ic


# 获取当前时间："yyyy-MM-dd" 格式
def get_date_with_offset(days_offset):
    # 获取当前日期
    current_date = datetime.now()

    # 计算偏移后的日期
    date_with_offset = current_date + timedelta(days=days_offset)

    # 格式化日期为 "yyyy-MM-dd" 格式
    formatted_date = date_with_offset.strftime("%Y-%m-%d")

    return formatted_date


def get_tn_date(days_offset, datelist):
    # 获取当前日期并计算偏移后的日期
    current_date = datetime.now()
    date_with_offset = current_date + timedelta(days=days_offset)
    print(date_with_offset.strftime("%Y-%m-%d"))

    # 调整日期直到不在 datelist 中
    while date_with_offset.strftime("%Y-%m-%d") in datelist:
        date_with_offset += timedelta(days=1)
        print('日期已存在，调整日期:',date_with_offset)

    # 返回最终的格式化日期
    return date_with_offset.strftime("%Y-%m-%d")


print(get_tn_date(2,[u'2025-03-10', u'2025-03-12', u'2025-03-13', u'2025-03-15'] ))