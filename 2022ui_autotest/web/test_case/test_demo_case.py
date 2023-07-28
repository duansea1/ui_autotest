
import pytest
from web.data.data import *
from pytest_assume.plugin import assume


@pytest.mark.assume1
def test_assume():
    a, b = 1, 2
    assume(a > b)
    # assert a == b


def test_error():
    pass


@pytest.mark.xfail(reason='always xpass')
def test_xpass():
    pass

@pytest.mark.demo
@pytest.mark.xfail(reason='always xfail')
def test_xfail():
    assert False


# @pytest.mark.skip(reason="skip the case")
@pytest.mark.demo1
@pytest.mark.parametrize("i", [1, 2, 3, 4])
def test_skip(i):
    print(i)
    pass


@pytest.mark.excel
@pytest.mark.parametrize("name,mobile,prince,city,county,adress,alisa,is_default,msg",
                         read_excel(filename="ddt_test_new_adress.xlsx"))
def test_print_excel(name,
                     mobile,
                     prince,
                     city,
                     county,
                     adress,
                     alisa,
                     is_default,
                     msg):
    print("excel文件：", name,
          mobile,
          prince,
          city,
          county,
          adress,
          alisa,
          is_default,
          msg)


pytest.main(["-vrA", "-vs", "-m=assume1"])
