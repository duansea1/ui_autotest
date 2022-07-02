# encoding = utf-8
# 在远程服务上，增加注释
# 在远程分支master修改，第一次
import unittest
from Calc import Calc

class Mytest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("单元测试前，创建Calc类的实例")
        cls.c = Calc()   # 实例化calc

    # 具体的测试用例
    def test_add(self):
        print("run test_add")
        self.assertEqual(Mytest.c.add(1, 2, 12), 15, 'test add fail')

    def test_sub(self):
        print("run test_sub")
        self.assertEqual(Mytest.c.sub(2, 1, 3), -2, 'test sub fail')

    def test_mul(self):
        print("run test_mul")
        self.assertEqual(Mytest.c.mul(2, 3, 5), 30, 'test mul fail')

    def test_div(self):
        print("run test_div")
        self.assertEqual(Mytest.c.div(8, 2, 4), 2, 'test div fail')

if __name__ == "__main__":
    unittest.main()
