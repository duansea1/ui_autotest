# coding = utf-8

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


if __name__ == "__main__":

    pass