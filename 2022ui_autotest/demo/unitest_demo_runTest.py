#encoding = utf - 8

import unittest
import random


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        # 初始化一个递增序列
        self.seq = range(10)

    def tearDown(self):
        pass

    def runTest(self):
        # 从序列seq中随机选取一个元素
        element = random.choice(self.seq)
        # 验证随机元素确实在列表中
        print('------验证随机数在其中-------')
        self.assertTrue(element in self.seq)


class TestDictValueFormatFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # 随机打乱原seq的顺序
        print('-------随机数字：', self.seq)
        random.shuffle(self.seq)
        self.seq.sort()   #paixu
        self.assertSetEqual(self.seq, range(10))
        # 验证执行函数时抛出了 TypeError 异常
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))

    if __name__ == '__main__':
        unittest.main()
        # testcase = TestSequenceFunctions.runTest()



