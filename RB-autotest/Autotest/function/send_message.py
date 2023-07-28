import sys

import requests
import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(6)
driver.get(sys.argv[1])
time.sleep(1)
status = driver.find_element_by_xpath('/html/body/span[3]').text
print(status)
if '0 failed' in status:
    driver.quit()
    pass
else:
    url = "https://pushbear.ftqq.com/sub"
    param = {
        'sendkey': '4082-faa644079c993c330c47b3e4341af9ee',
        'text': sys.argv[2],
        'desp': '时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    result = requests.get(url, params=param)
    print(result)
    # 必定可以报异常
    fp = open(sys.argv[6] + '.png', 'rb')
