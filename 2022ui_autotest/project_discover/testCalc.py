# coding = utf-8

import unittest
from Calc import Calc

class Mytest(unittest.TestCase):
    c = None

    @classmethod
    def setUpClass(cls):
        print("单元测试前，创建Calc类的实例")

    # 具体的测试用例，一定要以test开头
    def test_add(self):
        print("run add()")
        self.assertEqual(Calc.add(self, 1, 2, 12), 15, 'test[ success!!!!!!!!')

    def sub(self, x, y, *d):
        result = x -y
        for i in d:
            result -= i
        return result

    @classmethod
    def mul(cls, x, y, *d):
        # 乘法运算
        result = x * y
        for i in d:
            result *= i
        return result

    @classmethod
    def div(cls, x, y, *d):
        # 除法运算
        if y != 0:
            result = x / y
        else:
            return -1
        for i in d:
            if i != 0:
                result /= i
            else:
                return -1
        return result