'''
Created on 2017年8月3日

@author: caocheng
'''
import os

import pytest
# 
# from business.manage.warehouse_sys import proprietary_products
# from function import system
# 
# 
# def test_out_bound(selenium,warehouse,do_num,ordertype):
# #     do_num = io_.read_txt('send_no', 'out_bound')[0]
# #     warehouse = io_.read_txt('send_no', 'out_bound')[1]
# #     try:
# #         flag = io_.read_txt('send_no', 'out_bound')[2]
# #     except:
# #         flag = 'C'
# 
# 
#     print(u'登录')
#     proprietary_products.out_bound_login(selenium, warehouse)
#     
# 
# #     print(u'订单分配')
# #     f = proprietary_products.order_distribution(selenium, do_num)
# #     assert "分配完成" in f
# 
#     print(u'波次生成')
#     text = proprietary_products.order_bigWaveList(selenium, do_num, ordertype, warehouse)
#     wvsh_id = text.split(":")[1]
#     # wvsh_id = 'WVSH31710120000008'
#     print(u'波次号：'+wvsh_id)
#     assert "波次生成成功" in text
# 
#     print(u'波次计划')
#     pick_id = proprietary_products.order_wavesPlanList(selenium, wvsh_id,ordertype,warehouse)
#     print(u'分拣号：'+pick_id)
#     assert pick_id != None
# 
#     print(u'分拣确认')
#     assert '操作成功' in proprietary_products.order_pick(selenium, pick_id)
# 
#     # 暂时不用
#     # print(u'分拣')
#     # order_sorting(driver, wvsh_id)
# 
#     print(u'核拣装箱')
#     carton_no = proprietary_products.order_reCheck(selenium, do_num, warehouse)
#     print('箱号：' + carton_no)
# 
#     print(u'出库交接')
#     proprietary_products.order_entruckLoadingList(selenium, carton_no)
# 
# 
# if __name__ == '__main__':
#     from selenium import webdriver
#     driver = webdriver.Firefox()
#     driver.maximize_window()
#     driver.implicitly_wait(20)
#     test_out_bound(driver)
#     # report_name = system.get_report_path(os.path.basename(__file__).split('.')[0])
#     # print(report_name)
#     # args = [os.path.basename(__file__), '--driver=Firefox', '--html=' + report_name, '--self-contained-html']
#     driver.quit()
