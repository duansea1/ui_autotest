# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-15 15:06
# ---
import pytest

@pytest.fixture(scope='session')

def fixture_list():
    l = []
    yield l