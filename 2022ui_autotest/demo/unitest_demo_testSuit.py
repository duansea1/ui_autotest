#encoding = utf - 8

import unittest
import random


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        # 初始化一个递增序列
        self.seq = range(10)

    def tearDown(self):
        pass

    def test_choice(self):
        # 从序列seq中随机选取一个元素
        element = random.choice(self.seq)
        # 验证随机元素确实在列表中
        print('------验证随机数在其中-------')
        self.assertTrue(element in self.seq)

    def test_sample(self):
        # 验证执行的语句是否出现了异常
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)


class TestDictValueFormatFunctions(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)

    def tearDown(self):
        pass

    def test_shuffle(self):
        # 随机打乱原seq的顺序
        print('-------随机数字：', self.seq)
        # random.shuffle将列表随机打乱
        random.shuffle(list(self.seq))
        list(self.seq).sort()   #paixu
        self.assertEqual(self.seq, range(10))
        # 验证执行函数时抛出了 TypeError 异常
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))

    if __name__ == '__main__':
        """
        TestLoader类：测试用例加载器，返回一个测试用例集合
        LoadTestFromTestCase类：根据给定的测试类，获取其中的所有以“test”开头的测试方法，并返回一个测试集合
        TestSuit类  组装测试用例的实例，其中Text 表示以文本形式输出测试结果
        """
        # 根据给定的测试类，获取其中的所有以test开头的测试方法，并返回一个测试套件
        testCase1 = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
        testCase2 = unittest.TestLoader().loadTestsFromTestCase(TestDictValueFormatFunctions)
        #将多个测试类加载到 测试套件中
        suite = unittest.TestSuite([testCase1, testCase2])
        # 设置verbosity = 2，可以打印更详细的执行信息
        unittest.TextTestRunner(verbosity=2).run(suite)





