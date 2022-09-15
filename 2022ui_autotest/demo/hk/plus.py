# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月05日 19:58
# ---
import pluggy

# HookspecMarker 和HOOKimplMarker 实际上是一个装饰器带参数的装饰器类，作用是给函数增加额外的属性设置
hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")

# 定义自己的Spec,这里可以理解未定义接口类
class MySpec:
    # hookspec是个装饰类中的方法的装饰器，为此方法增额外的属性设置，这里的myhook可以理解未定义了一个接口
    @hookspec
    def myhook(self, arg1, arg2):
        print("myhook-Myspec")
        # pass


    # 定义一个插件
class Plugin_1:
    # 插件中实现了上面定义的接口，同样这个实现接口的方法用hookimpl装饰器装饰，功能是返回两个参数的和
    @hookimpl
    def myhook(self, arg1, arg2):
        print("inside Plugin_1.myhook()")
        return arg1 + arg2

# 定义第二个插件
class Plugin_2:
    # 插件中实现了上面定义的接口，同样这个实现接口方法用 hookimpl装饰器装饰，功能是返回两个参数的差
    @hookimpl
    def myhook(self, arg1, arg2):
        print("inside PLugin_2.myhook()")
        return arg1 - arg2

# 实例化一个插件管理的对象，注意这里的名称要与文件开头定义装饰器的时候的名称一致
pm = pluggy.PluginManager("myproject")

# 将自定义的接口类加到钩子定义中
pm.add_hookspecs(MySpec)

# 注册定义的两个插件
pm.register(Plugin_1())
pm.register(Plugin_2())

# 通过插件管理对象的钩子调用方法，这时候这两个插件中的这个方法会执行，而且遵循后注册先执行即LIFO的原则，两个插件的结果将以列表形式返回
results = pm.hook.myhook(arg1=1, arg2=2)
print(results)