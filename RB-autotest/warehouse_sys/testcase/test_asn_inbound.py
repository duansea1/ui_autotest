'''
Created on 2019年1月18日

@author: geqiuli
'''
from business.inbound_process import Warehouse_inbound
import pytest

@pytest.mark.test_asn_in
def test_asn_inbound(selenium,asn_num,warehouse_id):
    '''ASN 单号，完成入库流程'''
    wms=Warehouse_inbound(selenium)
    wms.inbound_process(asn_num, warehouse_id)



if __name__ == '__main__':
    from public import tools
    tools.runtc(__file__,'test_asn_in',driver='Chrome',
                options=['--warehouse_id=13','--asn_num=712099996398'])