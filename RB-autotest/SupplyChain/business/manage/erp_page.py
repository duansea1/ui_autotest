'''
Created on 2018年6月20日

@author: geqiuli
'''
from time import sleep
import re
from business.BasePage import Base
from business.manage import resources as R


class ERP_Operation(Base):

    def toggle_menu_levelone(self,modname):
        '''
        @param modname: 一级菜单名称
        '''
        #menus=self.driver.find_elements_by_css_selector('#page_accordion>.l-accordion-header>.l-accordion-header-inner>p')   #所有的一级菜单
        #menus_btn=self.driver.find_elements_by_css_selector('#page_accordion>.l-accordion-header>.l-accordion-toggle')   #所有的一级菜单的折叠闭合按钮
        menus = self.find_elements(R.ErpSystem.menu_first_level)
        menus_btn = self.find_elements(R.ErpSystem.menubtn_first_level)
        for i in range(len(menus)):
            if menus[i].text.strip()==modname:
                print(menus_btn[i].get_attribute("class"))
                if 'l-accordion-toggle-close' in menus_btn[i].get_attribute("class"):
                    menus[i].click()    #点击一级菜单
                    sleep(1)
                    break
        
        
    
    def toggle_menu_leveltwo(self,modname):    
        '''
        @param modname: 二级菜单名称
        '''
        #contents=self.driver.find_elements_by_css_selector('#page_accordion>.l-accordion-content')   #所有的二级菜单的容器
        contents=self.find_elements(R.ErpSystem.menu_second_container)   #所有的二级菜单的容器
        if len(contents)==1:
            contents[0].find_element_by_link_text(modname).click()   #点击二级菜单
            sleep(2)
        else:
            #print('多个content被定位到')
            for c in contents:
                print(c.get_attribute('style'))
                if 'display: block' in c.get_attribute('style'):
                    c.find_element_by_link_text(modname).click()   #点击二级菜单
                    sleep(2)
                    break
                
        
        selected_tab=self.find_element(R.ErpSystem.current_tab)   #tabs显示
        tabid=selected_tab.get_attribute('tabid')
        self.mod_frame=self.driver.find_element_by_id(tabid) 
        print(self.mod_frame.get_attribute('src'))  
        self.driver.switch_to.frame(self.mod_frame)    #切换iframe
        
        
    def search_user_by_mobile(self,mob_num):
        '''
        @param mob_num: 手机号'''
        mobile_input=self.driver.find_element_by_css_selector('input[ligeruiid="memberAuthMobile"]')    #定位到手机号输入框
        mobile_input.clear()
        mobile_input.send_keys(mob_num)
        self.driver.find_element_by_id('querybefore').click()  #点击查询按钮
        sleep(3)
        result_text=self.driver.find_element_by_css_selector('.l-bar-message>span').text    #搜索结果总数
        pattern=r'总(.*?)条.*?'
        total_num=re.search(pattern,result_text)
        print('搜索结果：',total_num.group(0))
        #print(total_num.group(1).strip())
        return total_num.group(1).strip()
        
    def doctor_create_order(self,mob_num):
        '''
        @param mob_num: 手机号'''
        result_num=self.search_user_by_mobile(mob_num)
        
        if result_num!='0':
            self.driver.find_element_by_link_text('跳转登录').click()    #点击搜索的第一条记录的下单按钮
            sleep(2)
            #self.driver.find_element_by_link_text('下单').click()    #点击搜索的第一条记录的下单按钮
            #sleep(2)
            self.driver.switch_to.default_content()
            #print(self.driver.window_handles)
            self.switch_to_latest_windows()
            print('跳转到：',self.driver.title)
            print('登录信息：',self.driver.find_element_by_id('logininfo').text)
    
    
    
if __name__ == '__main__':
    pass