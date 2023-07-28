"""
Created on 2017年8月3日
@author: caocheng

Modified by whb @ 2018.12.21

"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from business.BasePage import Base
from business.warehouse_sys import outbound_resource as R


class Warehouse_outbound(Base):
    warehouse_list={
        "70":"test1111",
        "20":"重庆药业仓",
        "233951":"广州药网仓库",
        "233903":"广州药业2号仓",
        "13":"广州药业仓库（新）",
        "15":"昆山药网仓库",
        "30":"昆山亿方药业仓",
        "233900":"廊坊仓库",
        "233950":"上海药网仓库",
        "10":"天津仓",
        "233901":"武汉仓库",
        "53":"武汉测试药业仓"
        }

    def outbound_process(self, warehouse_id, do_num, isYCorder):
        """通用方法"""
        # self.driver = webdriver.Chrome()
        # self.maximize_window()
        # 登陆
        self.outbound_login(warehouse_id)
        # 查询do_num状态
        do_status = self.outbound_delivery_order(do_num, isYCorder)
        if '初始化' in do_status:
            self.outbound_initial_process(do_num, isYCorder)
        elif '分配完成' in do_status:
            self.outbound_dispatched_process(do_num, isYCorder)
        elif '拣货完成' in do_status:
            self.outbound_confirmed_process(do_num, isYCorder)
        elif '分拣完成' in do_status:
            self.outbound_sorted_process(do_num)
        elif '装箱完成' in do_status:
            self.outbound_encaseed_process(do_num)
        else:
            print('DO状态异常')
        return

    def outbound_initial_process(self, do_num, isYCorder):
        """状态为初始化的do_num"""
    # 订单分配
        order_dispatch_status = self.outbound_order_distribution(do_num)
        if "分配成功" in order_dispatch_status:
            # 生成波次
            wave_status = self.outbound_wave_generation(do_num, isYCorder)
            if "波次生成成功" in wave_status:
                # 波次计划
                wave_id = wave_status.split(":")[1]
                pick_id = self.outbound_wave_plan(wave_id, isYCorder)
                if pick_id != None:
                    # 拣货确认
                    confirm_status = self.outbound_pick_confirm(pick_id)
                    if '操作成功' in confirm_status:
                        # 分拣
                        sorting_status = self.outbound_sorting(wave_id)
                        if '分拣成功' in sorting_status:
                            # 核拣装箱
                            carton_no = self.outbound_encasement(do_num)
                            if carton_no != None:
                                # 出库交接
                                handover_status = self.outbound_handover(carton_no)
                                if '已发货' in handover_status:
                                    print('出库完成，关闭浏览器')
                                    self.driver.quit()
                                else:
                                    print('交接失败！')
                            else:
                                print('装箱失败！')
                        else:
                            print('分拣失败！')
                    else:
                        print('拣货确认失败！')
                else:
                    print('波次计划失败！')
            else:
                print('生成波次失败！')
        else:
            print('分配失败！')

        return

    def outbound_dispatched_process(self, do_num, isYCorder):
        """状态为分配完成的do_num"""
        wave_id = self.outbound_getwave_id(do_num, isYCorder)
        if wave_id == None:
            # 生成波次
            wave_status = self.outbound_wave_generation(do_num, isYCorder)
            if "波次生成成功" in wave_status:
                # 波次计划
                wave_id = wave_status.split(":")[1]
            else:
                print('生成波次失败！')
        pick_id = self.outbound_wave_plan(wave_id, isYCorder)
        if pick_id != None:
            # 拣货确认
            confirm_status = self.outbound_pick_confirm(pick_id)
            if '操作成功' in confirm_status:
                # 分拣
                sorting_status = self.outbound_sorting(wave_id)
                if '分拣成功' in sorting_status:
                    # 核拣装箱
                    carton_no = self.outbound_encasement(do_num)
                    if carton_no != None:
                        # 出库交接
                        handover_status = self.outbound_handover(carton_no)
                        if '已发货' in handover_status:
                            print('出库完成，关闭浏览器')
                            self.driver.quit()
                        else:
                            print('交接失败！')
                    else:
                        print('装箱失败！')
                else:
                    print('分拣失败！')
            else:
                print('拣货确认失败！')
        else:
            print('波次计划失败！')

        return

    def outbound_confirmed_process(self, do_num, isYCorder):
        """状态为拣货完成的do_num"""
        # 获取波次号
        wave_id = self.outbound_getwave_id(do_num, isYCorder)
        if wave_id != None:
            # 分拣
            sorting_status = self.outbound_sorting(wave_id)
            if '分拣成功' in sorting_status:
                # 核拣装箱
                carton_no = self.outbound_encasement(do_num)
                if carton_no != None:
                    # 出库交接
                    handover_status = self.outbound_handover(carton_no)
                    if '已发货' in handover_status:
                        print('出库完成，关闭浏览器')
                        self.driver.quit()
                    else:
                        print('交接失败！')
                else:
                    print('装箱失败！')
            else:
                print('分拣失败！')
        else:
            print('查询波次号失败！')

        return

    def outbound_sorted_process(self, do_num):
        """状态为分拣完成的do_num"""
        # 核拣装箱
        carton_no = self.outbound_encasement(do_num)
        if carton_no != None:
            # 出库交接
            handover_status = self.outbound_handover(carton_no)
            if '已发货' in handover_status:
                print('出库完成，关闭浏览器')
                self.driver.quit()
            else:
                print('交接失败！')
        else:
            print('装箱失败！')

        return

    def outbound_encaseed_process(self, do_num):
        """状态为装箱完成的do_num"""
        # 获取箱号
        carton_no = self.outbound_getcarbon_no(do_num)
        if carton_no != None:
            # 出库交接
            handover_status = self.outbound_handover(carton_no)
            if '已发货' in handover_status:
                print('出库完成，关闭浏览器')
                self.driver.quit()
            else:
                print('交接失败！')
        else:
            print('查询箱号失败！')

        return

    def outbound_getwave_id(self, do_num, isYCorder):
        """出库管理-发货单-获取波次号"""
        self.driver.get('http://10.6.80.248:8080/delivery/deliveryOrderList.xhtml')
        sleep(3)
        print('出库管理-发货单')
        self.send_keys(R.DeliveryOrder.start_do, do_num)
        self.send_keys(R.DeliveryOrder.end_do, do_num)
        # start_do = self.find_element_by_css_selector('#searchForm>table>tbody>tr>td:nth-child(2)>input')
        # start_do.clear()
        # start_do.send_keys(do_num)
        # end_do = self.find_element_by_css_selector('#searchForm>table>tbody>tr>td:nth-child(4)>input')
        # end_do.clear()
        # end_do.send_keys(do_num)
        # 是否为B端订单
        if isYCorder=='True':
            self.find_element(R.DeliveryOrder.isYCorder).click()
            self.find_element(R.DeliveryOrder.search_button).click()
            # self.find_element_by_css_selector('#searchForm>table>tbody>tr:nth-child(3)>td:nth-child(11)>input').click()
            # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(1)
        result = self.find_elements(R.DeliveryOrder.result)
        # result = self.find_elements_by_xpath("//tbody[@id='selectForm:resultTable:tb']/tr")
        if len(result) == 0:
            print('未查询到记录')
        else:
            # return self.find_element_by_xpath("//tbody[@id='selectForm:resultTable:tb']/tr/td[18]").text
            return self.find_element(R.DeliveryOrder.wave_id).text

    def outbound_getcarbon_no(self, do_num):
        """出库管理-获取箱号"""
        print('打开核拣装箱页面')
        self.driver.get('http://10.6.80.248:8080/delivery/reCheck.xhtml')
        sleep(1)
        main_handle = self.driver.current_window_handle
        print('主窗口是' + main_handle)
        print('点击查询核拣记录')
        self.find_element(R.Encasement.recheck_detail).click()
        # self.driver.find_element_by_id('queryReCheckLink').click()
        sleep(2)
        all_handles = self.driver.window_handles
        for other_handle in all_handles:
            if other_handle != main_handle:
                self.driver.switch_to_window(other_handle)
                break
        secondary_handle = self.driver.current_window_handle
        print('次级窗口是' + secondary_handle)
        self.send_keys(R.Encasement.order_no, do_num)
        self.find_element(R.Encasement.submit_button).click()
        # self.driver.find_element_by_id('searchForm:orderNo').send_keys(do_num)
        # self.driver.find_element_by_id('submitBtn').click()
        sleep(1)
        result = self.find_elements(R.Encasement.result)
        # result = self.find_elements_by_xpath("//td[@id='resultForm:face_info']/table/tbody/tr/td/div/table/tbody/tr")
        # result = driver.find_elements_by_css_selector('#resultForm:face_info>table>tbody>tr>td>div>table>tbody>tr')
        if len(result) == 0:
            print('无查询结果')
        else:
            carton_no = self.find_element(R.Encasement.carton_no).text
            # carton_no = self.find_element_by_xpath(
            # "//td[@id='resultForm:face_info']/table/tbody/tr/td/div/table/tbody/tr[2]/td[3]/a").text
        self.driver.close()
        sleep(1)
        self.driver.switch_to_window(main_handle)
        sleep(1)

        return carton_no

    def outbound_login(self, warehouse_id):
        """登录页"""
        print('打开仓储管理系统')
        self.driver.maximize_window()
        self.driver.get('http://10.6.80.248:8080/login.xhtml')
        self.wait_until_display(R.Login.login_button)
        sleep(2)
        print('输入用户名' + R.user_name)
        self.send_keys(R.Login.user_name, R.user_name)
        print('输入密码' + R.user_password)
        self.send_keys(R.Login.password, R.user_password)
        sleep(2)
        print('选择仓库id=' + warehouse_id)
        print('选择的仓库是；',self.warehouse_list[str(warehouse_id)])
        # sleep(2)
        # selenium.find_element_by_id('loginForm:password').click()
        sleep(2)
        print('选择仓库' + warehouse_id)
        # sel = selenium.find_element_by_id('loginForm:warehouse')
        # Select(sel).select_by_value(warehouse_id)
        selector = Select(self.find_element(R.Login.warehouse))
        selector.select_by_value(warehouse_id)
        sleep(2)
        # print('已选择的仓库' + selector.first_selected_option().text)
        print('点击登录按钮，进入仓储管理系统')
        self.find_element(R.Login.login_button).click()
        return

    def outbound_delivery_order(self, do_num, isYCorder):
        """出库管理-发货单"""
        # 查询DO单号状态
        self.driver.get('http://10.6.80.248:8080/delivery/deliveryOrderList.xhtml')
        sleep(3)
        print('出库管理-发货单，输入DO号' + do_num)
        self.send_keys(R.DeliveryOrder.start_do, do_num)
        self.send_keys(R.DeliveryOrder.end_do, do_num)
        # start_do = self.find_element_by_css_selector('#searchForm>table>tbody>tr>td:nth-child(2)>input')
        # start_do.clear()
        # start_do.send_keys(do_num)
        # end_do = self.find_element_by_css_selector('#searchForm>table>tbody>tr>td:nth-child(4)>input')
        # end_do.clear()
        # end_do.send_keys(do_num)
        # 是否为B端订单
        print('是否为B端订单')
        if isYCorder=='True':
            self.find_element(R.DeliveryOrder.isYCorder).click()
        self.find_element(R.DeliveryOrder.search_button).click()
        #   self.find_element_by_css_selector('#searchForm>table>tbody>tr:nth-child(3)>td:nth-child(11)>input').click()
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(1)
        result = self.find_elements(R.DeliveryOrder.result)
        # result = self.find_elements_by_xpath("//tbody[@id='selectForm:resultTable:tb']/tr")
        # result = selenium.find_element_by_css_selector('#selectForm:resultTable:tb>tr')
        if len(result) == 0:
            print('未查询到记录')
        else:
            do_status = self.find_element(R.DeliveryOrder.do_status).text
            print('DO单状态为' + do_status)
            return do_status
            # return self.find_element_by_xpath("//tbody[@id='selectForm:resultTable:tb']/tr/td[4]").text

    def outbound_order_distribution(self, do_num):
        """出库管理-订单分配"""
        print('进入订单分配页面')
        self.driver.get('http://10.6.80.248:8080/delivery/doAllocate.xhtml')
        sleep(2)
        print('查找开始发货单号元素，输入do_num号' + do_num)
        # selenium.find_element_by_name('searchForm:j_id237').clear()
        # selenium.find_element_by_name('searchForm:j_id237').send_keys(do_num)
        # selenium.find_element_by_name('searchForm:j_id241').clear()
        # selenium.find_element_by_name('searchForm:j_id241').send_keys(do_num)
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").send_keys(do_num)
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input").send_keys(do_num)
        self.send_keys(R.OrderDistribution.start_do, do_num)
        self.send_keys(R.OrderDistribution.end_do, do_num)
        print('点击查询按钮')
        self.find_element(R.OrderDistribution.search_button).click()
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(2)
        # rich-table-row rich-table-firstrow listTableSingular
        # result = self.find_elements_by_xpath("//tbody[@id='selectForm:resultTable:tb']/tr")
        result = self.find_elements(R.OrderDistribution.result)
        if len(result) == 0:
            print('未查询到结果')
        else:
            if self.find_element(R.OrderDistribution.all_selected).is_selected() is False:
                self.find_element(R.OrderDistribution.all_selected).click()
            # if self.find_element_by_xpath("//tr[@class='rich-table-subheader']/th[1]/div/input").is_selected() is False:
            #     self.find_element_by_xpath("//tr[@class='rich-table-subheader']/th[1]/div/input").click()
            # self.driver.find_element_by_id('buttonToolForm:btnQuery2').click()
            self.find_element(R.OrderDistribution.dispatch_button).click()
            sleep(2)

            print('返回检查点')
            return self.find_element(R.Normal.message).text
            # return self.find_element_by_class_name('rich-messages-label').text

    def outbound_wave_generation(self, do_num, isYCorder):
        """出库管理-生成波次"""
        print('进入生成波次页面')
        self.driver.get('http://10.6.80.248:8080/delivery/bigWaveList.xhtml')
        # is_disappeared = WebDriverWait(selenium, 30).until(
        #     lambda x: x.find_element_by_xpath(".//*[@id='mainSizeControlBox']/div[1]").is_displayed())
        # if is_disappeared:
        sleep(2)
        print('查找发货单号元素，输入do_num号' + do_num)
        # selenium.find_element_by_xpath("searchForm:j_id238").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").send_keys(do_num)
        self.send_keys(R.WaveGeneration.do_num, do_num)

        if isYCorder=='True':
            print('B端订单，勾选B端单选按钮')
            self.find_element(R.WaveGeneration.isYCorder).click()
            # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[5]/td[10]/input").click()

        print('点击查询按钮')
        self.find_element(R.WaveGeneration.search_button).click()
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(2)
        result = self.find_elements(R.WaveGeneration.result)
        # result = self.find_elements_by_xpath("//tbody[@id='selectForm:resultTable:tb']/tr")
        if len(result) == 0:
            print('未查询到结果')
        else:
            if self.find_element(R.WaveGeneration.select_checkbox).is_selected() is False:
                self.find_element(R.WaveGeneration.select_checkbox).click()
            # if self.find_element_by_xpath(
            #         "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[1]/input").is_selected() is False:
            #     self.find_element_by_xpath(
            #         "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[1]/input").click()
            sleep(1)
            print('点击勾选订单生成波次按钮')
            self.find_element(R.WaveGeneration.generate_button).click()
            # self.find_element_by_name('buttonToolForm:btnQuery2').click()
            sleep(3)

            print('返回检查点')
            return self.find_element(R.Normal.message).text
            # return self.find_element_by_class_name('rich-messages-label').text

    def outbound_wave_plan(self, wave_id, isYCorder):
        """出库管理-波次计划"""
        print('波次编码是' + wave_id)
        print('进入波次计划页面')
        self.driver.get('http://10.6.80.248:8080/delivery/wavesPlanList.xhtml')
        sleep(2)
        print('填入波次编号From')
        self.send_keys(R.WavePlan.start_wave, wave_id)
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").send_keys(wave_id)
        print('填入波次编号To')
        self.send_keys(R.WavePlan.end_wave, wave_id)
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input").send_keys(wave_id)

        if isYCorder=='True':
            print('B端订单，勾选B端单选按钮')
            self.find_element(R.WavePlan.isYCorder).click()
            # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[4]/td[7]/input[2]").click()

        print('点击查询按钮')
        self.find_element(R.WavePlan.search_button).click()
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(2)
        result = self.find_elements(R.WavePlan.result)
        # result = self.find_elements_by_xpath("//tr[@class='rich-table-row rich-table-firstrow listTableSingular']")
        if len(result) == 0:
            print('未查询到结果')
        else:
            print('点击波次编号')
            self.find_element(R.WavePlan.wave_link_1st).click()
            # self.find_element_by_xpath("//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/a").click()
            main_handle = self.driver.current_window_handle
            print(main_handle)

        # clickJS = 'setTimeout(function(){document.querySelector("tr.rich-table-row>td:nth-child(2)>a").click()},100)'
        # selenium.execute_script(clickJS)
        # selenium.find_element_by_id('selectForm:j_id352:0:j_id359').click()
        # sleep(2)

            print('挑选窗口')
            all_handles = self.driver.window_handles
            for other_handle in all_handles:
                if (other_handle != main_handle):
                    self.driver.switch_to_window(other_handle)
                    break

            print('点击弹窗内的波次编号')
            # print('one: ', selenium.title)
            second_handle = self.driver.current_window_handle
            sleep(2)
            self.find_element(R.WavePlan.wave_link_2nd).click()
            # self.find_element_by_xpath("//div[@class='tableContainer']/table/tbody/tr[3]/td[2]/a").click()
            sleep(2)

            # clickJS = 'setTimeout(function(){document.getElementById("saveForm:j_id30").click()},100)'
            # selenium.execute_script(clickJS)

            print('挑选窗口2')
            all_handles = self.driver.window_handles
            for other_handle in all_handles:
                if other_handle != main_handle and other_handle != second_handle:
                    self.driver.switch_to_window(other_handle)
                    break

            print('获取拣货单号')
            sleep(2)
            # print('two: ', selenium.title)
            # pick_id = self.find_element_by_xpath("//div[@class='rich-panel-body ']/table/tbody/tr/td[2]/a").text
            pick_id = self.find_element(R.WavePlan.pick_id).text
            print('拣货单号是' + pick_id)
            print('关闭窗口')
            self.driver.close()
            self.driver.switch_to_window(second_handle)
            sleep(1)
            self.driver.close()
            self.driver.switch_to_window(main_handle)
            sleep(1)
            return pick_id

    def outbound_pick_confirm(self, pick_id):
        """出库管理-拣货确认"""
        print('打开拣货确认页面')
        self.driver.get('http://10.6.80.248:8080/delivery/pick.xhtml')
        sleep(2)
        print('填入拣货单号')
        self.send_keys(R.PickConfirm.pick_id, pick_id)
        # self.driver.find_element_by_id('dataForm:pickNoInput').clear()
        # self.driver.find_element_by_id('dataForm:pickNoInput').send_keys(pick_id)
        print('填入工号，随便填啥')
        self.send_keys(R.PickConfirm.work_no, '111')
        # self.driver.find_element_by_id('dataForm:pickInput').clear()
        # self.driver.find_element_by_id('dataForm:pickInput').send_keys('111')
        print('填入拣货设施，随便填啥')
        self.send_keys(R.PickConfirm.equipment_no, '111')
        # self.driver.find_element_by_id('dataForm:facilityInput').clear()
        # self.driver.find_element_by_id('dataForm:facilityInput').send_keys('111')
        print('输入回车键')
        self.driver.find_element_by_id('dataForm:facilityInput').send_keys(Keys.ENTER)
        sleep(3)
        return self.find_element(R.Normal.message).text
        # return self.find_element_by_class_name('rich-messages-label').text

    def outbound_sorting(self, wave_id):
        """出库管理-分拣"""
        print('打开分拣页面')
        self.driver.get('http://10.6.80.248:8080/delivery/sorting.xhtml')
        sleep(2)
        print('输入波次号')
        self.send_keys(R.Sorting.wave_id, wave_id)
        # self.driver.find_element_by_id('searchForm:waveNo').clear()
        # self.driver.find_element_by_id('searchForm:waveNo').send_keys(wave_id)
        sleep(1)
        print('点击按波次强制分拣')
        # self.driver.find_element_by_id('searchForm:btnSeed1').click()
        self.find_element(R.Sorting.sort_button).click()
        sleep(1)
        print('点击确认按钮')
        self.driver.switch_to_alert().accept()
        sleep(1)
        return self.find_element(R.Normal.message).text

    def outbound_encasement(self, do_num):
        """出库管理-核减装箱"""
        print('打开核拣装箱页面')
        self.driver.get('http://10.6.80.248:8080/delivery/reCheck.xhtml')
        sleep(1)
        print('输入发货单号')
        self.send_keys(R.Encasement.do_num, do_num)
        # self.driver.find_element_by_id('searchForm:orderNoInput').send_keys(do_num)
        print('点击确定按钮')
        self.find_element(R.Encasement.search_button).click()
        # self.driver.find_element_by_id('searchForm:doSearchBtn').click()
        sleep(2)
        print('点击查看订单明细')
        self.find_element(R.Encasement.order_detail).click()
        # self.find_element_by_css_selector('input[value="查看订单明细"]').click()
        sleep(2)
        # table = selenium.find_element_by_id('reCheckRecords')
        # table_rows = table.find_elements_by_tag_name('tr')
        # rows = len(table_rows) - 1
        # print(rows)

        # if is_element_exist('reCheckRecords:0:j_id708') is True:
        #     product_id = selenium.find_element_by_id('reCheckRecords:0:j_id708').text
        # else:
        #     origin_product_id = selenium.find_element_by_id('reCheckRecords:0:j_id707').text
        #     product_id = origin_product_id.split(",")[1]
        # product_id = self.find_element_by_xpath("//table[@id='reCheckRecords']/tbody/tr[1]/td[6]").text
        trs = self.find_elements(R.Encasement.trs)
        product_id = []
        product_count = []
        for tr in trs:
            product_id.append(tr.find_elements_by_tag_name('td')[4].text)
        for tr in trs:
            product_count.append(tr.find_elements_by_tag_name('td')[3].text)
        print('产品数量为' + str(len(trs)))
        print('产品条码为' + str(product_id))
        print('未核拣数为' + str(product_count))
        # product_id = self.find_element(R.Encasement.product_id).text
        # product_count = self.find_element(R.Encasement.product_count).text
        print('点击关闭窗口按钮')
        self.find_element(R.Encasement.close_button).click()

        # 循环装箱
        for i in range(0, len(trs), 1):
            if product_count[i] != 0:
                print('产品条码为' + str(product_id[i]))
                print('未核拣数为' + str(product_count[i]))
                sleep(1)
                if self.find_element(R.Encasement.select_checkbox).is_selected() is True:
                    self.find_element(R.Encasement.select_checkbox).click()
                # if self.driver.find_element_by_id('setScanMethodCB').is_selected() is True:
                #         self.driver.find_element_by_id('setScanMethodCB').click()
                # self.driver.find_element_by_id('newProductBarCode').clear()
                # self.driver.find_element_by_id('newProductBarCode').send_keys(product_id)
                self.send_keys(R.Encasement.product_id_input, product_id[i])
                self.send_keys(R.Encasement.product_num_input, product_count[i])
                self.driver.find_element_by_id('newProductBarCode').send_keys(Keys.ENTER)
                self.driver.find_element_by_id('newProductNumber').send_keys(Keys.ENTER)
                sleep(1)
        self.driver.switch_to_alert().accept()
        sleep(1)
        self.send_keys(R.Encasement.carton_qty, '1')
        # self.driver.find_element_by_id('confirmCartonQtyPanelSubview:cartonQtyInput').send_keys('1')
        # self.driver.find_element_by_id('confirmCartonQtyPanelSubview:confirmPackedNumForm:doConfirmCartonQtyBtn').click()
        self.find_element(R.Encasement.confirm_encase).click()
        sleep(1)
        main_handle = self.driver.current_window_handle
        print('主窗口是' + main_handle)
        print('点击查询核拣记录')
        self.driver.find_element_by_id('queryReCheckLink').click()
        all_handles = self.driver.window_handles
        for other_handle in all_handles:
            if other_handle != main_handle:
                self.driver.switch_to_window(other_handle)
                break
        secondary_handle = self.driver.current_window_handle
        print('次级窗口是' + secondary_handle)
        self.driver.find_element_by_id('searchForm:orderNo').clear()
        self.driver.find_element_by_id('searchForm:orderNo').send_keys(do_num)
        self.driver.find_element_by_id('searchForm:orderNo').send_keys(Keys.ENTER)
        sleep(1)
        # carton_no = selenium.find_element_by_css_selector('a[href="javascript:void(0)"]').text
        result = self.find_elements(R.Encasement.result)
        # result = self.find_elements_by_xpath("//td[@id='resultForm:face_info']/table/tbody/tr/td/div/table/tbody/tr")
        # result = driver.find_elements_by_css_selector('#resultForm:face_info>table>tbody>tr>td>div>table>tbody>tr')
        if len(result) == 0:
            print('无查询结果')
        else:
            carton_no = self.find_element(R.Encasement.carton_no).text
            # carton_no = self.find_element_by_xpath(
            #     "//td[@id='resultForm:face_info']/table/tbody/tr/td/div/table/tbody/tr[2]/td[3]/a").text
            self.driver.close()
            sleep(1)
            self.driver.switch_to_window(main_handle)
            print('箱号是' + carton_no)
            return carton_no

        # if rows == 1:
        #     print('取消选中逐件扫描')
        #     selenium.find_element_by_id('setScanMethodCB').click()
        #     sleep(2)
        #     print('点击查看订单明细')
        #     selenium.find_element_by_css_selector('input[value="查看订单明细"]').click()
        #     sleep(2)
        #     print('获取产品编码')
        #     product_code = selenium.find_element_by_id('reCheckRecords:0:j_id701').text
        #     print('点击关闭窗口按钮')
        #     selenium.find_element_by_id('hidelink').click()
        #     sleep(1)
        #     print('输入产品编码')
        #     selenium.find_element_by_id('newProductBarCode').send_keys(product_code)
        #     print('输入回车键')
        #     selenium.find_element_by_id('newProductBarCode').send_keys(Keys.ENTER)
        #     sleep(1)
        #     print('抓取产品个数')
        #     product_no = selenium.find_element_by_id('productTotalEl').text
        #     if warehouse_id == '10' or warehouse_id == '15':
        #         print('输入拣货总数量')
        #         sleep(2)
        #         selenium.find_element_by_id('skuCountInput').send_keys(product_no)
        #     print('输入产品个数')
        #     sleep(4)
        #     selenium.find_element_by_id('newProductNumber').clear()
        #     selenium.find_element_by_id('newProductNumber').send_keys(product_no)
        #     print('输入回车键')
        #     selenium.find_element_by_id('newProductNumber').send_keys(Keys.ENTER)
        #     sleep(4)
        #     print('点击确认按钮')
        #     selenium.switch_to_alert().accept()
        #     sleep(10)
        #     try:
        #         print('输入发票号码')
        #         selenium.find_element_by_id('invoiceInput').send_keys('I001')
        #         sleep(2)
        #         print('输入回车键')
        #         selenium.find_element_by_id('invoiceInput').send_keys(Keys.ENTER)
        #         sleep(3)
        #     except:
        #         pass
        #     # 判断是不是昆山仓，如果是需要输入箱子数量
        #     if warehouse_id == '15':
        #         print('输入数量')
        #         selenium.find_element_by_id('confirmCartonQtyPanelSubview:cartonQtyInput').send_keys('1')
        #     sleep(3)
        #     print('点击完成按钮')
        #     selenium.find_element_by_id('confirmCartonQtyPanelSubview:confirmPackedNumForm:doConfirmCartonQtyBtn').click()
        #     sleep(3)
        # elif rows > 1:
        #     print('取消选中逐件扫描')
        #     selenium.find_element_by_id('setScanMethodCB').click()
        #     print('获取未装箱数')
        #     pending = int(selenium.find_element_by_id('productPendingEl').text)
        #     # print(u'抓取产品总数')
        #     # total = int(selenium.find_element_by_id('productTotalEl').text)
        #     i = 1
        #     sleep(2)
        #     while pending > 0:
        #         print('点击查看订单明细')
        #         selenium.find_element_by_css_selector('input[value="查看订单明细"]').click()
        #         sleep(2)
        #         print('获取产品编码: %d' % i)
        #         product_code = selenium.find_element_by_id('reCheckRecords:' + str(i-1) + ':j_id701').text
        #         print('获取未检货数量: %d' % i)
        #         number = int(selenium.find_element_by_id('reCheckRecords:' + str(i-1) + ':j_id698').text)
        #         print(number)
        #         print('点击关闭窗口按钮')
        #         selenium.find_element_by_id('hidelink').click()
        #         sleep(1)
        #         print('输入产品编码')
        #         selenium.find_element_by_id('newProductBarCode').send_keys(product_code)
        #         print('输入回车键')
        #         selenium.find_element_by_id('newProductBarCode').send_keys(Keys.ENTER)
        #         sleep(1)
        #         print('输入产品个数')
        #         sleep(2)
        #         selenium.find_element_by_id('newProductNumber').clear()
        #         selenium.find_element_by_id('newProductNumber').send_keys(number)
        #         print('输入回车键')
        #         selenium.find_element_by_id('newProductNumber').send_keys(Keys.ENTER)
        #         sleep(1)
        #         i += 1
        #         pending = pending - number
        #         sleep(4)
        #         if pending == 0:
        #             print('点击确认按钮')
        #             selenium.switch_to_alert().accept()
        #     try:
        #         print('输入发票号码')
        #         selenium.find_element_by_id('invoiceInput').send_keys('I001')
        #         sleep(2)
        #         print('输入回车键')
        #         selenium.find_element_by_id('invoiceInput').send_keys(Keys.ENTER)
        #         sleep(3)
        #     except:
        #         pass
        #     # 判断是不是昆山仓，如果是需要输入箱子数量
        #     if warehouse_id == '15':
        #         print('输入数量')
        #         selenium.find_element_by_id('confirmCartonQtyPanelSubview:cartonQtyInput').send_keys('1')
        #     sleep(3)
        #     print('点击完成按钮')
        #     selenium.find_element_by_id('confirmCartonQtyPanelSubview:confirmPackedNumForm:doConfirmCartonQtyBtn').click()
        #     sleep(3)

        # clickJS = 'setTimeout(function(){document.getElementById("buttonToolForm:j_id239").click()},100)';
        # selenium.execute_script(clickJS)
        # sleep(3)
        # handle = selenium.current_window_handle
        # print('查询核检记录')
        # clickJS = 'setTimeout(function(){document.getElementById("queryReCheckLink").click()},100)';
        # selenium.execute_script(clickJS)
        # sleep(3)
        # print('挑选窗口')
        # all_handles = selenium.window_handles
        # for h in all_handles:
        #     if h != handle:
        #         selenium.switch_to_window(h)
        #         break
        # sleep(3)
        # print('输入发货单号')
        # selenium.find_element_by_id('searchForm:orderNo').send_keys(do_num)
        # print('点击查询按钮')
        # selenium.find_element_by_id('submitBtn').click()
        # sleep(2)
        # print('获取箱号')
        # carton_no = selenium.find_element_by_css_selector('a[href="javascript:void(0)"]').text
        # selenium.close()
        # selenium.switch_to_window(handle)
        # return carton_no

    def outbound_handover(self, carton_no):
        """出库管理-出库交接"""
        print('打开出库交接页面')
        self.driver.get('http://10.6.80.248:8080/delivery/entruckLoadingList.xhtml')
        sleep(1)
        main_handle = self.driver.current_window_handle
        print('主窗口是' + main_handle)
        print('点击DO人工交接')
        self.find_element(R.Handover.do_manual_handover).click()
        # self.find_element_by_xpath("//form[@id='buttonToolForm']/span[10]/span/a").click()
        all_handles = self.driver.window_handles
        for other_handle in all_handles:
            if other_handle != main_handle:
                self.driver.switch_to_window(other_handle)
                break
        secondary_handle = self.driver.current_window_handle
        print('次级窗口是' + secondary_handle)
        print('点击保存')
        self.find_element(R.Handover.save_button).click()
        # self.find_element_by_xpath("//form[@id='addForm']/table/tbody/tr[2]/td/div/input[1]").click()
        # selenium.find_element_by_css_selector('[class="btnCla"][value="保存"]').click()
        sleep(2)
        self.send_keys(R.Handover.carton_no, carton_no)
        # self.driver.find_element_by_id('addDetailForm:carrierNo').clear()
        # self.driver.find_element_by_id('addDetailForm:carrierNo').send_keys(carton_no)
        self.driver.find_element_by_id('addDetailForm:carrierNo').send_keys(Keys.ENTER)
        sleep(2)
        print('点击关闭交接单')
        self.find_element(R.Handover.close_button).click()
        # self.find_element_by_xpath("//form[@id='addForm']/table/tbody/tr[2]/td/div/input[4]").click()
        # selenium.find_element_by_css_selector('[class="btnCla"][value="关闭交接单"]').click()
        self.driver.switch_to_alert().accept()
        sleep(1)
        self.driver.switch_to_alert().accept()
        sleep(1)
        self.driver.switch_to_window(main_handle)
        sleep(1)
        self.find_element(R.Handover.search_button).click()
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(2)
        handover_status = self.find_element(R.Handover.handover_status).text
        # handover_status = self.find_element_by_xpath("//div[@id='loadForm:dataDiv']/table/tbody/tr/td[4]").text
        # handover_status = selenium.find_element_by_id('loadForm:j_id309:0:j_id320').text
        print('交接状态是' + handover_status)
        return handover_status

        # clickJS = 'setTimeout(function(){document.getElementById("buttonToolForm:j_id239").click()},100)';
        # selenium.execute_script(clickJS)
        # sleep(3)
        # print('挑选窗口')
        #
        # all_handles = selenium.window_handles
        # for h in all_handles:
        #     if h != handle:
        #         selenium.switch_to_window(h)
        #         break
        # sleep(3)
        # print('点'u'击保存按钮')
        #
        # selenium.find_element_by_id('addForm:j_id97').click()
        # sleep(2)
        # print('输入箱号')
        # selenium.find_element_by_id('addDetailForm:carrierNo').send_keys(carton_no)
        # sleep(2)
        # print('输入回车键')
        # selenium.find_element_by_id('addDetailForm:carrierNo').send_keys(Keys.ENTER)
        # sleep(2)
        # print('点击关闭交接单')
        # selenium.find_element_by_id('addForm:j_id98').click()
        # sleep(2)
        # print('点击确认按钮')
        # selenium.switch_to_alert().accept()
        # sleep(3)
        # print('点击确认按钮')
        # selenium.switch_to_alert().accept()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    testOut = Warehouse_outbound(driver)
    testOut.outbound_process('13', '7029625910', 'true')


    # DO单号
    # do_num = "7029627717"
    # # 仓库编码，广东药城为13，重庆药城20，药网暂用天津仓10
    # warehouse_id = "13"
    # # 是否为药城订单，药城填true，药网填false
    # isYCorder = 'True'
    #
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.implicitly_wait(20)
    #
    # print('登录')
    # outbound_login(driver, warehouse_id)
    #
    # print('订单分配')
    # order_dispatch_status = outbound_order_distribution(driver, do_num)
    # print(order_dispatch_status)
    # assert "分配成功" in order_dispatch_status
    #
    # print('波次生成')
    # wave_status = outbound_wave_generation(driver, do_num, isYCorder)
    # print(wave_status)
    # assert "波次生成成功" in wave_status
    #
    # print('波次计划')
    # wave_id = wave_status.split(":")[1]
    # pick_id = outbound_wave_plan(driver, wave_id, isYCorder)
    # assert pick_id != None
    #
    # print('拣货确认')
    # assert '操作成功' in outbound_pick_confirm(driver, pick_id)
    #
    # print('分拣')
    # assert '分拣成功' in outbound_sorting(driver, wave_id)
    #
    # print('核拣装箱')
    # carton_no = outbound_encasement(driver, do_num)
    # assert carton_no != None
    #
    # print('出库交接')
    # # carton_no = '7029627717'
    # handover_status = outbound_handover(driver, carton_no)
    # assert '已发货' in handover_status
    #
    # print('出库完成，关闭浏览器')
    # driver.quit()
