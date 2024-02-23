# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-17 12:05
# ---
"""

https://so.gushiwen.cn/search.aspx?type=title&page=3&value=%e6%98%a5%e5%a4%a9&valuej=%e6%98%a5
"""

import re

import queue
import threading
import requests

count = 1
def downloader(q: queue.Queue):
    while not q.empty():
        url = q.get()
        r = requests.get(url, verify=False)
        print(url)
        print(re.findall(r"page=(\d)&value=", url))
        page_num = (re.findall(r"page=(\d)&value=", url))[0]
        print('page_num:', page_num)
        filename = f"春天{page_num}.html"
        with open(filename, 'wb') as f:
            f.write(r.content)


if __name__ == "__main__":
    q = queue.Queue()
    for i in range(1, 3):
        q.put(f"https://so.gushiwen.cn/search.aspx?type=title&page={i}&value=%e6%98%a5%e5%a4%a9&valuej=%e6%98%a5")
    # while not q.empty():
    #     print(q.get())

    t = threading.Thread(target=downloader, args=(q,))
    t.start()
    t.join()
    print("finished")