'''
Created on 2019年1月18日

@author: geqiuli
'''

"""出库类型为2-调拨出库，3-RTV退货时，is_yc_order=False"""


from business.outbound_process import Warehouse_outbound
import pytest

@pytest.mark.test_do_out
def test_do_outbound(selenium,warehouse_id,do_num,is_yc_order,outbound_type):
    '''DO 单号，完成出库流程'''
    wms=Warehouse_outbound(selenium)
    wms.outbound_process(warehouse_id, do_num, is_yc_order,outbound_type)


if __name__ == '__main__':
    from public import test
    test.runtc(__file__,'test_do_out',driver='Chrome',
                options=['--warehouse_id=13','--do_num=7032777032',
                         '--is_yc_order=True','--outbound_type=1']) #True&False