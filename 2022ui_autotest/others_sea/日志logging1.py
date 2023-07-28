# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年2月月06日 9:33
# ---
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')
logging.error("error")
logging.log(logging.DEBUG, "%s is %s old", "tom的", "年龄")


