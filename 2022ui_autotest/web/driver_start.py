
from selenium import webdriver

from time import sleep
driver = webdriver.Chrome()
driver.maximize_window()
sleep(1)
# driver.minimize_window()

driver.get(r"http://www.baidu.com")
# sleep(2)
print("页面title", driver.title)
print("当前页面网址", driver.current_url)
# print("", driver.get_cookie())

# driver.find_element("su")
driver.find_element_by_id('su').click()
driver.quit()
