'''
Created on 2018年11月19日

@author: liya
'''
import pytest
from time import sleep
from business.BasePage import Base
from business.manage import resources as R, manage_home
from public.files import read_json
from selenium.webdriver.support.select import Select
from business.manage.manage_home import ManageSystem
from business.manage.yaoex_self_support_manage import YaoexMenu


@pytest.mark.test_1
def test_addpromotion(selenium):
    """
    1药城自营后台创建特价活动"""
    ms = ManageSystem(selenium)
    ms.login_with_account()
#     ms.toggle_workplat()
    ms.chose_subsystem('1号药城自营后台','系统仓库', 'True')
#     ms.choose_manage_subsystem('1号药城自营后台')
    ym = YaoexMenu(selenium)
    ym.select_merchant('8353') #自营商家后台，选择广东壹号药业
    ym.father_menu('促销活动')  #左侧一级菜单：促销活动
    ym.child_menu('活动管理')   #左侧二级菜单：活动管理
    ym.choose_promotion_tab('特价活动')
    ym.creat_promotion() #新建活动
    ym.promotion_name('自动化特价券-互斥') #输入活动名称
    ym.creat_promotion('自动化特价券-互斥')
    ym.promotion_time('2022', '3') #活动结束时间-2022年3月的今天；开始时间-今天
    ym.chose_custm('testauto') #输入客户组
    ym.chose_use_coupon('1') #特价客户组，不可用券（只显示特价，不能再用其他优惠券）
    ym.price_to_custm('0')  #价格对未登录客户不展示
    ym.creat_promotion_btn() #提交特价活动
#     assert u'自动化特价券-互斥' in selenium.page.source
    ym.operate_promotion('编辑商品')
#     name = ym.promotion_name()
    ym.search_promotion_name('自动化特价-券互斥')
    ym.operate_promotion('编辑商品')
    ym.add_product('0081922114') #添加本公司商品编码，轮椅车H062-自动化专用-其他人勿用
    

    
if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'test_1',driver='Chrome')