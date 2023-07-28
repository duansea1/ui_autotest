#encoding = utf - 8

# 忽略某个测试用例
import unittest
import random
import sys


class TestSequenceFunctions1(unittest.TestCase):
    a = 1

    def setUp(self):
        # 初始化一个递增序列
        self.seq = list(range(10))

    def tearDown(self):
        pass

    def runTest(self):
        # 从序列seq中随机选取一个元素
        element = random.choice(self.seq)
        # 验证随机元素确实在列表中
        print('------验证随机数在其中-------')
        self.assertTrue(element in self.seq)


class TestDictValueFormatFunctions(unittest.TestCase):
    a = 1

    def setUp(self):
        self.seq = list(range(10))

    @unittest.skip("skipping-第一条case")
    def test_shuffle(self):
        # 随机打乱原seq的顺序
        print('-------随机数字：', self.seq)
        random.shuffle(self.seq)
        self.seq.sort()   #paixu
        self.assertSetEqual(self.seq, range(10))
        # 验证执行函数时抛出了 TypeError 异常
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))

    # 如果a大于5则忽略该测试方法
    @unittest.skipIf(a > 5, "condition is not satisfied")
    def test_choice(self):
        # 从序列seq中随机选取一个元素
        element = random.choice(self.seq)
        # 验证随机元素确实在列表中
        print('------验证随机数在其中-------')
        self.assertTrue(element in self.seq)

    # 除非执行用例的平台是window平台，否则忽略该测试方法
    @unittest.skipUnless(sys.platform.startswith('linux'), 'requires Windows')
    def test_sample(self):
        # 验证执行的语句是否出现了异常
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

    if __name__ == '__main__':
        # unittest.main()
        # testcase = TestSequenceFunctions.runTest()
        testClass = unittest.TestLoader().loadTestsFromTestCase(TestDictValueFormatFunctions)
        suite = unittest.TestSuite(testClass)
        unittest.TextTestRunner(verbosity=2).run(suite)



