'''
Created on 2019年1月18日

@author: geqiuli
'''
from business.warehouse_sys.outbound_process import Warehouse_outbound
import pytest

@pytest.mark.test_do_out
def test_do_outbound(selenium,warehouse_id,do_num,is_yc_order):
    '''DO 单号，完成出库流程'''
    wms=Warehouse_outbound(selenium)
    wms.outbound_process(warehouse_id, do_num, is_yc_order)


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'test_do_out',driver='Chrome')