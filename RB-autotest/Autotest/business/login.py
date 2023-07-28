'''
Created on 2019年8月1日

@author: Administrator
'''
from Demoproject.home import HomePage
from Demoproject.BasePage import Base
from time import sleep


class Login(Base):
    
    def login_with_the_user(self, usernmae, password):
        '''登录固定账号'''
        self.driver.get('http://codemaster.runbaba.com/Home/Public/login.html')
        sleep(3)
        user=self.driver.find_element_by_id('account')
        user.click()
        user.clear()
        user.send_keys(usernmae)
        p=self.driver.find_element_by_id('password')
        p.click()
        p.clear()
        p.send_keys(password)
        v=self.driver.find_element_by_id('verify')
        v.click()
        v.clear()
        v.send_keys('8888')
        self.driver.find_element_by_class_name('user_reg_sub').click()

if __name__ == '__main__':
    pass