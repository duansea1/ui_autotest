"""
Created on 2019/3/13
@author: liya
"""

import requests


class Pms_Job(object):


    def pms_rtv_job(self):
        """rtv-asn推送WMSjob"""
        url = 'http://pms.111.com.cn/service/kingbos/sendRtvToDts.json?oper=qaTestUser'
        r = requests.get(url)
        print(r.text)

    def pms_po_job(self):
        """po-asn推送WMSjob"""
        url = 'http://pms.111.com.cn/service/kingbos/sentAsnToDts.json?oper=qaTestUser'
        r = requests.get(url)
        print(r.text)

    def pms_to_job(self):
        """to-asn推送WMSjob"""
        url = 'http://pms.111.com.cn/service/kingbos/sendTranToDts.json?oper=qaTestUser'
        r = requests.get(url)
        print(r.text)

