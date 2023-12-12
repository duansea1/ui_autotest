# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-14 16:52
# ---
import pytest
import logging
def init_data(fixture_value):
    if fixture_value == 1:
        return 'unsold'
    elif fixture_value == 2:
        value = 'onsale'
        return value
    elif fixture_value == 3:
        return 'sellout'
    else:
        return False

@pytest.fixture(params=[1, '参数2', 2], ids=init_data)
def my_fixture(request):
    req_param = request.param
    print('\n参数为【{}】,执行sql--插入【{}】状态的数据'.format(req_param, req_param))
    yield req_param
    print('\n执行sql--清理参数为【{}】的测试数据'.format(req_param, req_param))
    print("\n-------------------------")

def test_fixtures_01(my_fixture):
    print('\n 正在执行【{}】的case'.format(my_fixture))
    print(my_fixture)
    assert 1 == 1

class Test_case1:
    # def __init__(self):
    #     pass

    def test_sum_01(self, fixture_list):
        print('执行test_sum_01')
        fixture_list.append('a')
        print(f'a fixture_ex id = {fixture_list}')
        assert 2==2

    def test_nums_02(self, fixture_list):
        print('执行test_sum_01')
        fixture_list.append('b')
        print(f'b fixture_ex id = {fixture_list}')
        assert 2==23

class Test_case2:
    # def __init__(self):
    #     pass

    def test_sum_01(self, fixture_list):
        print('执行test_sum_01')
        fixture_list.append('c')
        print(f'c fixture_ex id = {fixture_list}')
        assert 2==2

if __name__ == "__main__":

    pytest.main('-s','--html')
    # 命令行执行：pytest '-k' 'onsale' ' test_my_fixture_params_and_ids.py
