'''
Created on 2019年1月18日

@author: geqiuli
'''
from business.warehouse_sys.inbound_process import Warehouse_inbound
import pytest

@pytest.mark.test_asn_in
def test_do_outbound(selenium,asn_num,warehouse_id):
    '''DO 单号，完成出库流程'''
    wms=Warehouse_inbound(selenium)
    wms.inbound_process(warehouse_id, asn_num, warehouse_id)

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'test_asn_in',driver='Chrome')