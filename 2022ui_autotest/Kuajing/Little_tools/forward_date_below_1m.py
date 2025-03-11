import datetime
import calendar



def is_holiday(date):
    """判断是否为节假日"""
    return date in holidays


def add_working_days(start_date, days_to_add):
    """增加工作日天数，跳过指定的节假日"""
    current_date = start_date
    added_days = 0

    while added_days < days_to_add:
        current_date += datetime.timedelta(days=1)
        if not is_holiday(current_date):  # 只有非节假日的工作日才计数
            added_days += 1

    return current_date


def calculate_future_date(post_date, days_to_add):
    """计算未来日期并考虑节假日顺延"""
    future_date = post_date + datetime.timedelta(days=days_to_add)

    # 如果未来日期是节假日，则顺延至下一个非节假日的工作日
    while is_holiday(future_date):
        future_date += datetime.timedelta(days=1)

    return future_date


def add_month_with_holiday(post_date):
    """按照规则增加一个月，并考虑节假日顺延"""
    year = post_date.year
    month = post_date.month
    day = post_date.day

    # 计算下个月的同一天
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    # 如果原日期是月末最后一天，则目标日期也是下个月的最后一天
    if day == calendar.monthrange(year, month)[1]:
        next_day = calendar.monthrange(next_year, next_month)[1]
    else:
        try:
            next_day = min(day, calendar.monthrange(next_year, next_month)[1])
            next_month_same_day = datetime.date(next_year, next_month, next_day)
        except ValueError:
            # 如果下个月没有该天（例如31号），则取下个月最后一天
            next_day = calendar.monthrange(next_year, next_month)[1]

    next_month_same_day = datetime.date(next_year, next_month, next_day)

    # 如果新日期是节假日，则顺延至下一个工作日
    while is_holiday(next_month_same_day):
        next_month_same_day += datetime.timedelta(days=1)

    return next_month_same_day


def calculate_all_dates(post_date):
    """计算所有需要的日期"""
    dates = {}

    # 计算1D、1W、2W、1M后的日期
    dates['1D'] = calculate_future_date(post_date, 1)
    dates['1W'] = calculate_future_date(post_date, 7)
    dates['2W'] = calculate_future_date(post_date, 14)
    dates['3W'] = calculate_future_date(post_date, 21)
    dates['1M'] = add_month_with_holiday(post_date)

    return dates

# 示例节假日列表，实际应用中应根据具体情况更新
holidays = {
    datetime.date(2025, 3, 1),  # 假设这是个节假日
    datetime.date(2025, 3, 8),  # 另一个假设的节假日
    datetime.date(2025, 3, 18),
}

# 测试用例
spot_date = datetime.date(2025, 3, 13)  # 示例起始日期
result_dates = calculate_all_dates(spot_date)

for key, value in result_dates.items():
    print(f"{key} 后的日期: {value}")