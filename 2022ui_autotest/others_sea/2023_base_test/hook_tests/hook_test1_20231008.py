# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月08日 9:37
# ---
import time
class LazyPerson(object):
    def __init__(self, name, hook=None):
        self.name = name
        self.watch_tv_func = hook
        self.have_dinner_func = hook

    def get_up(self):
        print("%s get up at:%s" % (self.name, time.time()))

    def get_to_sleep(self):
        print("%s get to sleep at:%s" % (self.name, time.time()))

    def register_tv_hook(self, watch_tv_func):
        self.watch_tv_func = watch_tv_func

    def register_dinner_hook(self, have_dinner_func):
        self.have_dinner_func = have_dinner_func

    def enjoy_a_lazy_day(self):
        # get up
        self.get_up()
        # time.sleep(1)
        # watch tv
        # check the watch_tv_func(hooked or  unhooked)
        if self.watch_tv_func is not None:
            print('开始执行了----')
            self.watch_tv_func(self.name, '12岁')           # 重点在这(self.name) 传参给函数
            print('执行结束----')
        # unhooked
        else:
            print('no tv to watch')
        time.sleep(0.5)

        # have dinner
        # check the have_dinner_func(hooked or unhooked)
        # hooked
        if self.have_dinner_func is not None:
            self.have_dinner_func   # (self.name)
        else:
            print('nothing to eat')

        time.sleep(1)
        self.get_to_sleep()

def watch_daydayup(name, age):
    print("%s : ：调用此函数The program ---day day up--- is funny!!!。。" % name, '年龄%s：'%age)


def watch_happyfamily(name):
    print("%s : The program ---happy family--- is boring!!!" % name)

def eat_meat(name):
    print("%s : The meat is nice!!!" % name)


def eat_hamburger(name):
    print("%s : The hamburger is not so bad!!!" % name)


if __name__ == "__main__":
    lazy_tom = LazyPerson('Tom')
    # lazy_jerry = LazyPerson('jery')

    # register hook
    lazy_tom.register_tv_hook(watch_tv_func=watch_daydayup)   # 注册钩子函数
    # lazy_tom.register_dinner_hook(eat_hamburger)

    # lazy_jerry.register_tv_hook(watch_daydayup)
    # lazy_jerry.register_dinner_hook(eat_hamburger)

    # eat a day
    lazy_tom.enjoy_a_lazy_day()
    # lazy_jerry.enjoy_a_lazy_day()

