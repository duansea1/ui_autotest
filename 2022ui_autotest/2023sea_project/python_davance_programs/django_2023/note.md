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


