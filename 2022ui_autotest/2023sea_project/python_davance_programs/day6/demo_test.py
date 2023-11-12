
# 什么是单例模式
# 什么是装饰器，带参数的装饰器的调用顺序
# __new__ 和__init__的区别
# supershi shenm

# 实现一个类，前5次创建对象，以后创建返回5个中的一个
import random
class Myclass(object):
    objs = []

    def __new__(cls, *args, **kwargs):
        if len(cls.objs) < 5:
            obj = super().__new__(cls)
            cls.objs.append(obj)
        else:
            obj = random.choice(cls.objs)
        return obj
