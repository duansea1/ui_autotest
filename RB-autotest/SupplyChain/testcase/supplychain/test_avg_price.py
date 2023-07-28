"""
Created on 2019/3/12
@author: liya
"""

import pytest
from business.pms.avg_price import Pms_Avg_Price

@pytest.mark.pms_2
def test_avg_price_assert(selenium):
    '''计算平均价是否正确'''
    p = Pms_Avg_Price(selenium)
    p.avg_price()   # 计算平均价
    p.assert_avg_price()  # 校验计算平均价和库中的平均价是否一致
    # p.clear_file('pms_avg_price.txt')  # 清空文件内容


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='pms_2', driver='Chrome')  # Firefox，Chrome
