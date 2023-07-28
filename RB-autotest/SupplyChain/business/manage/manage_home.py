'''
Created on 2018年5月7日

@author: geqiuli
'''
from time import sleep
from business.BasePage import Base
from business.manage import resources as R
from public.files import read_json
from selenium.webdriver.support.select import Select

MGR_URL='http://manage.111.com.cn/'

class ManageSystem(Base):

    def login(self,uname,upwd):
        ''''''
        self.driver.get(MGR_URL)
        sleep(3)
        #username=dr.find_element(by=By.CSS_SELECTOR,'input[name="username"]')
        username=self.driver.find_element_by_name('username')
        username.clear()
        username.send_keys(uname)
        #password=dr.find_element(by=By.CSS_SELECTOR,'input[name="password"]')
        password=self.driver.find_element_by_name('password')
        password.clear()
        password.send_keys(upwd)
        self.find_element(R.Managehome.login_button).click()
        sleep(3)
    
    def login_with_account(self, plat='1'):
        account=read_json('account', source='manage')
        self.login(account['name'], account['password'])
        self.chose_platform(plat)
        
    def chose_platform(self, plat='1'):
        '''
        @param plat: 1-广州壹号药网有限公司, 2-广州壹号药业有限公司, 3-重庆亿昊药业有限公司'''
        self.wait_until_display(R.Managehome.platform_selector)
        if plat!=1:
            Select(self.find_element(R.Managehome.platform_selector)).select_by_value(plat)
        self.find_element(R.Managehome.platform_submit_btn).click()
    
    def toggle_workplat(self, workplat='我的工作台'):
        '''切换工作台：
        @param plat: 我的工作台、 系统仓库、 系统工具'''
        current_workplat=self.find_element(R.Managehome.current_work_plat)
        print('当前工作台：',current_workplat.text.strip())
        if current_workplat.text.strip()!=workplat:
            all_workplat=self.find_elements(R.Managehome.work_plat)       
            for work in all_workplat:
                if work.text.strip()==workplat:
                    print('切换到工作台：',work.text.strip())
                    work.click()
                    sleep(2)
                    break
              
    def chose_subsystem(self,subsys,workflat='我的工作台',partialtext=False):    
        '''选择子系统
        @param workflat: 需要切换的工作台：我的工作台、 系统仓库、 系统工具
        @param partialtext: 请查看图标是文字还是图片，如果是文字请传True。
        已知的以下几个需要传True：1号药城自营后台、IM管理系统、搜索后台管理、手机报表、TMS配送管理系统(新)等'''
        self.toggle_workplat(workflat)
        if partialtext:
            sub_sys=self.driver.find_element_by_partial_link_text(subsys)
        else:
            sub_sys=self.driver.find_element_by_link_text(subsys)
        print('选择的子系统为：',sub_sys.text.strip())
        self.find_child_use_ele(sub_sys, R.Managehome.sub_system_image).click()

        sleep(2)
        self.switch_to_latest_windows()
        print('进入：',self.driver.title)
        return self.driver.page_source
    
    def get_all_subsystems(self, workplat='系统仓库'):
        self.toggle_workplat(workplat)
        all_subsys=self.find_elements(R.Managehome.sub_system)
        return all_subsys
        
            
#     def choose_manage_subsystem(self,sys):
#         '''选择系统仓库的子系统
#         :param sys: 采购管理系统，权限管理系统，商城管理 ,1号药城运营后台'''
# #         self.driver.find_element_by_css_selector('.header > div > ul > li.active').click()
#         menus = self.find_elements(R.Managehome.child_system) #定位页面中的多个元素
# #         menus = self.get_all_subsystems('系统仓库')
#         for p in menus:
#             if p.text.strip() == sys:
#                 p.click()
#                 print("当前系统：", self.driver.title)
#         sleep(3)
#         self.driver.implicitly_wait(10)
        
        
    def my_system_more(self):
        """我的系统，更多："""
#         more = self.driver.find_element_by_css_selector(R.Managehome.more_system)
#         more = self.driver.find_element_by_css_selector('.title-more > .more')
        self.click(R.Managehome.more_system)
        sleep(1)
        self.driver.switch_to_alert
        print(self.driver.title)
    
    def choose_subsystem_from_mysystem(self, sys):
        """
        我的系统-更多中，选择子系统；（线上权限开通后，在我的工作台-我的系统-更多中进入）
        :parama: sys:子系统
        """
        self.my_system_more()
        sub_system = self.find_elements(R.Managehome.my_systems)
#         sub_system = self.find_elements('.dialog-content-main > ul > li > a')
        for p in sub_system:
            if p.text == sys:
                print(p.text)
                p.click()
        sleep(3)
        self.switch_to_latest_windows()
          
        
    
if __name__ == '__main__':
    pass