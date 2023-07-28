'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-16 11:34:10
#文件项目:   TMS
#文件名称:   登录模块
 '''
from time import sleep
from business.BasePage import Base
from business.manage import resources as R
from public.files import read_json
from business.tms.Resource import R
class Login(Base):

    def tms_login(self):
        self.driver.get(R.tms_menu.menu_link)
        print('进入TMS 配送管理系统')
        account=read_json('account',source='manage')
        id=account['name']
        pin=account['password']
        self.send_keys(R.tms_menu.user,id)
        self.send_keys(R.tms_menu.pwd,pin)
        self.click(R.tms_menu.login_button)
        sleep(1)
        current_url=self.get_current_url()
        print('当前网址为：'+current_url)

    def tms_login_in_new_window(self):
        print ('进入TMS 配送管理系统')
        js = 'window.open("http://tms2.111.com.cn/home");'
        self.driver.execute_script (js)
        sleep(1)
        account = read_json ('account', source='manage')
        id = account['name']
        pin = account['password']
        self.send_keys (R.tms_menu.user, id)
        self.send_keys (R.tms_menu.pwd, pin)
        self.click (R.tms_menu.login_button)
        sleep (1)
        current_url = self.get_current_url ()
        print ('当前网址为：' + current_url)

