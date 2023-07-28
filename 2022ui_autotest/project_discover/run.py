
# encoding = utf-8
import unittest


if __name__ == "__main__":
    # 加载当前目录下所有有效的测试模块， ”." 表示 当前目录
    testSuit = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(testSuit)