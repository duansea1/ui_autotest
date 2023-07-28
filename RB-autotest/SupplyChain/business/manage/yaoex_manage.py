'''
Created on 2018年11月15日

@author: zengkai
'''
from business.BasePage import Base
from business.manage import resources as R
from time import sleep
from selenium.webdriver.support.select import Select
from public.files import read_txt


class Yaoex(Base):
    
    
    def click_frist_level(self,first_name):
        '''选择一级菜单'''
        first_level_btns = self.find_elements(R.YaoexManage.yaoex_first_level)
        flag=True
        for btn in first_level_btns:
            if btn.text.strip()==first_name:
                flag=False
                btn.click()
                sleep(3)
                break
        
        if flag:
            print('未找到一级菜单：',first_name)
            raise Exception('未找到一级菜单')
        
#         for i in range(len(first_level_btns)):
#             if first_level_btns[i].text.strip()==frist_name:
#                 first_level_btns[i].click() #点击一级菜单
#                 sleep(3)
#                 break
        
        
   
    def click_child_level(self,child_name):
        '''选择二级菜单'''
        child_all_levels = self.find_elements(R.YaoexManage.yaoex_all_level)
        flag=True
        for c in child_all_levels:
            if c.text.strip()==child_name:
                flag=False
                c.click()
                sleep(3)
                break
        
        if flag:
            print('未找到二级级菜单：',child_name)
            raise Exception('未找到二级菜单')
        
#         for i in range(len(child_all_levels)):
#             if child_all_levels[i].text.strip()==child_name:
#                 child_all_levels[i].click() #点击二级菜单
#                 sleep(3)
#                 break 
        
        self.driver.switch_to.frame('iframes')
        sleep(3)
    
    
    def search_1qg_multiquery(self,spu=None,aid=None,display='all',suppler=None):
        '''多条件查询
        @param display:    默认None/all，0-展示，1-不展示 
        @param suppler:    默认None/all,展示所有商家，8353-广东壹号药业，125476-重庆亿昊药业'''
        if spu:
            self.find_element(R.YaoexManage.spu_code).send_keys(spu)
        if aid:    
            self.find_element(R.YaoexManage.active_id).send_keys(aid)
        if display!='all' and display is not None:
            Select(self.find_element(R.YaoexManage.select_option)).select_by_value(display)
        if suppler!='all' and suppler is not None:
            Select(self.find_element(R.YaoexManage.select_shop)).select_by_value(suppler)
        sleep(2)
        self.find_element(R.YaoexManage.query).click()
        
        
    def create_1qg_activitie(self):
        ''''''
        self.find_element(R.YaoexManage.create_btn).click()
        sleep(3)
        create_params=read_txt('1qigou_create','manage')
        upload_btns=self.find_elements(R.YaoexManage.upload_button)
        for btn in upload_btns:
            btn.click()
            sleep(60)
            self.find_element(R.YaoexManage.upload_pop_addimg).send_keys('D:/000imgs/111111111111111111.png')
            sleep(1)
            self.find_element(R.YaoexManage.upload_pop_upload).click()
            sleep(1)
            self.find_element(R.YaoexManage.upload_pop_confirm).click()
            sleep(1)
            
        for paramstr in create_params:
            title=paramstr.split('——')[0]
            param=paramstr.split('——')[1]
            if title=='活动商家':
                if param=='all':
                    self.find_element(R.YaoexManage.shop_select_all).click() #补全
                else:
                    ele_loc='input[entername="{}"]'.format(param)
                    self.driver.find_element_by_css_selector(ele_loc).click()
            if title=='项目名称':
                self.driver.find_element_by_id('project_name').send_keys(param)
            if title=='活动描述':
                self.driver.find_element_by_id('project_desc').send_keys(param)
            if title=='预计发货时间':
                self.driver.find_element_by_id('delivery_time').send_keys(param)
            if title=='排序':
                sleep(3)
                self.driver.find_element_by_id('sort').send_keys(param)
                sleep(4)
            if title=='添加活动商品':
                self.driver.find_element_by_id('addProduct').click()
                sleep(3)
                #handles = self.window_handles  # 获取所有弹出窗口句柄
                #self.switch_to.window(handles[-1])  # 切换到弹出窗口
                #sleep(3)
                self.find_element(R.YaoexManage.product_code).send_keys(param)
                sleep(2)
                self.driver.find_element_by_id('saveProduct').click()
                sleep(3)
            if title=='客户类型':
                new_param=param.split(',')
                for i in new_param:
                    ele_par='input[textname="{}"]'.format(i)
                    self.driver.find_element_by_css_selector(ele_par).click() 
             
            if title=='活动单位':
                self.driver.find_element_by_id('unit').send_keys(param)
            if title=='批号':
                self.driver.find_element_by_id('batch_no').send_keys(param)
            if title=='有效期':
                self.driver.find_element_by_id('dead_line').send_keys(param)
            if title=='原价':
                self.driver.find_element_by_id('purchase_price').send_keys(param)            
            if title=='1起购价':
                self.driver.find_element_by_id('subscribe_price').send_keys(param)
            if title=='每人最多认购':
                self.driver.find_element_by_id('subscribe_num_per_client').send_keys(param)
            if title=='活动总量':
                self.driver.find_element_by_id('project_sum').send_keys(param)
            if title=='活动基数':
                self.driver.find_element_by_id('project_base_num').send_keys(param)
            if title=='客户基数':
                self.driver.find_element_by_id('client_base_num').send_keys(param)
            if title=='认购准则':
                self.driver.find_element_by_id('rule_desc').send_keys(param)
        self.find_element(R.YaoexManage.save_active).click()
        
    if __name__ == '__main__':
        pass  
    #def search_1qg_by_id(self,aid):
       # '''活动id查询'''
       # self.find_element(R.YaoexManage.active_id).send_keys(aid)
       # sleep(2)
       # self.find_element(R.YaoexManage.query).click()    
    
    #def search_1qg_by_id_by_spucode(self,spu):
       # '''多条件查询'''
       # self.find_element(R.YaoexManage.spu_code).send_keys(spu)
        #sleep(2)
        #self.find_element(R.YaoexManage.query).click()  