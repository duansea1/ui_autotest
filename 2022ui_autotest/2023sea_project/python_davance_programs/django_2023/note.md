一 虚拟环境
1.创建虚拟环境
方式一：直接使用pycharm专业创建

方式二：
手动创建
a.安装pipenv
b 创建虚拟环境并进入虚拟环境中
pip shell
如果当前路径下，没有虚拟环境，会自动创建，名称为：项目名-随机符
2、如果在当前路径下，已经创建了虚拟环境，则直接进入到已创建的虚拟环境中

c、将解释器修改为虚拟环境中的解释器
1、查看解释器的路径
pipenv --venv
2\修改解释器
file--setting--project--add

二、搭建django项目工程
1、修改pypip文件中的url

2\下载django程序
直接在pycharm中下载django
手动下载（打开teminal-pipenv shell进入虚拟环境中 使用pip install django）


3、创建django项目工程
a、django-admin startproject django_project .  创建django项目，以django_project为根目录
b. a、django-admin startproject django_project   创建django项目，新增django_project为根目录
C:\Users\段海洋\myfiles\auto_files\ui_autotest\2022ui_autotest\2023sea_project\python_davance_programs\django_project>

4、启动django
a、python manage.py runserver
下面的命令会使服务器监听 8080 端口：
b.python manage.py runserver 8080
c.停止django -->ctrl+C

d.-- pycharm 专业版，可以启动启动器，add config-》点击+--选择django

5、开启git版本管理
a、pycharm专业版可以打开vcs-enable-选择git
b、pycharm社区版可以打开teminanl--》git init

三、提交版本
1\在项目根目录下创建.gitignore文件，将无需进行版本管理的文件添加到文件中

2、将修改添加到暂存区
git add .
3\将暂存区的内容添加到本地仓库
git commit -m “注释”

四、django项目工程结构
1、与项目同名的包
 __init__ 为包文件
 asgi.py 用于启动asci协议应用服务的入口文件，在异步项目部署时使用
 urls.py 用于创建全局路由
 wsgi.py 用于启动wsgi协议应用服务的入口文件

2、项目根路径下的文件
db.sqllite3--django项目自带的数据库
mange.py 用于管理django项目的管理工具

五、子应用
1、意义
1）解耦：将各功能模块保持独立
2）复用：方便各功能模块进行复用

2、创建
方式一：python manage.py startapp myappsea（子应用名称）
方式二：专业版 tools-》run mange.py task--->直接输入startapp 子应用名称

3、注册
1）需要在setting.py中的installed——apps中进行注册
2）注册方法：有两种
 -“子应用名称”
 -“子应用名称”.apps.myappsea Config

4、子应用结构
 migrations 用于存放迁移脚本
 admin 用于配置admin后台管理站点
 apps.py 用于定义模型类
 models 用于定义模型类
 tests 用于定义当前子应用的单元测试逻辑
 views 用于定义子应用的业务逻辑


六、从数据库中操作数据
1、可以使用pymysql模块执行原生的sql语句去操作数据库
    a、备份sql语句一般比较复杂，维护困难
    b、sql语句的安全性无法得到保障，可能会有sql注入的风险
    c、数据库的创建、数据表的生产、数据备份以及数据库的迁移非常麻烦
    d、sql语句的性能无法保障

2、ORM框架
a、数据库：需要提前准备数据库
b、数据表：与ORM框架中的模型类一一对应
c、字段、模型中的类属性（filed子类）
d、记录：类似于模型类的多个实例

3、mysql中有哪些对象
    a、数据库：
    b、数据表：
    c、字段：
    d、记录：
【迁移脚本】-只要修改了model.py文件中的字段，需要执行如下
1、 python manage.py makemigrations projects  
2、python manage.py sqlmigrate myappsea 0002_projects
3、python manage.py migrate myappsea


针对myappsea中的view.py文件
---对项目操作的5个接口有哪些痛点--
a、大量重复的代码，冗余代码较多
b、数据校验麻烦，往往需要嵌套多级if判断，校验的复用性较差
c、代码没有统一的规范，代码维护差
d、获取项目列表数据时，有很多功能缺失
    没有分页、过滤筛选、排序功能
e、整个项目的痛点：
    1、没有提供认证授权功能
    2、没有提供限流功能
    3、传递参数形式比较单一、只支持json格式的参数，不支持xxx-form-urlencoded
    4、5个接口无法放在同一个类视图中

# **django restframwork**

在Django的REST framework（DRF）中，Field类用于定义序列化器（serializer）中的字段：
* 1、read_only: 如果设置为True，则此字段在序列化时将被包含，但在反序列化时将被忽略。这意味着，数据可以从模型或查询集中被读取并转换为Python数据类型，但不能从传入的请求数据中更新模型。
* 2、write_only: 如果设置为True，则此字段在反序列化时将被包含，但在序列化时将被忽略。这意味着，数据可以从传入的请求数据中更新模型，但不会包含在序列化后的输出中。
* 3、required: 通常用于指定字段是否必须出现在反序列化的数据中。如果设置为False，则字段可以为空或者不存在。默认为True，但如果字段设置了default参数，则required默认为False。
* 4、default: 如果未提供字段值，则使用此默认值。empty是一个特殊的标记值，用于表示没有默认值。
* 5、initial: 用于预填充HTML表单字段的值。这不会影响反序列化过程，只是用于在呈现表单时提供一个初始值。
* 6、source: 用于指定从对象实例中访问的字段名称。例如，如果source='user.email'，则序列化器将从关联的user对象中获取email字段。
* 7、label: 用于HTML表单字段的标签。如果没有提供，则通常使用字段名称，并将其转换为人类可读的格式。
* 8、help_text: 用于HTML表单字段的帮助文本。
* 9、style: 一个字典，包含用于控制如何渲染字段的键值对。这主要用于控制HTML表单字段的呈现方式。
* 10、error_messages: 一个字典，用于覆盖字段默认的错误消息。例如，您可以自定义“此字段是必需的”消息。
* 11、validators: 一个用于字段验证的函数列表。每个函数都应该接收一个参数（字段值）并引发一个ValidationError，如果验证失败的话。
* 12、allow_null: 如果设置为True，则None将被视为有效值。默认情况下，字段不允许None值，除非字段也有default=None设置。

一、创建序列化器对象
1、只传递instance
    a、调用is_valid方法会报错
    b、调用errors、validate_data会报错
    c、调用data属性，，可以进行序列化输出

2、只传递data参数
    a、必须调用is_valid方法开始对数据进行校验
    b、调用errors、validate_data不会报错；
    c、调用save方法会指定调用序列化器类的create方法
    d、调用data属性，，可以进行序列化输出
    （如果调用save方法并且update方法返回模型对象的话，那么会把模型对象作为序列化输出的源数据；如果
    没有调用save方法，那么会把validate_data作为序列化输出的源数据）
3、同时传递instance和data参数