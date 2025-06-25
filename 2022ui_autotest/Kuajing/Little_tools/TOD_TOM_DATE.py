import json
from datetime import datetime, timedelta
from loguru import logger as log

"""计算 TOD、TOM、SPOT FORWARD 日期"""

datelist = [u'2025-04-15', u'2025-04-16',u'2025-04-17', u'2025-05-01', u'2025-05-23', u'2026-03-24', u'2026-03-25', u'2026-03-26', u'2026-03-27', u'2026-03-28', u'2026-03-29', u'2026-03-30', u'2026-04-10', u'2026-04-11']


def get_dates_by_offsets( datelist):
    """
    根据传入的天数偏移量列表和一个需要避开的日期列表，计算并返回避开指定日期后的正确日期。

    :param offsets: 整数形式的天数偏移量列表
    :param datelist: 需要避开的日期列表，格式为 "%Y-%m-%d"
    """
    current_date = datetime.now().date()  # 获取当前日期，仅日期部分
    log.info("t_0_date:  {}".format(current_date))
    avoid_dates = set(datelist)  # 节假日结合
    log.info(u"节假日集合：{}".format(avoid_dates))
    date_type = {"t_-1_date": "OTHER_DATE", "t_0_date": "TOD_DATE", "t_1_date": "TOM_DATE", "t_2_date": "SPOT_DATE",
                 "t_3_date": "FORWARD_1D"}
    results = {}




    # 动态增加后续固定偏移量（如 t_1_date 和 t_2_date）

    # 计算 t_1_date
    t1_date = current_date + timedelta(days=1)
    while t1_date.strftime("%Y-%m-%d") in avoid_dates:
        t1_date += timedelta(days=1)

    t1_key = "t_1_date"
    t1_value = t1_date.strftime("%Y-%m-%d")
    results[t1_key] = t1_value
    vars.put(t1_key, t1_value)
    log.info("{}:{}:  {}".format(date_type[t1_key], t1_key, t1_value))

    # 计算 T+2（基于 T+1）
    t2_date = t1_date + timedelta(days=1)
    while t2_date.strftime("%Y-%m-%d") in avoid_dates:
        t2_date += timedelta(days=1)

    t2_key = "t_2_date"
    t2_value = t2_date.strftime("%Y-%m-%d")
    results[t2_key] = t2_value
    vars.put(t2_key, t2_value)
    log.info("{}:  {}".format(t2_key, t2_value))


get_dates_by_offsets(datelist)