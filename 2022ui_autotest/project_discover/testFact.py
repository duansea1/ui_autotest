
#encoding = utf-8
"""unittest-以test开始定义方法， 断言每个case都应该有"""
import unittest
from Calc import Calc
from functools import reduce


class MytestCase_testFact(unittest.TestCase):

    def setUp(self):
        self.num = 5

    def testFactorial(self):
        # 生成一个递增序列
        seq = range(1, self.num + 1)
        # 求阶乘
        res = reduce(lambda x, y: x * y, seq)
        # 断言阶乘结果
        print("断言阶乘结果")
        # self.assertEqual(res, 120, "断言阶乘结果错误")
