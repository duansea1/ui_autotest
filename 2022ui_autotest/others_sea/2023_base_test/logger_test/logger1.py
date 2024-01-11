# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月12日 17:13
# ---
import logging
logger = logging.getLogger("日志名字")
logger.setLevel(level="DEBUG")  # 设置日志收集器级别

handler = logging.FileHandler("日志路径.py")  # 初始化日志处理器 - 文件输出（指定位置使用绝对路径，默认当前目录下）
handler.setLevel("WARNING")

console_handler = logging.StreamHandler()  # 控制台输出
console_handler.setLevel("DEBUG")

logger.addHandler(handler) # 添加handler
logger.addHandler(console_handler)
# 设置日志格式，中间间隔使用冒号也可以(模块名字-报错行-收集器名字-级别-信息)
fmt = logging.Formatter("%(filename)s-%(lineno)s-%(name)s-%(levelname)s-%(massage)s")
handler.setFormatter(fmt) # 日志轮转 - 添加日志处理器
# 设置不同级别的logger -- 选择一个级别就可以
logging.info("")
logging.debug("")
logging.warning("111")
logging.error("")
logging.critical("")