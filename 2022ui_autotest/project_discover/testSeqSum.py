
# encoding = utf-8
import unittest


class MytestCase_SeqSum(unittest.TestCase):

    def testEqual(self):
        seq = \
            range(11)
        self.assertNotEqual(sum(seq), 56, "断言列表元素之和结果错误")
        return {"ret": 0}
