"""
Created on 2018.12.27

Author: whb

"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from business.BasePage import Base
from business import inbound_resource as R


class Warehouse_inbound(Base):

    def inbound_process(self, ASN_num, warehouse_id):
        """通用方法"""
        # self = webdriver.Chrome()
        self.driver.maximize_window()
        # 登陆
        home_URL = self.inbound_login(warehouse_id)
        assert 'home.xhtml' in home_URL

        # ASN状态查询
        ASN_info = self.inbound_ASNstatus(ASN_num)
        ASN_type = ASN_info[0]
        print('ASN类型为' + ASN_type)
        ASN_status = ASN_info[1]
        print('ASN状态为' + ASN_status)
        if 'DO退货' in ASN_type:
            if '初始化' in ASN_status:
                # 入库管理-验收
                accept_message = self.inbound_accpet_DOreturned(ASN_num, ASN_type)
                print(accept_message)
                if '操作成功' in accept_message:
                    # 入库管理-上架
                    on_shelves_status = self.inbound_on_shelves(ASN_num)
                    print(on_shelves_status)
                    if '已完成' in on_shelves_status:
                        # 入库管理-ASN审核
                        ASN_status = self.inbound_aduit(ASN_num, ASN_type)
                        print(ASN_status)
                        if '完成' in ASN_status:
                            print('入库完成，关闭浏览器')
                            self.driver.quit()
                        else:
                            assert print('审核失败！')
                    else:
                        assert print('上架失败！')
                else:
                    assert print('验收失败！')

            elif '验收完成' in ASN_status:
                # 入库管理-ASN审核
                ASN_status = self.inbound_aduit(ASN_num, ASN_type)
                print(ASN_status)
                if '完成' in ASN_status:
                    # 入库管理-上架
                    on_shelves_status = self.inbound_on_shelves(ASN_num)
                    print(on_shelves_status)
                    if '已完成' in on_shelves_status:
                        print('入库完成，关闭浏览器')
                        self.driver.quit()
                    else:
                        print('上架失败！')
                else:
                    print('审核失败！')

            elif '审核完成' in ASN_status:
                # 入库管理-上架
                on_shelves_status = self.inbound_on_shelves(ASN_num)
                print(on_shelves_status)
                if '已完成' in on_shelves_status:
                    print('入库完成，关闭浏览器')
                    self.driver.quit()
                else:
                    assert print('上架失败！')

            else:
                assert print('ASN状态异常')

        elif '正品' in ASN_type:
            if '初始化' in ASN_status:
                # 入库管理-收货
                receive_message = self.inbound_receive(ASN_num)
                if '操作成功' in receive_message:
                    # 入库管理-验收
                    accept_message = self.inbound_accpet_DOreturned(ASN_num, ASN_type)
                    print(accept_message)
                    if '操作成功' in accept_message:
                        # 入库管理-上架
                        on_shelves_status = self.inbound_on_shelves(ASN_num)
                        print(on_shelves_status)
                        if '已完成' in on_shelves_status:
                            # 入库管理-ASN审核
                            ASN_status = self.inbound_aduit(ASN_num, ASN_type)
                            print(ASN_status)
                            if '完成' in ASN_status:
                                print('入库完成，关闭浏览器')
                                self.driver.quit()
                            else:
                                assert print('审核失败！')
                        else:
                            assert print('上架失败！')
                    else:
                        assert print('验收失败！')
            elif '验收完成' in ASN_status:
                # 入库管理-ASN审核
                ASN_status = self.inbound_aduit(ASN_num, ASN_type)
                print(ASN_status)
                if '完成' in ASN_status:
                    # 入库管理-上架
                    on_shelves_status = self.inbound_on_shelves(ASN_num)
                    print(on_shelves_status)
                    if '已完成' in on_shelves_status:
                        print('入库完成，关闭浏览器')
                        self.driver.quit()
                    else:
                        assert print('上架失败！')
                else:
                    assert print('审核失败！')

            elif '审核完成' in ASN_status:
                # 入库管理-上架
                on_shelves_status = self.inbound_on_shelves(ASN_num)
                print(on_shelves_status)
                if '已完成' in on_shelves_status:
                    print('入库完成，关闭浏览器')
                    self.driver.quit()
                else:
                    assert print('上架失败！')
            else:
                assert print('ASN状态异常')
        elif '调拨' in ASN_type:
            if '初始化' in ASN_status:
                # 入库管理-验收
                accept_message = self.inbound_accpet_DOreturned(ASN_num, ASN_type)
                print(accept_message)
                if '操作成功' in accept_message:
                    # 入库管理-上架
                    on_shelves_status = self.inbound_on_shelves(ASN_num)
                    print(on_shelves_status)
                    if '已完成' in on_shelves_status:
                        # 入库管理-ASN审核
                        ASN_status = self.inbound_aduit(ASN_num, ASN_type)
                        print(ASN_status)
                        if '完成' in ASN_status:
                            print('入库完成，关闭浏览器')
                            self.driver.quit()
                        else:
                            assert print('审核失败！')
                    else:
                        assert print('上架失败！')
                else:
                    assert print('验收失败！')
        else:
            assert print('现仅支持DO退货&正品&调拨入库，其他类型待开发')

        return

    def inbound_login(self, warehouse_id):
        """登陆仓库管理系统"""
        print('打开仓储管理系统')
        self.driver.get('http://10.6.80.248:8080/login.xhtml')
        self.wait_until_display(R.Login.login_button)
        sleep(2)
        print('输入用户名' + R.user_name)
        self.send_keys(R.Login.user_name, R.user_name)
        print('输入密码' + R.user_password)
        self.send_keys(R.Login.password, R.user_password)
        sleep(2)
        print('选择仓库id=' + warehouse_id)
        # sel = self.driver.find_element_by_id('loginForm:warehouse')
        # Select(sel).select_by_value(warehouse_value)
        selector = Select(self.find_element(R.Login.warehouse))
        selector.select_by_value(warehouse_id)
        sleep(2)
        print('点击登录按钮，进入仓储管理系统')
        self.find_element(R.Login.login_button).click()
        # print('已选择的仓库' + selector.first_selected_option().text)
        # self.driver.find_element_by_id('loginForm:submitBtn').click()
        # print('打开仓库管理系统')
        # self.get('http://10.6.80.248:8080/login.xhtml')
        # sleep(2)
        # print('输入用户名' + user_name)
        # self.driver.find_element_by_id('loginForm:userName').clear()
        # self.driver.find_element_by_id('loginForm:userName').send_keys(user_name)
        # print('输入密码' + user_password)
        # self.driver.find_element_by_id('loginForm:password').clear()
        # self.driver.find_element_by_id('loginForm:password').send_keys(user_password)
        # sleep(1)
        # print('选择仓库' + warehouse_id)
        # selector = Select(self.driver.find_element_by_id('loginForm:warehouse'))
        # selector.select_by_value(warehouse_id)
        # print('点击登录')
        # self.driver.find_element_by_id('loginForm:submitBtn').click()
        # sleep(2)
        print('跳转首页')
        return self.driver.current_url

    def inbound_ASNstatus(self, ASN_num):
        """入库管理-ASN查询"""
        print('进入入库管理-ASN查询')
        self.driver.get('http://10.6.80.248:8080/receive/asnList.xhtml')
        sleep(1)
        print('输入ASN编号查询' + ASN_num)
        self.send_keys(R.ASNQuery.ASN_input, ASN_num)
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").send_keys(ASN_num)
        # self.find_element_by_name('searchForm:j_id290').clear()
        # self.find_element_by_name('searchForm:j_id290').send_keys(ASN_num)
        self.find_element(R.ASNQuery.search_button).click()
        sleep(2)
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        result = self.find_elements(R.ASNQuery.result)
        if len(result) == 0:
            print('无查询结果')
        else:
            ASN_info = []
            # ASN类型
            ASN_info.append(self.find_element(R.ASNQuery.ASN_type).text)
            # ASN状态
            ASN_info.append(self.find_element(R.ASNQuery.ASN_status).text)
            return ASN_info

    def inbound_receive(self, ASN_num):
        """入库管理-收货"""
        print('入库管理-收货')
        self.driver.get('http://10.6.80.248:8080/receive/compReceiveEntity.xhtml')
        sleep(1)
        print('输入ASN编码' + ASN_num)
        # self.driver.find_element_by_id('searchForm:asnNo').clear()
        # self.driver.find_element_by_id('searchForm:asnNo').send_keys(ASN_num)
        self.send_keys(R.Receive.ASN_input, ASN_num)
        self.find_element(R.Receive.search_button).click()
        # self.driver.find_element_by_id('searchForm:btnQuery1').click()
        sleep(2)
        result = self.find_elements(R.Receive.result)
        if len(result) == 0:
            print('无查询结果')
        else:
            print('输入批号')
            self.send_keys(R.Receive.batch_no, 'autoscript001')
            self.find_element(R.Receive.batch_no).send_keys(Keys.ENTER)
            print('选择生产日期')
            self.find_element(R.Receive.production_date).click()
            print('选择有效期')
            self.find_element(R.Receive.production_date).click()
            print('输入随货同行单号')
            self.send_keys(R.Receive.consignment_no, 'autoscript002')
            expected_qty = self.find_element(R.Receive.expected_qty).text
            print('输入实收数' + expected_qty)
            self.send_keys(R.Receive.received_qty, expected_qty)
            sleep(1)
            self.send_keys(R.Receive.refer_price, '100')
            sleep(1)
            print('点击完成收货')
            # # self.driver.find_element_by_id('searchForm:receiveBtn').click()
            self.find_element(R.Receive.receive_button).click()
            sleep(1)
            # return self.find_element_by_class_name('rich-messages-label').text
            return self.find_element(R.Normal.message).text

    def inbound_accpet_DOreturned(self, ASN_num, ASN_type):
        """入库管理-验收(DO退货)"""
        print('入库管理-验收')
        self.driver.get('http://10.6.80.248:8080/receive/receiveEntity.xhtml')
        print('输入ASN编码' + ASN_num)
        self.send_keys(R.Accept.ASN_input, ASN_num)
        # self.driver.find_element_by_id('searchForm:asnNo').clear()
        # self.driver.find_element_by_id('searchForm:asnNo').send_keys(ASN_num)
        print('点击查询')
        # self.driver.find_element_by_id('searchForm:btnQuery1').click()
        self.find_element(R.Accept.search_button).click()
        sleep(2)
        if ASN_type == 'DO退货':
            try:
                # self.driver.find_element_by_id('invoiceForm:noInvoiceBtn').click()
                self.find_element(R.Accept.no_invoice_button).click()
            except:
                pass
        # 有无发票不影响业务流程
        # print('是否为药城售后：' + isYCservice)
        # try:
        #     if isYCservice == '1':
        #         self.driver.find_element_by_id('invoiceForm:j_id744').click()
        #     else:
        #         self.driver.find_element_by_id('invoiceForm:noInvoiceBtn').click()
        # except:
        #     pass
        sleep(2)
        main_handle = self.driver.current_window_handle
        print('主窗口是' + main_handle)
        print('点击ASN超链接')
        # self.driver.find_element_by_id('searchForm:j_id253').click()
        # self.find_element_by_xpath(
        #     "//div[@id='searchForm:searchArea']/div[1]/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/a").click()
        self.find_element(R.Accept.ASN_link).click()
        all_handles = self.driver.window_handles
        for other_handle in all_handles:
            if other_handle != main_handle:
                self.driver.switch_to_window(other_handle)
                break
        secondary_handle = self.driver.current_window_handle
        print('次级窗口是' + secondary_handle)

        trs = self.driver.find_element_by_id('saveForm:p2:tb').find_elements_by_tag_name('tr')
        product_id = []
        receive_qty = []
        ASN_row_status = []
        for tr in trs:
            product_id.append(tr.find_elements_by_tag_name('td')[8].text)
        for tr in trs:
            receive_qty.append(tr.find_elements_by_tag_name('td')[13].text)
        for tr in trs:
            ASN_row_status.append(tr.find_elements_by_tag_name('td')[2].text)
        print('产品数量为' + str(len(trs)))
        print('产品编码为' + str(product_id))
        print('应收数量为' + str(receive_qty))
        print('ASN列状态为' + str(ASN_row_status))
        self.driver.close()
        self.driver.switch_to_window(main_handle)
        sleep(1)

        """循环确认收货"""
        for i in range(0, len(trs), 1):
            if ASN_row_status[i] == '初始化':
                print('确认收货第' + str(i) + '件')
                self.send_keys(R.Accept.product_barcode, product_id[i])
                # self.driver.find_element_by_id('searchForm:productBarcode').clear()
                # self.driver.find_element_by_id('searchForm:productBarcode').send_keys(product_id[i])
                self.find_element(R.Accept.product_barcode).send_keys(Keys.ENTER)
                # self.send_keys(R.Accept.product_barcode, Keys.ENTER)
                sleep(3)
                try:
                    remove_reset_JS = "document.getElementById('searchForm:ajForm:skuImageColse').removeAttribute('reset')"
                    self.driver.execute_script(remove_reset_JS)
                    sleep(1)
                    # self.driver.find_element_by_id('searchForm:ajForm:skuImageColse').click()
                    self.find_element(R.Accept.close_image).click()
                    sleep(1)
                    self.find_element(R.Accept.product_address).send_keys('TEST')
                except:
                    pass
                # self.driver.switch_to_alert().accept()
                # 判断ASN类型
                if ASN_type == '正品':
                    self.find_element(R.Accept.lpn_no).send_keys(Keys.ENTER)
                    sleep(1)
                    try:
                        self.find_element(R.Accept.product_address).send_keys('TEST')
                    except:
                        pass
                else:
                    print('输入验收数量' + str(receive_qty))
                    # self.driver.find_element_by_id('searchForm:qty').clear()
                    # self.driver.find_element_by_id('searchForm:qty').send_keys(receive_qty[i])
                    self.send_keys(R.Accept.receive_qty, receive_qty[i])
                    sleep(1)
                    # 可能会弹出商品图片
                    try:
                        remove_reset_JS = "document.getElementById('searchForm:ajForm:skuImageColse').removeAttribute('reset')"
                        self.driver.execute_script(remove_reset_JS)
                        sleep(1)
                        # self.driver.find_element_by_id('searchForm:ajForm:skuImageColse').click()
                        self.find_element(R.Accept.close_image).click()
                        sleep(1)
                        self.driver.find_element_by_id('searchForm:qty').send_keys(receive_qty[i])
                        sleep(1)
                    except:
                        pass
                    self.find_element(R.Accept.receive_qty).send_keys(Keys.ENTER)
                    # self.find_element(R.Accept.product_address).send_keys('TEST')
                    # self.driver.find_element_by_id('searchForm:qty').send_keys(Keys.ENTER)
                    sleep(1)
                    main_handle = self.driver.current_window_handle
                    print('选择生产日期，默认为今天')
                    # self.find_element_by_css_selector("div#_c_ctrl_1>input.year").click()
                    # js = 'document.getElementsByName("xx").style.display="block";'
                    # driver.execute_script(js)
                    self.driver.find_element_by_css_selector(
                        "[class='myCalendar'][style^='display: block']").find_element_by_css_selector(
                        "div.container>div.mainPanel>div.date>span.focusCell>a").click()
                    # local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    # self.find_elements_by_id('_c_ctrl_1')[i].send_keys(local_time)
                    sleep(2)
                    print('有效时间、批号、随货同行单、LPN 回车')
                    # self.find_elements_by_id('_c_ctrl_2')[i].send_keys(Keys.ENTER)
                    # self.find_element_by_css_selector("div#_c_ctrl_2>input.year").send_keys(Keys.ENTER)
                    self.driver.find_element_by_css_selector(
                        "[class='myCalendar'][style^='display: block']").find_element_by_css_selector(
                        "div.container>div.mainPanel>div.date>span.focusCell>a").click()
                    # self.driver.switch_to_window(main_handle)
                    sleep(1)
                    self.find_element(R.Accept.batch_no).send_keys('test')
                    self.find_element(R.Accept.batch_no).send_keys(Keys.ENTER)
                    # self.driver.find_element_by_class_name('batchNo').send_keys(Keys.ENTER)
                    sleep(1)
                    self.find_element(R.Accept.refer_no).send_keys(Keys.ENTER)
                    # self.driver.find_element_by_id('searchForm:referNo').send_keys(Keys.ENTER)
                    sleep(1)
                    self.find_element(R.Accept.lpn_no).send_keys(Keys.ENTER)
                    # self.driver.find_element_by_id('searchForm:lpn').send_keys(Keys.ENTER)
                    sleep(1)
                try:
                    # self.driver.find_element_by_id('fullBox').click()
                    self.find_element(R.Accept.full_box).click()
                    sleep(5)
                except:
                    pass

                # 确认是否收货成功
                # print('点击ASN超链接')
                # self.driver.find_element_by_id('searchForm:j_id253').click()
                # all_handles = self.driver.window_handles
                # for other_handle in all_handles:
                #   if other_handle != main_handle:
                #       self.driver.switch_to_window(other_handle)
                #       break
                # secondary_handle = self.driver.current_window_handle
                # print('次级窗口是' + secondary_handle)
                # tbody = self.driver.find_element_by_id('saveForm:p2:tb')
                # accept_status = tbody.find_elements_by_tag_name('tr')[i].find_elements_by_name('td')[2].text
                # try:
                #     '验收成功' in accept_status
                # except AssertionError:
                #     print('验收失败')
                # self.driver.close()
                # self.driver.switch_to_window(main_handle)
                # sleep(1)

        # 所有商品验收完成会有审核弹框，部分验收不会弹
        try:
            all_handles = self.driver.window_handles
            for other_handle in all_handles:
                if other_handle != main_handle:
                    self.driver.switch_to_window(other_handle)
                    break
            sleep(1)
            secondary_handle = self.driver.current_window_handle
            print('次级窗口是' + secondary_handle)
            print('点击关闭')
            # 712100001631
            self.find_element(R.Accept.close_aduit_window).click()
            # self.find_element_by_xpath("//div[@id='saveForm:operDiv']/input[2]").click()
            # self.driver.find_element_by_id('saveForm:j_id22').click()
            self.driver.switch_to_alert().accept()
            self.driver.close()
            sleep(1)
            self.driver.switch_to_window(main_handle)
            sleep(1)
        except:
            pass
        self.driver.switch_to_window(main_handle)
        sleep(1)
        print('点击上架发布')
        self.find_element(R.Accept.release_button).click()
        # self.driver.find_element_by_id('searchForm:releaseBtn').click()
        self.driver.switch_to_alert().accept()
        sleep(3)
        return self.find_element(R.Normal.message).text

    # def inbound_accept_purchasing(self, ASN_num):
    #     """入库管理-验收(正采)"""
    #     # 712100001502
    #     print('入库管理-验收')
    #     self.driver.get('http://10.6.80.248:8080/receive/receiveEntity.xhtml')
    #     print('输入ASN编码' + ASN_num)
    #     self.send_keys(R.Accept.ASN_input, ASN_num)
    #     # self.driver.find_element_by_id('searchForm:asnNo').clear()
    #     # self.driver.find_element_by_id('searchForm:asnNo').send_keys(ASN_num)
    #     print('点击查询')
    #     # self.driver.find_element_by_id('searchForm:btnQuery1').click()
    #     self.find_element(R.Accept.search_button).click()
    #     sleep(2)
    #     return

    def inbound_on_shelves(self, ASN_num):
        """入库管理-上架"""
        print('进入入库管理-上架')
        self.driver.get('http://10.6.80.248:8080/receive/putawayList.xhtml')
        sleep(1)
        print('输入ASN编号查询' + ASN_num)
        # self.driver.find_element_by_id('searchForm:asnNo').clear()
        # self.driver.find_element_by_id('searchForm:asnNo').send_keys(ASN_num)
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        self.send_keys(R.OnShelves.ASN_input, ASN_num)
        self.find_element(R.OnShelves.search_button).click()
        sleep(2)
        result = self.find_elements(R.OnShelves.result)
        if len(result) == 0:
            print('无查询结果')
        else:
            main_handle = self.driver.current_window_handle
            print('主窗口是' + main_handle)
            # if '已发布' in self.find_element_by_xpath("//div[@id='selectForm:dataDiv']/table/tbody/tr/td[3]").text:
            if '已发布' in self.find_element(R.OnShelves.onshelves_status).text:
                print('点击上架单号')
                # css选择器路径内有:容易报错
                # self.find_element_by_css_selector('div#selectForm:j_id273:0:j_id284>a')
                # self.find_element_by_css_selector('div[id=selectForm:j_id273:0:j_id284]')
                # self.driver.find_element_by_id('selectForm:j_id273:0:j_id284').find_element_by_tag_name('a').click()
                # self.find_element_by_xpath(
                #     "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/div/a").click()
                self.find_element(R.OnShelves.onshelves_num).click()
                sleep(2)
                all_handles = self.driver.window_handles
                for secordary_handle in all_handles:
                    if secordary_handle != main_handle:
                        self.driver.switch_to_window(secordary_handle)
                        break
                print('次级窗口是' + secordary_handle)
                print('勾选全选')
                # if self.driver.find_element_by_id('saveForm:dataTable:j_id45header:sortDiv').find_element_by_tag_name('input').is_selected() is False:
                #     self.driver.find_element_by_id('saveForm:dataTable:j_id45header:sortDiv').find_element_by_tag_name('input').click()
                # if self.find_element_by_xpath(
                #         "//tr[@class='rich-table-subheader ']/th[1]/div/input").is_selected() is False:
                #     self.find_element_by_xpath("//tr[@class='rich-table-subheader ']/th[1]/div/input").click()
                if self.find_element(R.OnShelves.all_selected).is_selected() is False:
                    self.find_element(R.OnShelves.all_selected).click()
                    sleep(1)
                # 确认上架，如失败则强制上架
                try:
                    print('点击确认上架')
                    self.find_element(R.OnShelves.confirm_onshelves).click()
                    # self.find_element_by_xpath("//div[@id='saveForm:operDiv']/input[2]").click()
                    # self.driver.find_element_by_id('saveForm:j_id18').click()
                    sleep(1)
                    self.driver.switch_to_alert().accept()
                    sleep(1)
                    on_shelves_status = self.find_element(R.Normal.message).text
                    # on_shelves_status = self.find_element_by_class_name('rich-messages-label').text
                    if '操作成功' not in on_shelves_status:
                        if self.find_element(R.OnShelves.onshelves_message).is_selected() is False:
                            self.find_element(R.OnShelves.onshelves_message).click()
                        # if self.driver.find_element_by_xpath(
                        #         "//tr[@class='rich-table-subheader']/th[1]/div/input").is_selected() is False:
                        #     self.driver.find_element_by_xpath("//tr[@class='rich-table-subheader']/th[1]/div/input").click()
                        # self.driver.find_element_by_id('saveForm:dataTable:j_id45header:sortDiv').is_selected() is False
                        # self.driver.find_element_by_id('saveForm:dataTable:j_id45header:sortDiv').is_selected()
                        sleep(1)
                        print('点击强制上架')
                        self.find_element(R.OnShelves.force_onshelves).click()
                        # self.find_element_by_xpath("//div[@id='saveForm:operDiv']/input[3]").click()
                        # self.driver.find_element_by_id('saveForm:j_id19').click()
                        sleep(1)
                        self.driver.switch_to_alert().accept()
                        on_shelves_status = self.find_element(R.Normal.message).text
                        # on_shelves_status = self.find_element_by_class_name('rich-messages-label').text
                        if '操作成功' not in on_shelves_status:
                            print('强制上架失败！')
                        sleep(1)
                        # on_shelves_status = self.find_element_by_class_name('rich-messages-label')
                        # try:
                        #     '操作成功' in on_shelves_status
                        # except AssertionError:
                        #     print('操作失败')
                except:
                    pass

                print('点击关闭')
                self.find_element(R.OnShelves.close_onshelves_window).click()
                # self.find_element_by_xpath("//div[@id='saveForm:operDiv']/input[6]").click()
                # self.driver.find_element_by_id('saveForm:j_id22').click()
                self.driver.switch_to_window(main_handle)
                sleep(1)
                print('再次查询')
                self.find_element(R.OnShelves.search_button).click()
                # self.driver.find_element_by_id('searchForm:btnQuery').click()
                sleep(1)
                return self.find_element(R.OnShelves.onshelves_status).text
                # return self.find_element_by_xpath("//div[@id='selectForm:dataDiv']/table/tbody/tr[1]/td[3]").text
                # self.driver.find_element_by_id('selectForm:j_id273:0:j_id288').text

            else:
                return self.find_element(R.OnShelves.onshelves_status).text
                # return self.find_element_by_xpath("//div[@id='selectForm:dataDiv']/table/tbody/tr/td[3]").text

    def inbound_aduit(self, ASN_num, ASN_type):
        """入库管理-ASN审核"""
        print('进入入库管理-ASN查询')
        self.driver.get('http://10.6.80.248:8080/receive/asnList.xhtml')
        sleep(1)
        print('输入ASN编号查询' + ASN_num)
        self.send_keys(R.Aduit.ASN_input, ASN_num)
        self.find_element(R.Aduit.search_button).click()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").clear()
        # self.find_element_by_xpath("//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input").send_keys(ASN_num)
        # self.find_element_by_name('searchForm:j_id290').clear()
        # self.find_element_by_name('searchForm:j_id290').send_keys(ASN_num)
        # self.driver.find_element_by_id('searchForm:btnQuery').click()
        sleep(2)
        result = self.find_elements(R.ASNQuery.result)
        if len(result) == 0:
            print('无查询结果')
        else:
            main_handle = self.driver.current_window_handle
            print('主窗口是' + main_handle)
            print('点击ASN编号')
            self.find_element(R.Aduit.ASN_num).click()
            # self.find_element_by_xpath("//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/a").click()
            # self.driver.find_element_by_id('selectForm:detailTable:0:j_id403').click()
            sleep(1)
            all_handles = self.driver.window_handles
            for secordary_handle in all_handles:
                if secordary_handle != main_handle:
                    self.driver.switch_to_window(secordary_handle)
                    break
            print('次级窗口是' + secordary_handle)
            print('点击审核')
            if ASN_type == '正品':
                self.find_element(R.Aduit.aduit_button_purchasing).click()
            else:
                self.find_element(R.Aduit.aduit_button).click()
            # self.find_element_by_xpath("//div[@id='saveForm:operDiv']/input[3]").click()
            # self.driver.find_element_by_id('saveForm:j_id24').click()
            self.driver.switch_to_alert().accept()
            sleep(1)
            # ASN_detail_status = self.find_element_by_class_name('rich-messages-label').text
            ASN_detail_status = self.find_element(R.Normal.message).text
            try:
                '操作成功' in ASN_detail_status
            except AssertionError:
                print('操作失败')
            if ASN_type == '正品':
                self.find_element(R.Aduit.aduit_button_purchasing).click()
            else:
                self.find_element(R.Aduit.close_button).click()
            # self.find_element_by_xpath("//div[@id='saveForm:operDiv']/input[5]").click()
            # self.driver.find_element_by_id('saveForm:j_id26')
            self.driver.close()
            self.driver.switch_to_window(main_handle)
            sleep(1)
            print('再次查询')
            self.find_element(R.Aduit.search_button).click()
            # self.driver.find_element_by_id('searchForm:btnQuery').click()
            sleep(1)
            return self.find_element(R.ASNQuery.ASN_status).text
            # return self.driver.find_element_by_id('selectForm:detailTable:0:asnStatus').text

if __name__ == '__main__':
    driver = webdriver.Chrome()
    testIn = Warehouse_inbound(driver)
    testIn.inbound_process('712100001707', '13')
    # ASN编码
    # ASN_num = '200001108686'
    # # 仓库编号，广东药城为13，重庆药城20，天津药网10，昆山药网15
    # warehouse_id = '15'
    #
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.implicitly_wait(20)
    #
    # # 登陆
    # user_name = 'admin'
    # user_password = 'admin123'
    # home_URL = inbound_login(driver, user_name, user_password, warehouse_id)
    # assert 'home.xhtml' in home_URL
    #
    # # #入库管理-收货
    # # receive_message = inbound_receive(driver, ASN_num)
    # # print(receive_message)
    # # assert '操作成功' in receive_message
    #
    # # 入库管理-验收
    # accept_message = inbound_accpet_DOreturned(driver, ASN_num)
    # print(accept_message)
    # assert '操作成功' in accept_message
    #
    # # 入库管理-上架
    # on_shelves_status = inbound_on_shelves(driver, ASN_num)
    # print(on_shelves_status)
    # assert '已完成' in on_shelves_status
    #
    # # 入库管理-ASN审核
    # ASN_status = inbound_aduit(driver, ASN_num)
    # print(ASN_status)
    # assert '完成' in ASN_status
    #
    # print('入库完成，关闭浏览器')
    # driver.quit()