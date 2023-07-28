# coding = utf-8
import unittest
from HTMLTestRunner import HTMLTestRunner

class Calc(object):

    def add(self, x, y, *d):
        """
        :param x:
        :param y:
        :param d: *d 入参是个列表
        :return:
        """
        result = x + y
        print('result-----add1:', result, x, y)
        for i in d:
            result = result + i
        print('result-----add2:', result)
        return result

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


class SuiteTestCalc(unittest.TestCase):
    def setUp(self):
        self.c = Calc()

    @unittest.skip("skipping-过滤")
    def test_Sub(self):
        print('sub')
        self.assertEqual(self.c.sub(100, 34, 6), 60, "求差结果错误")

    def testAdd(self):
        print("add-case")
        self.assertEqual(self.c.add(2, 3, 4), 9, "求和结果错误")


class SuiteTestPow(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)
        self.b = Calc()

    def test_Pow(self):
        print("pow")
        self.assertEqual(self.b.add(2, 3, 4), 9, "pow求和结果错误")


if __name__ == "__main__":

    suite1 = unittest.TestLoader().loadTestsFromTestCase(SuiteTestCalc)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(SuiteTestPow)
    suite = unittest.TestSuite([suite1, suite2])
    # unittest.TextTestRunner(verbosity=2).run(suite)
    filename = r"C:\Users\Public\Documents\test.html"
    print("===============filename==============", filename)
    with open(filename, "wb") as fb:
        runner = HTMLTestRunner(stream=fb, title="测试报告-unittest", description="加减乘除的测试")
        runner.run(suite)
