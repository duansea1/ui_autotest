# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-24 21:13
# ---
# 推导式公式 [迭代中的每一个元素 for语句 条件判断]
print(["第" + str(i) for i in range(1, 50) if i % 2 == 0])
cooks = "ey=JzdWIiOiIxIiwiaXNzIj.oiaHR0cDpcL1wvOiIsImV4cCI==6MTY5O.DM1NzQ2NCwiaWF0IjoxNjk==4MzE0MjY0L.CJuYm=iOjE2O"
new_cookie = {}
for cook in cooks.split("."):
    print(cook)
    s = cook.split("=")
    print(s)
    new_cookie[s[0]] = s[1]
print(new_cookie)

print({cook.split("=")[0]: cook.split("=")[1] for cook in cooks.split('.')})  # 字典推导式

