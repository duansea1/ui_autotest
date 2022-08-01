
from selenium import webdriver
import unittest
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

VisitUrl = r'http://sougou.com'
url_baidu = r'http://www.baidu.com'


# def baidu():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     sleep(1)
#     # driver.minimize_window()
#
#     driver.get(url_baidu)
#     # sleep(2)
#     print("页面title", driver.title)
#     print("当前页面网址", driver.current_url)
#     # print("", driver.get_cookie())
#
#     # driver.find_element("su")
#     driver.find_element_by_id('su').click()
#     driver.quit()


class VisitSouGouByChrome(unittest.TestCase):

    def setUp(self):
        '''启动浏览器'''

        self.driver = webdriver.Chrome()  # 启动谷歌浏览器
        self.driver.maximize_window()


    # def test_visitsougou(self):
    #     # 访问搜狗首页
    #     self.driver.get(VisitUrl)
    #     print(self.driver.current_url)
    #     sleep(2)
    #     # 访问百度
    #     self.driver.get(url_baidu)
    #     print(self.driver.current_url)
    #     # 返回上一次访问过的搜狗首页
    #     self.driver.back()
    #     sleep(1)
    #     self.driver.forward()  # 再次回到百度首页
    #     self.driver.refresh()  # 刷新当前页面
    #     sleep(1)
    #     position = self.driver.get_window_position()
    #     print("坐标：", position)
    #     self.driver.set_window_position(y=200, x=400)
    #     # 设置浏览器的位置后，再次获取浏览器的位置信息
    #     print("设置后：", self.driver.get_window_position())


    def test_getTitle(self):
        # 获取页面的属性值
        self.driver.get(url_baidu)
        print(self.driver.current_url)
        title = self.driver.title
        print("title:", title)

    def test_operateWindowHandle(self):
        self.driver.get(url_baidu)
        # 获取当前窗口的句柄
        now_handle = self.driver.current_window_handle
        print("当前窗口的句柄：", now_handle)
        try:
            result = self.driver.get_screenshot_as_file(r"C:\Users\段海洋\Pictures\Saved Pictures\screenPicture.png")
            print(result)
        except IOError as e:
            print(e)
        sleep(2)


        search = self.driver.find_element_by_id('kw')
        search.send_keys("w3cschool")
        search_btn = self.driver.find_element_by_id('su')
        print("双点击")
        action_chain = ActionChains(self.driver)
        action_chain.double_click(search_btn).perform()
        # print("元素是否可见：", search_btn.is_displayed())
        sleep(20)




        search_btn.click()  # 点击搜索
        sleep(2)
        w3c_door = self.driver.find_element_by_xpath('//*[@id="3"]//a')
        w3c_door.click()
        sleep(2)
        # 获取窗口所有句柄
        all_handles = self.driver.window_handles
        print("所有的句柄-最后一个：", self.driver.window_handles[-1])
        for handle in all_handles:
            if handle != now_handle:
                print("输出当前不一致的句柄：", handle)

        self.driver.switch_to_window(handle)
        self.driver.find_element_by_link_text('HTML').click()
        sleep(2)
        self.driver.close()  # 关闭当前的窗口
        sleep(2)
        # 打印主窗口的句柄
        print('主窗口的句柄：', now_handle)
        self.driver.switch_to_window(now_handle)
        sleep(3)
        print('返回到百度的首页')
        search.clear()
        search.send_keys('光荣之路自动化测试')
        search_btn.click()
        sleep(5)
        print("success")




    def tearDown(self):
        # 关闭浏览器
        self.driver.quit()

    def click_btn(self, ele):
        """@:param ele: 元素
        """
        ele.click()
        sleep(1)

    def printSelectText(self):
        "遍历所有选项并打印选项显示的文本和选项值"
        select = self.driver.find_element_by_class_name("name")
        all_options = self.driver.find_elements("jjj")
        for option in all_options:
            print(option.get_attribute('value'))
        print("done")


if __name__ == "__main__":
    unittest.main()
