import pytest
from business.manage.manage_home import ManageSystem
from time import sleep

@pytest.mark.manage_2
def test_manage_subsystem(selenium):
    mgr=ManageSystem(selenium)
    mgr.login_with_account()
    sub_systems=mgr.get_all_subsystems('系统仓库')
    for subs in sub_systems:
        sub_name=subs.text.strip()
        print('检查：',sub_name)
        if sub_name=='配送管理系统':
            continue
        subs.click()
        sleep(2)
        mgr.switch_to_latest_windows()
        #print(selenium.current_window_handle)
        assert '该网页无法正常运作' not in selenium.page_source
        assert '404 Not Found' not in selenium.page_source
        selenium.close()
        mgr.switch_to_latest_windows()

        
if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'manage_2',driver='Chrome')