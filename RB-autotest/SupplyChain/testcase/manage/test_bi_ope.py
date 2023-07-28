'''
Created on 2018年5月7日

@author: geqiuli
'''
import pytest
from business.manage.manage_home import ManageSystem
from business.manage.bi_ope import ope_home

@pytest.mark.manage_0
def test_ope_home(selenium):
    '''bi 数据中心：页面正常打开'''
    mgr=ManageSystem(selenium)
    mgr.login_with_account('1')   #登录集成管理后台
    ope_html=mgr.chose_module('数据中心','系统仓库')    #打开“数据中心”
    assert '502 Bad Gateway' not in ope_html
    assert 'qa_manage' in ope_html
    ope_home(selenium)  #显示数据中心左侧菜单

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'manage_0',driver='Chrome')