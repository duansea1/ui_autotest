һ ���⻷��
1.�������⻷��
��ʽһ��ֱ��ʹ��pycharmרҵ����

��ʽ����
�ֶ�����
a.��װpipenv
b �������⻷�����������⻷����
pip shell
�����ǰ·���£�û�����⻷�������Զ�����������Ϊ����Ŀ��-�����
2������ڵ�ǰ·���£��Ѿ����������⻷������ֱ�ӽ��뵽�Ѵ��������⻷����

c�����������޸�Ϊ���⻷���еĽ�����
1���鿴��������·��
pipenv --venv
2\�޸Ľ�����
file--setting--project--add

�����django��Ŀ����
1���޸�pypip�ļ��е�url

2\����django����
ֱ����pycharm������django
�ֶ����أ���teminal-pipenv shell�������⻷���� ʹ��pip install django��


3������django��Ŀ����
a��django-admin startproject django_project .  ����django��Ŀ����django_projectΪ��Ŀ¼
b. a��django-admin startproject django_project   ����django��Ŀ������django_projectΪ��Ŀ¼
C:\Users\�κ���\myfiles\auto_files\ui_autotest\2022ui_autotest\2023sea_project\python_davance_programs\django_project>

4������django
a��python manage.py runserver
����������ʹ���������� 8080 �˿ڣ�
b.python manage.py runserver 8080
c.ֹͣdjango -->ctrl+C

d.-- pycharm רҵ�棬����������������add config-�����+--ѡ��django

5������git�汾����
a��pycharmרҵ����Դ�vcs-enable-ѡ��git
b��pycharm��������Դ�teminanl--��git init

�����ύ�汾
1\����Ŀ��Ŀ¼�´���.gitignore�ļ�����������а汾������ļ���ӵ��ļ���

2�����޸���ӵ��ݴ���
git add .
3\���ݴ�����������ӵ����زֿ�
git commit -m ��ע�͡�

�ġ�django��Ŀ���̽ṹ
1������Ŀͬ���İ�
 __init__ Ϊ���ļ�
 asgi.py ��������asciЭ��Ӧ�÷��������ļ������첽��Ŀ����ʱʹ��
 urls.py ���ڴ���ȫ��·��
 wsgi.py ��������wsgiЭ��Ӧ�÷��������ļ�

2����Ŀ��·���µ��ļ�
db.sqllite3--django��Ŀ�Դ������ݿ�
mange.py ���ڹ���django��Ŀ�Ĺ�����

�塢��Ӧ��
1������
1�������������ģ�鱣�ֶ���
2�����ã����������ģ����и���

2������
��ʽһ��python manage.py startapp myappsea����Ӧ�����ƣ�
��ʽ����רҵ�� tools-��run mange.py task--->ֱ������startapp ��Ӧ������

3��ע��
1����Ҫ��setting.py�е�installed����apps�н���ע��
2��ע�᷽����������
 -����Ӧ�����ơ�
 -����Ӧ�����ơ�.apps.myappsea Config

4����Ӧ�ýṹ
 migrations ���ڴ��Ǩ�ƽű�
 admin ��������admin��̨����վ��
 apps.py ���ڶ���ģ����
 models ���ڶ���ģ����
 tests ���ڶ��嵱ǰ��Ӧ�õĵ�Ԫ�����߼�
 views ���ڶ�����Ӧ�õ�ҵ���߼�


���������ݿ��в�������
1������ʹ��pymysqlģ��ִ��ԭ����sql���ȥ�������ݿ�
    a������sql���һ��Ƚϸ��ӣ�ά������
    b��sql���İ�ȫ���޷��õ����ϣ����ܻ���sqlע��ķ���
    c�����ݿ�Ĵ��������ݱ�����������ݱ����Լ����ݿ��Ǩ�Ʒǳ��鷳
    d��sql���������޷�����

2��ORM���
a�����ݿ⣺��Ҫ��ǰ׼�����ݿ�
b�����ݱ���ORM����е�ģ����һһ��Ӧ
c���ֶΡ�ģ���е������ԣ�filed���ࣩ
d����¼��������ģ����Ķ��ʵ��

3��mysql������Щ����
    a�����ݿ⣺
    b�����ݱ�
    c���ֶΣ�
    d����¼��
��Ǩ�ƽű���-ֻҪ�޸���model.py�ļ��е��ֶΣ���Ҫִ������
1�� python manage.py makemigrations projects  
2��python manage.py sqlmigrate myappsea 0002_projects
3��python manage.py migrate myappsea


