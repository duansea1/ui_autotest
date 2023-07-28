# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年12月月09日 16:58
# ---

content = ["白色的鸽子", "白色的白色的鸽子白色的鸽子白色的鸽子鸽子",
           "蓝色色的鸽子", "2022年12 and i not in con月", "乌克兰", '黑色的太坑']
words = ["白色", "黑色","L色"]
con = []
for i in content:
    for word in words:
        print('ii', i, word)
        if (word in i or len(i)>15):
            con.append(i)
            # content.remove(i)
            # continue
print(set(con))
print(con)

# for i in content:
#     for word in words:
#         if word not in i and len(i) <15:
#             index = content.index(i)
#             print(index)
#             content.remove(i)
#             print(content)
#             content.insert(index,i)
#             print(con.append(index))
# print(content)