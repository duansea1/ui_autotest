import unittest

#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here

class myclass(object):

    @classmethod
    def sum(cls, a, b):
        return a + b   # 将两个传入参数进行相加操作

    @classmethod
    def sub(cls, a, b):
        return a - b


class mytest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """初始化类固件"""
        print ("-------setUpClass-初始化固件")
    @classmethod
    def tearDown(cls):
        """重构类固件"""
        print("-------tearDownClass-重构固件")

    # 初始化工作
    def setUp(self):
        self.a = 3
        self.b = 1
        print("----setUp-初始化工作")

    # 清理推出工作
    def tearDown(self):
        print("-----tearDown-退出工作")

    # 具体的测试用例一定要以test开头
    def testsum(self):
        # 断言两个数之和的结果是否为4
        self.assertEqual(myclass.sum(self.a, self.b), 4, 'test sum -fail')

    def testsub(self):
        # 断言两个数只差是否为2
        res = 3/0
        self.assertEqual(myclass.sub(self.a, self.b), 2, 'test sub-fail')


if __name__ == '__main__':
    unittest.main()
