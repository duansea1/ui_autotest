'''
Created on 2018年7月3日

@author: geqiuli

集团管理中心：http://arch-backend.111.com.cn/admin/index.do
'''
from time import sleep
from public import files
BASE='http://arch-backend.111.com.cn'
HOST='arch-backend.111.com.cn'

class Backend(object):
    def __init__(self,selenium):
        self.selenium=selenium
        self.handles=self.selenium.window_handles
        
    def login_arch_backend(self):
        account=files.read_json('account', 'manage')
        login_url='https://arch-backend.111.com.cn/admin/index.do'
        self.selenium.get(login_url)
        sleep(2)
        self.selenium.find_element_by_name('username').send_keys(account['name'])
        self.selenium.find_element_by_name('password').send_keys(account['password'])
        self.selenium.find_element_by_css_selector('.login_btn').click()    #点击登录按钮
        sleep(2)
        
        
    def sms_senddetail_page(self):
        pass

if __name__ == '__main__':
    pass